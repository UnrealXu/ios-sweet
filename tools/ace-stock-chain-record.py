#!/usr/bin/env python3
"""Decode the unique pre-handoff record from a saved pmsg capture; no device I/O."""
import argparse
import json
from pathlib import Path
import re
import struct

def decode(data,token,expect_ace=False):
    if not isinstance(data,bytes) or len(data)>1024*1024:raise ValueError('Invalid/oversized capture')
    if not re.fullmatch('[0-9a-f]{24}',token):raise ValueError('Invalid build token')
    marker=('ACECHAIN1:'+token+': forwarding original Android kernel\n').encode()
    if data.count(marker)!=1:raise ValueError('Missing or ambiguous current build marker')
    at=data.index(marker)+len(marker)
    raw=data[at:at+80]
    if len(raw)!=80 or raw[:8]!=b'ACECHN01':raise ValueError('Missing/truncated raw record')
    v=struct.unpack('<10Q',raw)
    if v[1]!=1 or v[3] not in [4,8] or v[4]&((1<<25)|5) or v[8]!=0:
        raise ValueError('Invalid pre-handoff stage/control/logger state')
    if not v[2] or v[2]&7 or not v[7] or v[9]&0x1fffff or v[9]<0x200000:
        raise ValueError('Invalid DT/timer/kernel entry values')
    if expect_ace and (v[7]!=13000000 or v[6]!=0x101122 or v[5] not in [0x412fd050,0x411fd411]):
        raise ValueError('Record does not match observed Ace CPU/timer facts')
    return dict(marker_token=token,offset=at,stage='before-stock-kernel-branch',incoming_x0=hex(v[2]),
                incoming_el=v[3]//4,active_sctlr=hex(v[4]),midr=hex(v[5]),mmfr0=hex(v[6]),
                cntfrq_hz=v[7],logger_status=0,stock_entry_pa=hex(v[9]),
                scope='Pre-handoff diagnostic record only; Android continuation requires separate evidence; NOT iOS')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('capture',type=Path);p.add_argument('--token',required=True);p.add_argument('--expect-ace',action='store_true');a=p.parse_args()
    with a.capture.open('rb') as f:data=f.read(1024*1024+1)
    print(json.dumps(decode(data,a.token,a.expect_ace),indent=2))

if __name__=='__main__':main()
