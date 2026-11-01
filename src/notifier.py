import time
from src.logger import get_logger

log = get_logger("Notifier")

class Notifier:
    """通知器类"""
    def __init__(self, channel: str):
        self.channel = channel

    def __call__(self, message: str) -> bool:
        """实现 __call__ 魔术方法，让实例可以直接被调用"""
        return self.send(message)

    def send(self, message: str) -> bool:
        try:
            # 真实场景这里会是 requests.post()
            time.sleep(0.5)  # 模拟网络延迟
            log.info(f"🚨 【{self.channel}】告警已发送: {message}")
            return True
        except Exception as e:
            log.error(f"❌ 【{self.channel}】告警发送失败: {e}")
            return False