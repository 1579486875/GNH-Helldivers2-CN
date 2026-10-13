# -*- coding: utf-8 -*-
"""解析 HD2 minidump：提取异常代码、异常地址、模块列表，定位崩溃位置"""
import os, struct, sys, glob

D = os.path.join(os.environ['APPDATA'], 'Arrowhead', 'Helldivers2', 'dumps')

STREAM = {3: 'ThreadList', 4: 'ModuleList', 5: 'MemoryList', 6: 'Exception',
          7: 'SystemInfo', 9: 'Memory64List', 11: 'MiscInfo', 12: 'MemoryInfoList',
          15: 'MiscInfo2', 16: 'MemoryInfoList2'}

MINIDUMP_HEADER = '<IIIIIIQ'   # sig, ver, streams, dirRva, checksum, ts, flags


def read_str(raw, rva):
    ln, = struct.unpack_from('<I', raw, rva)
    return raw[rva + 4:rva + 4 + ln].decode('utf-16-le', 'replace')


def parse(path):
    raw = open(path, 'rb').read()
    sig, ver, nstreams, dirrva = struct.unpack_from('<IIII', raw, 0)
    out = {'sig': raw[:4], 'nstreams': nstreams, 'size': len(raw)}
    if raw[:4] != b'MDMP':
        out['error'] = 'not a minidump'
        return out
    streams = {}
    for i in range(nstreams):
        stype, dsize, rva = struct.unpack_from('<III', raw, dirrva + 12 * i)
        streams.setdefault(stype, []).append((dsize, rva))

    # SystemInfo
    if 7 in streams:
        _, rva = streams[7][0]
        arch, level, build, plat = struct.unpack_from('<HHII', raw, rva)
        out['arch'] = {0: 'x86', 9: 'x64', 5: 'ARM'}.get(arch, arch)
        out['os_build'] = build

    # ModuleList
    mods = []
    if 4 in streams:
        _, rva = streams[4][0]
        n, = struct.unpack_from('<I', raw, rva)
        for i in range(n):
            base_rva = rva + 4 + i * 108
            base, size, cksum, tds, name_rva = struct.unpack_from('<QIIII', raw, base_rva)
            try:
                nm = read_str(raw, name_rva)
            except Exception:
                nm = '?'
            mods.append((base, size, nm))
    out['modules'] = mods

    # Exception
    exc = None
    if 6 in streams:
        _, rva = streams[6][0]
        tid, align = struct.unpack_from('<II', raw, rva)
        # EXCEPTION_RECORD at rva+8
        code, flags, nrec, addr = struct.unpack_from('<IIQQ', raw, rva + 8)
        nparam, = struct.unpack_from('<I', raw, rva + 0x28)
        params = struct.unpack_from('<15Q', raw, rva + 0x30)
        exc = {'thread': tid, 'code': code, 'flags': flags, 'address': addr,
               'nparam': nparam, 'params': params[:min(nparam, 15)]}
    out['exception'] = exc

    # 找到异常地址落在哪个模块
    if exc and mods:
        for base, size, nm in mods:
            if base <= exc['address'] < base + size:
                out['faulting_module'] = nm
                out['fault_offset'] = exc['address'] - base
                break
    return out


def main():
    files = sorted(glob.glob(os.path.join(D, '*.dmp')), key=os.path.getmtime, reverse=True)
    if len(sys.argv) > 1:
        files = [os.path.join(D, sys.argv[1])] + files
    CODES = {0xC0000005: 'ACCESS_VIOLATION', 0xC000001D: 'ILLEGAL_INSTRUCTION',
             0xC0000094: 'INTEGER_DIVIDE_BY_ZERO', 0xC0000096: 'PRIVILEGED_INSTRUCTION',
             0xC00000FD: 'STACK_OVERFLOW', 0xC0000374: 'HEAP_CORRUPTION',
             0x80000003: 'BREAKPOINT', 0xE06D7363: 'C++ EXCEPTION',
             0xC0000409: 'STACK_BUFFER_OVERRUN/FASTFAIL', 0xC0000602: 'FAIL_FAST'}
    for p in files[:7]:
        r = parse(p)
        print('=' * 100)
        print('文件: %s  (%.1f KB, %s)' % (os.path.basename(p), os.path.getsize(p) / 1024,
                                        __import__('datetime').datetime.fromtimestamp(os.path.getmtime(p))))
        print('  streams=%d  arch=%s' % (r.get('nstreams', -1), r.get('arch')))
        e = r.get('exception')
        if e:
            print('  ★ 异常: %s (0x%08X)  地址=0x%X  参数=%s'
                  % (CODES.get(e['code'], 'code'), e['code'], e['address'],
                     [hex(x) for x in e['params'] if x][:4]))
            if r.get('faulting_module'):
                print('  ★ 出错模块: %s  +0x%X' % (r['faulting_module'], r['fault_offset']))
            else:
                print('  ★ 出错模块: (地址不在任何已加载模块内)')
        mods = r.get('modules', [])
        print('  模块数: %d' % len(mods))
        # 只显示与游戏/mod/反作弊相关的模块
        keys = ('helldivers', 'GameGuard', 'npgg', 'npgm', 'npsc', 'steam', 'd3d', 'dxgi', 'nvidia',
                'lua', 'stingray', 'bitsquid', 'crs', 'overlay', 'nvoglv', 'amd', 'atio')
        for base, size, nm in mods:
            low = nm.lower()
            if any(k.lower() in low for k in keys):
                print('    0x%012X  %10d  %s' % (base, size, nm))
    print('=' * 100)


main()
