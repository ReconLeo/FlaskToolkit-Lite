# FlaskToolkit-Lite

<p align="center">
  <img src="https://github.com/ReconLeo/FlaskToolkit-Lite/actions/workflows/ci.yml/badge.svg" alt="CI">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/version-4.2.2-blue" alt="Version">
</p>

A Flask-based **plugin framework** for running scattered Python plugins and pure-frontend tools in one unified runtime.

## Features

- **Plugin packages (.zip)** — backend plugins ship with templates/static assets; frontend HTML tools are first-class citizens. Install / update / uninstall / enable / disable at runtime.
- **Multi-template large plugins** — page routes (`page=True`), helper modules, per-plugin static assets.
- **Permission model** — three levels (public / user / admin); auth is an optional plugin (guest mode when absent).
- **Hot reload** — file watching; changes take effect without restart.
- **Admin panel** — dashboard / plugin management / system info & reset.
- **Unified file transfer** — global upload ceiling (per-route overridable), Chinese-safe downloads (RFC 5987), download stats & Range.
- **Factory Reset / backup / restore / startup self-check**, plus a 309-assertion regression suite and GitHub Actions CI.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Local-only by default; set `FLASKTOOLKIT_HOST=0.0.0.0` for LAN use.

Install the `auth` plugin to enable login (default `admin / admin123`, editable in `plugins/configs/auth.json`).

Install official examples:

```bash
pip install -r requirements.txt   # install_all.py needs requests
python examples/install_all.py
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASKTOOLKIT_HOST` | `127.0.0.1` | Bind address; use `0.0.0.0` for LAN |
| `FLASKTOOLKIT_PORT` | auto-detect | Explicit port; falls back if occupied |
| `FLASKTOOLKIT_DEBUG` | off | Debug mode; disable in production |

## Official Examples

[`examples/`](examples/README.md) ships one-click installable examples that double as plugin-development templates:

| Example | Type | Highlights |
|---------|------|-----------|
| `hello_plugin` | Backend | Lifecycle hooks, permissions, config, custom page |
| `scheduler_demo` | Backend | APScheduler jobs (interval/cron) |
| `async_file_demo` | Backend | Upload limits, async tasks, status polling, result download |
| `dependent_demo` | Backend | Dependency declaration, cross-plugin calls |
| `multitool_demo` | Backend | Multi-template: page routes, helper .py, static assets |
| `dashboard_demo` | Frontend | Admin permission, backend API calls, ECharts, static assets |

## Documentation

- [Flask Plugin Framework Development Guide](documents/Flask插件框架开发规范-v4.0.md) — plugin development, permission model, frontend-tool spec, plugin-package format, ops tools.
- [Official examples guide](examples/README.md)

## Tests

17 scripts / 309 assertions, isolated-directory mode (no project pollution); CI runs them on Python 3.10 / 3.11 / 3.12.

<details>
<summary>Expand: 17 test scripts</summary>

```bash
cd FlaskToolkit-Lite
python tests/test_permission.py            # permission system 20
python tests/test_stage2.py                # security hardening regression 19
python tests/test_zip_slip.py              # plugin-package zip slip 19
python tests/test_pack_meta.py             # plugin-package meta consistency 17
python tests/test_reload_race.py           # hot-reload race 1
python tests/test_meta_e2e.py              # plugin-package meta end-to-end 10
python tests/test_frontend_zip_slip.py     # frontend-tool zip slip 21
python tests/test_frontend_chain.py        # frontend-tool chain end-to-end 23
python tests/test_admin_api.py             # admin API 21
python tests/test_factory_reset.py         # Factory Reset scope 37
python tests/test_error_pages.py           # error-code pages 12
python tests/test_plugin_cleanup.py        # uninstall installed_files manifest 23
python tests/test_frontend_permission.py   # frontend-tool access control 25
python tests/test_tools_ops.py             # ops tools backup/reset/config 19
python tests/test_page_router.py           # large-plugin multi-template page routing 21
python tests/test_framework_fixes.py       # public_page exemption + CSRF single-injection 9
python tests/test_file_transfer.py         # upload limits / Chinese-name downloads / Range 12
# total: 17 scripts / 309 assertions
```

</details>

## Security

- **Installing a plugin means trusting its author** — plugins run arbitrary code; only install from trusted sources.
- Not hardened for adversarial public networks; designed for your own machine or a trusted LAN.

## License

MIT License · AI-assisted development was used.
