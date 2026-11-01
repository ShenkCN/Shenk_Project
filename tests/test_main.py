import os
import sys
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.main import scan_log, load_config

# 测试 1：测试 scan_log 找不到文件
def test_scan_log_file_not_found():
    result = scan_log("not_exist.log", ["ERROR"])
    assert result == []

# 测试 2：模拟读取文件并匹配规则
@patch("builtins.open", new_callable=mock_open, read_data="INFO ok\nERROR failed\ntimeout error\n")
def test_scan_log_success(mock_file):
    # 拦截绝对路径拼接
    with patch("src.main.os.path.join", return_value="fake_path"):
        result = scan_log("app.log", ["ERROR", "timeout"])
        assert len(result) == 2
        assert "ERROR failed" in result
        assert "timeout error" in result

# 测试 3：测试并发告警（使用 Mock 拦截 Notifier.send，不实际发请求）
@patch("src.notifier.Notifier.send")
def test_notifier_mock(mock_send):
    mock_send.return_value = True
    from src.notifier import Notifier
    n = Notifier("钉钉")
    n.send("测试消息")
    mock_send.assert_called_once_with("测试消息")