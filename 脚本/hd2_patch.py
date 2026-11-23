#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hd2_patch.py -- Helldivers 2 .patch_N (Stingray bundle patch) 读写工具

格式（实测归纳）:
    0x00  u32 magic = 0xF0000011
    0x04  u32 = 1
    0x08  u32 = entry 数量 N
    0x20  u32 = 文件总字节数
    0x50  u64 = bundle id (固定 0xe217d12cfa8d4ea1)
    每个 entry i (0-based):
        0x68 + 80*i   u64 = entry 资源 id = murmur_hash_64A(资源路径, seed=0)
        0x70 + 80*i   u64 = bundle id (固定)
        0x78 + 80*i   u64 = entry 记录偏移 (= 数据偏移 - 8)
        0xA0 + 80*i   u64 = entry 数据长度 + 8
    数据区: entry i 的记录 = (u32 len, u32 type) 位于记录偏移处, 数据紧随其后
    type: 2 = Lua 源码 (明文)
    头部总长 = 0xC8 + 80*(N-1)
"""
from __future__ import annotations

import os
import struct

MAGIC = 0xF0000011
BUNDLE_ID = 0xE217D12CFA8D4EA1
M64 = (1 << 64) - 1


def murmur64a(data, seed=0):
    m = 0xC6A4A7935BD1E995
    r = 47
    length = len(data)
    h = (seed ^ ((length * m) & M64)) & M64
    n = length // 8
    for i in range(n):
        k = int.from_bytes(data[i * 8:i * 8 + 8], "little")
        k = (k * m) & M64
        k ^= k >> r
        k = (k * m) & M64
        h ^= k
        h = (h * m) & M64
    tail = data[n * 8:]
    if len(tail) >= 7:
        h ^= tail[6] << 48
    if len(tail) >= 6:
        h ^= tail[5] << 40
    if len(tail) >= 5:
        h ^= tail[4] << 32
    if len(tail) >= 4:
        h ^= tail[3] << 24
    if len(tail) >= 3:
        h ^= tail[2] << 16
    if len(tail) >= 2:
        h ^= tail[1] << 8
    if len(tail) >= 1:
        h ^= tail[0]
        h = (h * m) & M64
    h ^= h >> r
    h = (h * m) & M64
    h ^= h >> r
    return h


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def u64(b, o):
    return struct.unpack_from("<Q", b, o)[0]


def p32(v):
    return struct.pack("<I", v)


def p64(v):
    return struct.pack("<Q", v)


def align8(n):
    a = (n + 7) // 8 * 8
    if a <= n:
        a += 8
    return a


class Entry:
    __slots__ = ("index", "record_offset", "data_offset", "length", "type", "res_id", "data", "path_comment")

    def __init__(self, index, record_offset, length, type_, res_id, data):
        self.index = index
        self.record_offset = record_offset
        self.data_offset = record_offset + 8
        self.length = length
        self.type = type_
        self.res_id = res_id
        self.data = data
        self.path_comment = None

    def __repr__(self):
        return ("Entry#%d off=0x%x len=%d type=%d id=0x%016x path=%r" %
                (self.index, self.data_offset, self.length, self.type, self.res_id, self.path_comment))


class PatchFile:
    def __init__(self, data, source=""):
        self.raw = data
        self.source = source
        if len(data) < 0xC8 or u32(data, 0) != MAGIC:
            raise ValueError("magic/长度不符: %s" % source)
        self.count = u32(data, 8)
        self.size = u32(data, 0x20)
        if self.size != len(data):
            raise ValueError("0x20 大小 %d != 实际 %d (%s)" % (self.size, len(data), source))
        self.head_len = 0xC8 + 80 * (self.count - 1)
        self.entries = []
        for i in range(self.count):
            res_id = u64(data, 0x68 + 80 * i)
            record_offset = u64(data, 0x78 + 80 * i)
            len_plus8 = u64(data, 0xA0 + 80 * i)
            length = u32(data, record_offset)
            type_ = u32(data, record_offset + 4)
            if len_plus8 != length + 8:
                raise ValueError("entry%d 长度字段不一致: %d vs %d+8 (%s)" % (i, len_plus8, length, source))
            payload = data[record_offset + 8: record_offset + 8 + length]
            if len(payload) != length:
                raise ValueError("entry%d 数据越界 (%s)" % (i, source))
            e = Entry(i, record_offset, length, type_, res_id, payload)
            m = payload[:400].find(b"-- HD2-Addon: ")
            if m >= 0:
                nl = payload.find(b"\n", m)
                line = payload[m:(nl if nl >= 0 else m + 200)]
                e.path_comment = line[len(b"-- HD2-Addon: "):].decode("utf-8", "replace").strip()
            self.entries.append(e)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as fh:
            return cls(fh.read(), path)

    def text(self, index=-1):
        return self.entries[index].data.decode("utf-8", "replace")

    def rebuild_probe(self):
        out = bytearray(self.raw[: self.head_len])
        for e in self.entries:
            rec = len(out)
            out += p32(e.length) + p32(e.type) + bytearray(e.data)
            out += b"\x00" * (align8(e.length) - e.length)
            out[0x78 + 80 * e.index:0x80 + 80 * e.index] = p64(rec)
            out[0xA0 + 80 * e.index:0xA8 + 80 * e.index] = p64(e.length + 8)
        out[0x20:0x24] = p32(len(out))
        return bytes(out)


def rewrite_last_entry(original, payload):
    pf = PatchFile(original)
    index = pf.count - 1
    e = pf.entries[index]
    blob = bytearray(original[: e.data_offset]) + bytearray(payload)
    blob += b"\x00" * (align8(len(payload)) - len(payload))
    blob[0x20:0x24] = p32(len(blob))
    blob[e.record_offset:e.record_offset + 4] = p32(len(payload))
    blob[0xA0 + 80 * index:0xA8 + 80 * index] = p64(len(payload) + 8)
    return bytes(blob)


def make_patch(source_patch, payload, dest):
    with open(source_patch, "rb") as fh:
        original = fh.read()
    out = rewrite_last_entry(original, payload)
    d = os.path.dirname(dest)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(out)
    pf = PatchFile(out, dest)
    return {"dest": dest, "size": len(out),
            "entries": [(e.type, e.length, e.path_comment) for e in pf.entries]}


def backup(path, backup_root, mods_root):
    rel = os.path.relpath(path, mods_root)
    dst = os.path.join(backup_root, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        with open(path, "rb") as s, open(dst, "wb") as d:
            d.write(s.read())
    return dst


def self_test(mods_root=None):
    root = mods_root or os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
    files = []
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.endswith(".patch_0") or n.endswith(".patch_1"):
                files.append(os.path.join(dirpath, n))
    bad = 0
    lua_entries = 0
    id_ok = id_bad = 0
    counts = {}
    for p in sorted(files):
        try:
            pf = PatchFile.load(p)
        except Exception as exc:
            print("PARSE FAIL", p, exc)
            bad += 1
            continue
        counts[pf.count] = counts.get(pf.count, 0) + 1
        for e in pf.entries:
            if e.type == 2:
                lua_entries += 1
                if e.path_comment:
                    if murmur64a(e.path_comment.encode()) == e.res_id:
                        id_ok += 1
                    else:
                        id_bad += 1
                        print("ID MISMATCH", p, e.path_comment)
        try:
            PatchFile(pf.rebuild_probe(), p + " (rebuilt)")
        except Exception as exc:
            print("REBUILD FAIL", p, exc)
            bad += 1
    print("文件 %d 个, 异常 %d; Lua entry %d 个; 资源 id 校验 通过 %d / 失败 %d; entry 数分布 %s" %
          (len(files), bad, lua_entries, id_ok, id_bad, counts))


if __name__ == "__main__":
    self_test()
