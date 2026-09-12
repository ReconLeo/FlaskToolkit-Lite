# -*- coding: utf-8 -*-
"""插件/前端工具打包命令行工具

用法：
  1. 打包目录为可安装包（自动生成 manifest.json 哈希清单）
     python tools/package.py pack ./demo_tool -o demo_tool.zip --type frontend
     python tools/package.py pack ./demo_plugin -o demo_plugin.zip --type backend

  2. 查看包内容与清单状态
     python tools/package.py show demo_tool.zip

说明：
- manifest.json 记录包内全部成员（除清单自身）的 sha256，供完整性校验。
- 包结构（backend）：plugin.json + 主 .py + 可选 templates/static + manifest.json
- 包结构（frontend）：config.json + 入口 .html + 可选 static/ + manifest.json
"""
import argparse
import hashlib
import json
import os
import sys
import zipfile

MANIFEST_FILE = 'manifest.json'

# 允许直接运行（python tools/package.py ...）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cmd_pack(args):
    src = os.path.abspath(args.src_dir)
    if not os.path.isdir(src):
        print(f"错误：源目录不存在: {src}", file=sys.stderr)
        sys.exit(1)

    # 按类型校验必备清单文件
    meta_file = 'plugin.json' if args.type == 'backend' else 'config.json'
    if not os.path.exists(os.path.join(src, meta_file)):
        print(f"错误：{args.type} 包缺少清单文件 {meta_file}（应在源目录根下）", file=sys.stderr)
        sys.exit(1)

    # 收集全部文件（相对路径）
    file_list = []
    for root, dirs, files in os.walk(src):
        dirs.sort()
        for fn in sorted(files):
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, src).replace('\\', '/')
            file_list.append((rel, full))
    if not file_list:
        print("错误：源目录为空", file=sys.stderr)
        sys.exit(1)

    # 计算哈希 → manifest
    files_map = {rel: sha256_hex(open(full, 'rb').read()) for rel, full in file_list}
    manifest = {
        'schema_version': '1.0',
        'package_type': args.type,
        'files': files_map,
    }

    # 写 zip（manifest.json 在前）
    out = os.path.abspath(args.output)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MANIFEST_FILE, json.dumps(manifest, ensure_ascii=False, indent=2))
        for rel, full in file_list:
            zf.write(full, rel)

    print(f"已打包: {out}  [{args.type}]")
    print(f"  文件数: {len(file_list)}  清单: {MANIFEST_FILE}")


def cmd_show(args):
    try:
        zf = zipfile.ZipFile(args.package, 'r')
    except zipfile.BadZipFile:
        print("错误：无效的 zip 文件", file=sys.stderr)
        sys.exit(1)
    with zf:
        names = [n.replace('\\', '/') for n in zf.namelist()]
        print(f"包: {args.package}  成员 {len([n for n in names if not n.endswith('/')])} 个")
        print("成员清单:")
        for n in names:
            if not n.endswith('/'):
                print(f"  {n}")
        # 读取 manifest.json（若存在）
        try:
            m = json.loads(zf.read(MANIFEST_FILE))
            print(f"\n清单: schema={m.get('schema_version')} type={m.get('package_type')} "
                  f"files={len(m.get('files', {}))}")
        except KeyError:
            print(f"\n⚠ 缺少 {MANIFEST_FILE}（该包未含哈希清单）")
        except Exception as e:
            print(f"\n⚠ 读取 {MANIFEST_FILE} 失败: {e}")


def main():
    ap = argparse.ArgumentParser(description='FlaskToolkit 插件/前端工具打包工具')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('pack', help='打包目录为可安装包（生成 manifest.json）')
    p.add_argument('src_dir', help='源目录（backend: 含 plugin.json；frontend: 含 config.json）')
    p.add_argument('-o', '--output', required=True, help='输出 .zip 路径')
    p.add_argument('--type', choices=['backend', 'frontend'], default='frontend',
                   help='包类型（默认 frontend）')
    p.set_defaults(func=cmd_pack)

    s = sub.add_parser('show', help='查看包内容与清单状态')
    s.add_argument('package', help='包路径 .zip')
    s.set_defaults(func=cmd_show)

    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
