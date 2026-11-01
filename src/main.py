import os
import sys
import json
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from src.logger import get_logger
from src.notifier import Notifier

log = get_logger("Main")

def get_project_root() -> str:
    """获取项目根目录，彻底解决相对路径报错的问题"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Shenk 智能日志巡检与并发告警工具 v3")
    parser.add_argument("--log_file", type=str, default="app.log", help="要巡检的日志文件路径，默认 app.log")
    parser.add_argument("--rules", type=str, default="ERROR,timeout,OOM", help="巡检规则，逗号分隔")
    parser.add_argument("--channels", type=str, default="钉钉,飞书,企微", help="告警渠道，逗号分隔")
    return parser.parse_args()

def load_config() -> dict:
    """加载配置文件"""
    config_path = os.path.join(get_project_root(), "config", "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log.error(f"配置文件不存在: {config_path}")
        sys.exit(1)

def scan_log(file_path: str, rules: list[str]) -> list[str]:
    """扫描日志文件，返回命中的异常列表"""
    alerts = []
    full_path = os.path.join(get_project_root(), file_path)
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                for rule in rules:
                    if rule.lower() in line.lower():
                        alerts.append(line)
                        break  # 核心修复：一旦命中一个规则，记录后直接退出内层循环，防止重复
    except FileNotFoundError:
        log.error(f"找不到日志文件: {full_path}，请检查路径！")
        return []
    return alerts

def main() -> None:
    args = parse_args()
    config = load_config()

    # 优先级：命令行参数 > 配置文件
    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    log_file = args.log_file

    log.info(f"--- 开始巡检日志: {log_file} ---")
    alerts = scan_log(log_file, rules)

    if not alerts:
        log.info("✅ 日志正常，未发现异常。")
        return

    log.warning(f"⚠️ 共发现 {len(alerts)} 条异常，准备并发发送告警...")
    
    start_time = time.time()
    
    # 并发发送告警
    with ThreadPoolExecutor(max_workers=len(channels)) as pool:
        for channel in channels:
            notifier = Notifier(channel)
            # 因为实现了 __call__，可以直接像函数一样传参给 submit
            pool.submit(notifier, f"发现 {len(alerts)} 条异常，最后一条为: {alerts[-1]}")

    log.info(f"--- 告警发送完毕，总耗时: {time.time() - start_time:.2f} 秒 ---")

if __name__ == "__main__":
    main()