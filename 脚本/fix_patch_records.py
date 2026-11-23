# -*- coding: utf-8 -*-
"""修复 pack A：还原完整版（恢复 Bingus 翻译包）+ 清干净 entry 1 的记录区

用法:
  python fix_packA.py --dry     只检查
  python fix_packA.py --write   执行修复
  python fix_packA.py --restore 还原为最初备份
"""
import os, struct, sys, shutil, glob, datetime

M = os.path.join(os.environ['LOCALAPPDATA'], 'hd2arsenal', 'mods')
ADDON = os.path.join(M, 'GNH简体中文汉化包-Hellldivers2_AR395600', 'Addon')
PACK = os.path.join(ADDON, '9ba626afa44a3aa3.patch_0')
BK_DIR = os.path.join(ADDON, 'patch_backup_before_test')

BUNDLE_ID = 11623383793923069922
F40 = 68719476736          # 0x1000000000
F48 = 4294967312           # 0x100000010（取自 10-5 可用版 entry1）
F48_ENTRY0 = 16

DRY = '--dry' in sys.argv
WRITE = '--write' in sys.argv
RESTORE = '--restore' in sys.argv

if RESTORE:
    baks = sorted(glob.glob(os.path.join(BK_DIR, 'patch_0.*')))
    if not baks:
        print('没有备份'); sys.exit(1)
    shutil.copy2(baks[0], PACK)
    print('已还原:', baks[0])
    sys.exit(0)

# 1) 若当前是诊断版，先从备份还原成完整版
baks = sorted(glob.glob(os.path.join(BK_DIR, 'patch_0.*')))
cur = open(PACK, 'rb').read()
if baks and b'GNH-DIAG' in cur:
    print('检测到当前是诊断版，先从备份还原完整版:', os.path.basename(baks[0]))
    if not DRY:
        shutil.copy2(baks[0], PACK)
        cur = open(PACK, 'rb').read()
else:
    print('当前不是诊断版（或没有备份），直接检查')

raw = bytearray(cur)
print('patch 大小: %d' % len(raw))
cnt, = struct.unpack_from('<I', raw, 0x08)
print('entries: %d' % cnt)

CHANGES = []
for i in range(cnt):
    b = 0x68 + 80 * i
    res_id, = struct.unpack_from('<Q', raw, b)
    bundle, = struct.unpack_from('<Q', raw, b + 0x08)
    off, = struct.unpack_from('<Q', raw, b + 0x10)
    length, = struct.unpack_from('<I', raw, b + 0x38)
    tail = [struct.unpack_from('<Q', raw, b + 8 * k)[0] for k in (3, 4, 5, 6)]
    f40, = struct.unpack_from('<Q', raw, b + 0x40)
    f48, = struct.unpack_from('<Q', raw, b + 0x48)
    print()
    print('entry %d: res_id=%d off=0x%X len=%d' % (i, res_id, off, length))
    print('   bundleId=%d (期望 %d) %s' % (bundle, BUNDLE_ID, 'OK' if bundle == BUNDLE_ID else '★需修'))
    print('   +0x18..0x30=%s %s' % (tail, 'OK' if not any(tail) else '★需清零'))
    print('   +0x40=%d +0x48=%d' % (f40, f48))

    if bundle != BUNDLE_ID:
        CHANGES.append((b + 0x08, BUNDLE_ID, 'bundleId'))
    for k in (3, 4, 5, 6):
        v, = struct.unpack_from('<Q', raw, b + 8 * k)
        if v:
            CHANGES.append((b + 8 * k, 0, 'tail+0x%02X' % (8 * k)))
    # +0x40：entry0 与 entry1 都应为 F40
    if f40 != F40:
        CHANGES.append((b + 0x40, F40, '+0x40'))
    # +0x48：entry0 = 16；entry1 = 4294967312（照抄 10-5 可用版）
    want48 = F48_ENTRY0 if i == 0 else F48
    if f48 != want48:
        CHANGES.append((b + 0x48, want48, '+0x48'))

print()
print('=== 待修字段 (%d 处) ===' % len(CHANGES))
for off_b, val, name in CHANGES:
    old, = struct.unpack_from('<Q', raw, off_b)
    print('   0x%03X  %-12s %d -> %d' % (off_b, name, old, val))

if not CHANGES:
    print('无需修复')
    sys.exit(0)

if DRY:
    print('（dry-run，未写入）')
    sys.exit(0)

if WRITE:
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    pre = os.path.join(ADDON, 'patch_backup_before_fix')
    os.makedirs(pre, exist_ok=True)
    shutil.copy2(PACK, os.path.join(pre, 'patch_0.%s' % stamp))
    print('已备份 ->', os.path.join(pre, 'patch_0.%s' % stamp))
    for off_b, val, name in CHANGES:
        struct.pack_into('<Q', raw, off_b, val)
    open(PACK, 'wb').write(bytes(raw))
    print('已写入。大小 = %d（应与原值相同）' % os.path.getsize(PACK))
    print()
    print('请重新检查：python check_records.py')
