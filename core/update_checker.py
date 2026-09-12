# -*- coding: utf-8 -*-
"""
版本检查（Lite 精简版）：只读检查新版本，控制台提示；不支持更新源修改 / 框架下载

- 数据源：固定指向本仓库 lite 分支的 changelog.json（public 仓库可匿名访问），URL 不支持修改。
- 异步惰性：由 app 启动后的后台线程触发，不阻塞启动；网络 3s 超时，失败静默（仅日志）。
- 精简边界（相对主项目）：不做缓存 TTL、不做签名校验、不自动下载更新包、不可配置更新源。
"""
import json
import logging

import requests

import global_var

logger = logging.getLogger('flask.app')

# 固定更新数据源（Lite 仓库 public 后匿名可访问；始终指向 lite 分支 = 最新已发布 changelog）
CHANGELOG_URL = 'https://raw.githubusercontent.com/ReconLeo/FlaskToolkit-Lite/lite/changelog.json'
# changelog 数据必填字段（与 tools/release.py 生成一致）
REQUIRED_FIELDS = ('latest_version', 'published_at', 'changes')


def parse_version(version):
    """版本号转可比较 tuple：'4.2.2' -> (4, 2, 2)；非法段按 0 处理"""
    parts = []
    for seg in str(version or '').strip().lstrip('vV').split('.'):
        try:
            parts.append(int(seg))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def is_newer(latest, current):
    """latest > current 返回 True（tuple 逐位比较，无第三方依赖）"""
    return parse_version(latest) > parse_version(current)


def check_for_update(timeout=3):
    """拉取远端 changelog 并返回 dict；失败返回 None（静默，不影响启动）"""
    try:
        r = requests.get(CHANGELOG_URL, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, dict):
            return None
        if not all(k in data for k in REQUIRED_FIELDS):
            return None
        return data
    except Exception as e:
        logger.debug(f"检查更新失败（静默）: {e}", extra={'plugin': 'system'})
        return None


def background_check():
    """后台线程入口：检查更新并在控制台提示（纯附加，任何异常都不影响服务）"""
    try:
        data = check_for_update()
        if data is None:
            return
        latest = data.get('latest_version', '')
        if not latest:
            return
        if is_newer(latest, global_var.FRAMEWORK_VERSION):
            print(f"[更新] 发现新版本 v{latest}（当前 v{global_var.FRAMEWORK_VERSION}，"
                  f"变更 {len(data.get('changes') or [])} 条）。下载与发布说明："
                  f"{global_var.PROJECT_GITHUB}/releases", flush=True)
        else:
            print(f"[更新] 已是最新版本 v{global_var.FRAMEWORK_VERSION}", flush=True)
    except Exception:
        pass  # 检查更新为纯附加，任何异常都不应影响服务
