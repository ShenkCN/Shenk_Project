# 🚀 Shenk OpsTool v3 - 智能日志巡检与并发告警系统

## 📖 项目简介
本项目是一个基于 Python 开发的高并发、可扩展的自动化运维工具。针对企业级 IT 运维场景中日志散乱、告警延迟的痛点，本工具实现了**日志增量读取、规则动态匹配、告警降噪与多线程并发推送**。旨在将“非标”的现场排障动作，转化为标准化的自动化流程。

## ✨ 核心特性
- **模块化解耦**：采用 `src/config/tests` 的现代工程目录结构，业务逻辑与测试代码完全隔离。
- **高并发限流**：基于 `concurrent.futures.ThreadPoolExecutor` 实现告警消息的并发分发，将耗时从线性叠加压缩至 0.5 秒级。
- **日志按天切割**：集成 `TimedRotatingFileHandler`，自动实现日志文件的按天切分与 7 天备份，防止磁盘撑爆。
- **CLI 参数驱动**：基于 `argparse` 实现高度可定制化，支持动态传入日志路径、匹配规则与告警渠道，拒绝硬编码。
- **TDD 测试驱动**：基于 `pytest` 与 `unittest.mock` 编写单元测试，彻底隔离网络请求，实现 100% 自动化验证。

## 🛠️ 技术栈
- **语言**: Python 3.11
- **核心库**: `argparse`, `logging`, `concurrent.futures`
- **测试框架**: `pytest`, `pytest-cov`, `unittest.mock`

## 📂 目录结构
```text
Shenk_Project/
├── config/              # 配置文件目录
│   └── config.json      # 规则与告警渠道配置
├── logs/                # 运行日志存放目录（自动切割）
├── src/                 # 核心源码
│   ├── __init__.py
│   ├── logger.py        # 日志封装组件
│   ├── notifier.py      # 告警发送组件
│   └── main.py          # CLI入口与并发调度核心
├── tests/               # 单元测试
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt     # 依赖清单
└── README.md