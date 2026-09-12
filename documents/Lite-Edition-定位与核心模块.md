# Lite Edition —— 定位与核心模块清单

> 状态：草案（2026-09-12）
> 基线：`v4.2.2`（commit `4d7d602`，2026-09-02），分支 `lite`，已补 tag `v4.2.2`

## 一、定位

Lite Edition 是从 FlaskToolkit 演进线上拆分出的**极简、轻量、只留核心**的插件化框架分支。它在 `v4.2.2`（核心基建完备、外围能力尚未引入）处与主线分叉，面向**个人开发者与小型自托管**场景，把"插件化全栈工具集"这一核心价值做到最小可用、易于阅读与二次开发。

### 是什么 / 不是什么

| | 说明 |
|---|---|
| **是** | 插件加载与热重载、统一鉴权与权限、管理后台、插件包机制、前端工具混合展示、运维 CLI —— 最小可用闭环 |
| **不是** | main 后期叠加的深层安全体系、HTTPS/反代、i18n、配额、统计画像、Root 域、插件更新源、事件总线、主题/深色等外围能力 |

### 与 main（Community）的关系

- **同源分叉**：Lite 与 main 共享 v4.2.2 之前的演进历史，核心 API 与插件格式一致，示例插件可复用。
- **各自演进**：main 是全功能 Community（持续迭代、架构规模有意识控制）；Lite 是"只留核心"的精简维护线，二者互不干扰。
- **单向同步**：Lite 按需 cherry-pick main 的核心 bug 修复；main 后期外围能力**不回流** Lite。

## 二、设计原则

1. **核心最小化**：保留"无它框架即不存在"的模块；一切外围能力默认排除，确有需要再按需引入。
2. **零依赖优先**：保持标准库优先，避免把可选依赖（HTTPS 证书、mDNS、国际化等）带进默认运行。
3. **可读优先**：模块总数控制在 ~20 个以内、总量 ~3k 行，任何新开发者半天可读完 core/。
4. **插件兼容**：插件包格式、权限装饰器、路由约定与 v4.2.2 保持稳定，作为 Lite 的对外契约。

## 三、核心模块清单（基于 v4.2.2 实际结构）

### 3.1 一级·框架核心（必须保留）

| 模块 | 行数 | 职责 |
|------|------|------|
| `core/plugin_loader.py` | 323 | 插件加载、生命周期、静态资源/路由注册 |
| `core/plugin_pack.py` | 402 | 插件包机制：.zip 解析、字段校验、安装、卸载清单 |
| `core/plugin_cache.py` | 231 | 插件编译缓存 |
| `core/plugin_status.py` | 44 | 插件启停状态管理 |
| `core/watcher.py` | 242 | 文件监听与热重载 |
| `core/permission.py` | 180 | 统一鉴权与权限装饰器（login_required / permission） |
| `core/utils.py` | 101 | 通用工具（端口、路径、加密辅助） |
| `core/logging_setup.py` | 93 | 日志配置与插件日志适配 |
| `core/selfcheck.py` | 121 | 启动完整性自检 |
| `core/factory_reset.py` | 195 | Factory Reset |
| `routes/`（全部 6 个） | ~900 | admin / frontend / interceptor / plugin / public 路由 |
| `app.py`、`global_var.py`、`templates/`、`static/`、`data/frontend_tools.json` | — | 入口、全局常量、页面与静态资源 |

### 3.2 二级·框架特色（建议保留，构成差异化）

| 模块 | 行数 | 职责 |
|------|------|------|
| `core/frontend_tools.py` | 73 | 前端 HTML 工具混合展示（框架特色能力） |
| `core/stats.py` | 56 | 基础页面统计（v4.2.2 轻量版，**非** main 的 v4.14 统计画像） |

### 3.3 已削除（档位2 单机化落地）

| 模块 | 原行数 | 削除原因 |
|------|--------|---------|
| `core/package_sign.py` | 204 | 插件完整性签名。单机可信本机环境无需签名校验；`plugin_pack.py` 本不依赖它，削除不破坏插件加载 |
| `core/audit.py` | 86 | 管理后台审计日志。单机无多用户敏感操作追溯需求，随后台审计页一并移除 |
| `plugins/user_manage.py`、`plugins/user_manage.json` | — | 多用户账号管理。Lite 保留单管理员登录（`auth` 自带 `admin/admin123` 初始化），多用户 CRUD 移除 |
| `templates/admin/logs.html`、`stats.html`、`plugins/user_manage.html` | — | 后台仅保留 dashboard + plugins + system，去 logs/stats/audit 页与 user_manage 模板 |

### 3.4 运维工具（tools/，保留）

`tools/config.py` / `tools/backup.py` / `tools/package.py` / `tools/reset.py` —— 配置、备份、打包、重置四 CLI，构成最小运维闭环。

## 四、明确排除清单（main 后期外围，不引入 Lite）

以下能力在 v4.2.2 **本就不存在**，Lite 天然不含，无需剥离；日后也**不回流**：

- 深层安全：`core/capabilities.py`、`core/plugin_scanner.py`、`core/audit_hook.py`
- HTTPS / 反代（v4.5 / v4.12 Secure）
- i18n 国际化（v4.9）、配额（v4.9）
- 统计画像（v4.14）
- Root 权限域、`plugin_admin.py`、`plugin_updates.py`（v4.15）
- 事件总线、依赖解析（v4.16）
- mDNS / IP 变化检测 / 桌面启动器（v4.11）
- 主题 / 深色模式（v4.19）
- 首次运行向导 / 强制改密 / 邀请码 / 脚手架（v4.10）—— 如需按需移植，见第五章

## 五、演进策略

1. **主线 bug 修复同步**：cherry-pick main 中涉及插件加载 / 鉴权 / 后台 / 运维的修复；涉及 4.3+ 重构流程的提交须逐条审查。
2. **个人体验能力按需移植**：若 Lite 需要 v4.10 的首次运行向导 / 脚手架 / 邀请码等，作为独立能力 cherry-pick 或重新实现（与安全/生态重量低耦合，移植代价可控）。
3. **契约稳定**：插件格式、权限装饰器、路由约定对外冻结，保证示例插件与第三方插件可在 Lite 运行。
4. **回归保障**：维护 Lite 独立的最小回归套件（对齐 v4.2.2 的 tests/），每次改动全量跑通。

## 六、决策记录

| 日期 | 决策 |
|------|------|
| 2026-09-12 | 选定 `v4.2.2`（`4d7d602`）为 Lite 分叉点：核心完备（插件包/权限/后台/运维/CI）、外围最少（深层安全与生态能力均未引入）；补 tag `v4.2.2`、创建分支 `lite` |
| 2026-09-12 | 档位2·单机化削减落地：保留单管理员登录、后台仅 dashboard+plugins+system；删除 package_sign/audit/user_manage，去后台 logs/stats/audit 页；core 模块 15→13 |
| 2026-09-13 | 【已知问题·行尾】分叉带出的核心 `.py`（如 `core/plugin_loader.py`、`core/logging_setup.py`）为 **CRLF** 行尾，与 `.gitattributes` 强制 `*.py eol=lf` 不符（主项目文本文件统一 LF）。为最小化本次 cherry-pick diff，**暂不统一行尾**；后续如需治理，用 `git add --renormalize .` 刷新后再提交（注意会让该批文件 diff 放大） |
