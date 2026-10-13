# -*- coding: utf-8 -*-
"""检查所有汉化包 patch 的记录区是否有脏数据（非 0 保留字段 / 错误 bundleId）"""
import os, struct

M = os.path.join(os.environ['LOCALAPPDATA'], 'hd2arsenal', 'mods')

# 标准：entry 记录的 +0x18..+0x30 与 +0x40/+0x48 之外，保留字段应为 0
BUNDLE_ID = 11623383793923069922


def check(tag, path, ref_bundle=None):
    if not os.path.exists(path):
        print('%-34s 不存在' % tag)
        return None
    raw = open(path, 'rb').read()
    cnt, = struct.unpack_from('<I', raw, 0x08)
    print('=' * 88)
    print('%s  大小=%d  entries=%d' % (tag, len(raw), cnt))
    problems = 0
    for i in range(cnt):
        b = 0x68 + 80 * i
        vals = [struct.unpack_from('<Q', raw, b + 8 * k)[0] for k in range(10)]
        res_id, bundle, off = vals[0], vals[1], vals[2]
        tail_zeros = vals[3:7]          # +0x18..+0x30 期望 0
        length = vals[7]                # +0x38
        extra = vals[8:]                # +0x40, +0x48
        bad = []
        if ref_bundle is not None and bundle != ref_bundle:
            bad.append('bundleId=%d (期望 %d)' % (bundle, ref_bundle))
        if any(tail_zeros):
            bad.append('保留字段非 0: %s' % tail_zeros)
        print('  entry %d: res_id=%d off=0x%X len=%d bundleId=%d' % (i, res_id, off, length, bundle))
        print('           +0x18..0x30=%s  +0x40=%d +0x48=%d' % (tail_zeros, extra[0], extra[1]))
        if bad:
            problems += 1
            for x in bad:
                print('           ★ 问题: %s' % x)
    print('  => 问题 entry 数: %d' % problems)
    return problems


TOTAL = 0
TOTAL += check('pack A (GNH简体中文汉化包)', os.path.join(M, 'GNH简体中文汉化包-Hellldivers2_AR395600', 'Addon', '9ba626afa44a3aa3.patch_0'), BUNDLE_ID) or 0
TOTAL += check('pack B (Transmog汉化)', os.path.join(M, 'GNH-Transmog界面汉化-可选包_AR971368', 'Addon', '9ba626afa44a3aa3.patch_0'), BUNDLE_ID) or 0
TOTAL += check('孤儿包 GNH-Chinese-Simplified-Pack', os.path.join(M, 'GNH-Chinese-Simplified-Pack', 'Addon', '9ba626afa44a3aa3.patch_0'), BUNDLE_ID) or 0
TOTAL += check('孤儿包 GNH-Transmog-CN-Addon', os.path.join(M, 'GNH-Transmog-CN-Addon', 'Addon', '9ba626afa44a3aa3.patch_0'), BUNDLE_ID) or 0
TOTAL += check('10-5 旧版 pack A（可用基准）', r'C:\Users\asus\AppData\Local\Temp\dsh-hd2\old_pack\Addon\9ba626afa44a3aa3.patch_0', BUNDLE_ID) or 0
print()
print('总问题数:', TOTAL)
