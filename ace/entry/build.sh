#!/bin/sh
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
out="$repo/research/ace-entry-20261019"
address= bytes=
while [ "$#" -gt 0 ]; do
    case "$1" in
        --output-dir) [ "$#" -ge 2 ] || exit 2; out=$2; shift 2;;
        --pmsg-ram) [ "$#" -ge 3 ] || exit 2; address=$2; bytes=$3; shift 3;;
        *) echo "Usage: $0 [--output-dir DIR] [--pmsg-ram ADDRESS BYTES]" >&2; exit 2;;
    esac
done
out=$(python3 - "$repo" "$out" "$address" "$bytes" <<'PYCONFIG'
from pathlib import Path
import hashlib,json,sys,subprocess
r=Path(sys.argv[1]);out=Path(sys.argv[2]).expanduser().resolve();a,n=sys.argv[3:5]
if not out.is_relative_to(r/'research'):
    raise SystemExit('Output must be inside ignored research/')
if subprocess.run(['git','-C',str(r),'check-ignore','--quiet','--',str(out.relative_to(r))]).returncode:
    raise SystemExit('Output is not git-ignored')
config={'enabled':bool(a or n)}
if config['enabled']:
    address,size=int(a,0),int(n,0)
    if address<=0 or address%4 or not 13<=size<=0x7fffffff+12 or address+size>0xffffffffffffffff:
        raise SystemExit('Invalid explicit ordinary-RAM ring address/size')
    config.update(address=hex(address),bytes=size)
import importlib.util
spec=importlib.util.spec_from_file_location('pack',r/'tools/ace-probe-boot.py')
pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
p=r/'research/ace-offline/probe';d=json.loads((p/'verification.json').read_text())
pack.validate_probe((p/'probe.Image').read_bytes(),d,r/'probe')
out.mkdir(parents=True,exist_ok=True)
result=out/'verification.json'
if result.exists() and json.loads(result.read_text()).get('status')=='pass':
    result.replace(result.with_name('verification.prebuild.json'))
result.write_text(json.dumps({'status':'incomplete','reason':'entry image build requested; run verification'})+'\n')
(out/'pmsg-config.json').write_text(json.dumps(config,indent=2)+'\n')
header='#define ACE_ENTRY_PMSG_ENABLED '+str(int(config['enabled']))+'\n'
if config['enabled']:
    header+='#define ACE_ENTRY_PMSG_ADDRESS '+hex(address)+'\n#define ACE_ENTRY_PMSG_BYTES '+str(size)+'\n'
(out/'entry_config.h').write_text(header)
print(out)
PYCONFIG
)
cp "$repo/research/ace-offline/probe/probe.Image" "$out/probe.Image"
cp "$repo/research/ace-offline/probe/probe.elf" "$out/probe.elf"
aarch64-linux-gnu-gcc -march=armv8-a -nostdlib -I "$out" -c "$repo/ace/entry/start.S" -o "$out/start.o"
aarch64-linux-gnu-ld -T "$repo/ace/entry/linker.ld" "$out/start.o" -o "$out/entry.elf"
aarch64-linux-gnu-objcopy -O binary "$out/entry.elf" "$out/entry.Image"
aarch64-linux-gnu-objdump -dr "$out/entry.elf" > "$out/disassembly.txt"
aarch64-linux-gnu-readelf -rW "$out/start.o" > "$out/relocations.txt"
if aarch64-linux-gnu-nm -u "$out/entry.elf" | rg .; then exit 1; fi
if rg 'R_AARCH64_(ABS|PREL64|GLOB|JUMP_SLOT)' "$out/relocations.txt"; then exit 1; fi

python3 - "$repo" "$out" <<'PYMANIFEST'
from pathlib import Path
import hashlib,json,sys
r,o=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(o/'build-manifest.json').write_text(json.dumps({'status':'UNTESTED hardware',
 'image_sha256':sha(o/'entry.Image'),'probe_sha256':sha(o/'probe.Image'),
 'probe_elf_sha256':sha(o/'probe.elf'),'entry_config_sha256':sha(o/'entry_config.h'),
 'pmsg':json.loads((o/'pmsg-config.json').read_text()),
 'sources':{n:sha(r/'ace/entry'/n) for n in ['start.S','pmsg.S','linker.ld','build.sh']}},indent=2)+'\n')
PYMANIFEST
