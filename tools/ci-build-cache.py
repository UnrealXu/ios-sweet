#!/usr/bin/env python3
"""Prepare disposable CI sources and record compiler-cache evidence.

Never restore fakeroot, generated headers, kernel objects, or a linked kernel.
XNU's native CCACHE make variable handles compiler/flag/source/header checks.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

SOURCE_REPOS = ('xnu', 'bootstrap_cmds', 'dtrace', 'AvailabilityVersions',
                'Libsystem', 'libplatform', 'libdispatch')


def command(argv):
    return subprocess.check_output(argv, text=True).strip()


def reset_sources(dxb):
    """Only disposable dependency checkouts below the explicit dxb directory."""
    dxb = dxb.resolve()
    if dxb.name != 'dxb' or not (dxb / '.git').is_dir():
        raise ValueError('expected disposable dxb Git checkout')
    if (dxb / 'build').exists() or (dxb / 'fakeroot').exists():
        raise ValueError('object/fakeroot reuse is not supported by this cache')
    for name in SOURCE_REPOS:
        repo = dxb / name
        if not repo.exists():
            continue
        if repo.is_symlink() or not (repo / '.git').is_dir():
            raise ValueError('invalid cached source checkout: ' + name)
        # Remove previous patches and staged untracked providers. Reapply the
        # current checkout's patches; never reuse patched sources as-is.
        subprocess.run(['git', '-C', str(repo), 'reset', '--hard', 'HEAD'], check=True)
        subprocess.run(['git', '-C', str(repo), 'clean', '-ffdx'], check=True)


def identity(output):
    fingerprint = '\n'.join(command(args) for args in [
        ['xcodebuild', '-version'], ['xcrun', 'clang', '--version'],
        ['xcrun', '--sdk', 'macosx', '--show-sdk-version'], ['uname', '-m']])
    key = hashlib.sha256(fingerprint.encode()).hexdigest()[:24]
    with output.open('a') as stream:
        stream.write('toolchain=' + key + '\n')
    print(fingerprint)
    print('Toolchain cache identity:', key)


def prepare(workspace, mode):
    if command(['git', '-C', str(workspace / 'dxb'), 'rev-parse', 'HEAD']) != os.environ['DXB_SHA']:
        raise ValueError('disposable dxb does not match the pinned build recipe')
    reset_sources(workspace / 'dxb')
    if mode == 'cached':
        kdks = workspace / '.ci-cache/kdks'
        if kdks.is_dir():
            subprocess.run(['sudo', 'mkdir', '-p', '/Library/Developer/KDKs'], check=True)
            subprocess.run(['sudo', 'ditto', str(kdks), '/Library/Developer/KDKs'], check=True)
        cache = workspace / '.ci-cache/ccache'
        cache.mkdir(parents=True, exist_ok=True)
        config = workspace / '.ci-cache/ccache.conf'
        config.write_text('compiler_check = content\nsloppiness =\nmax_size = 1G\n')
        # Hosted jobs use the same workspace path. Do not rewrite __FILE__
        # strings just to enable relocatable caches; preserve uncached output.
        values = dict(CCACHE=shutil.which('ccache'), CCACHE_DIR=str(cache),
                      CCACHE_BASEDIR='', CCACHE_COMPILERCHECK='content',
                      CCACHE_CONFIGPATH=str(config))
        if not values['CCACHE']:
            raise ValueError('ccache was not installed')
        os.environ.update(values)
        with Path(os.environ['GITHUB_ENV']).open('a') as stream:
            for key, value in values.items():
                stream.write(f'{key}={value}\n')
        subprocess.run(['ccache', '--max-size', '1G'], check=True)
        subprocess.run(['ccache', '--zero-stats'], check=True)
    else:
        with Path(os.environ['GITHUB_ENV']).open('a') as stream:
            stream.write('CCACHE=\nCCACHE_DISABLE=1\n')


def report(workspace, seconds, status, mode):
    metrics = dict(build_seconds=seconds, build_exit_code=status, build_mode=mode,
                   cache_policy='fresh source patches/headers/make/link; compiler cache only')
    if mode == 'cached':
        stats = command(['ccache', '--print-stats'])
        metrics['ccache_stats'] = dict(line.split() for line in stats.splitlines())
        print(command(['ccache', '--show-stats', '--verbose']))
        # KDK files are public vendor dependencies; never commit these to Git.
        kdks = Path('/Library/Developer/KDKs')
        if kdks.is_dir() and not (workspace / '.ci-cache/kdks').exists():
            shutil.copytree(kdks, workspace / '.ci-cache/kdks',
                            dirs_exist_ok=True, symlinks=True)
    (workspace / 'build-metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    print(json.dumps(metrics, indent=2))
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with Path(summary).open('a') as stream:
            stream.write(f'### XNU build measurement\n\nMode: `{mode}`; Build: **{seconds}s**; exit: `{status}`.\n\n')
            if mode == 'cached':
                stream.write('```text\n' + command(['ccache', '--show-stats']) + '\n```\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['identity', 'prepare', 'report'])
    parser.add_argument('--workspace', type=Path, default=Path.cwd())
    parser.add_argument('--mode', choices=['cached', 'full'], default='cached')
    parser.add_argument('--seconds', type=int, default=0)
    parser.add_argument('--status', type=int, default=0)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if args.action == 'identity':
        identity(Path(os.environ['GITHUB_OUTPUT']))
    elif args.action == 'prepare':
        prepare(workspace, args.mode)
    else:
        report(workspace, args.seconds, args.status, args.mode)


if __name__ == '__main__':
    main()
