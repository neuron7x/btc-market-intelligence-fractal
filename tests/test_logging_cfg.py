import importlib
import json
import logging

import btcmi.logging_cfg as logging_cfg


def test_json_log_format(capsys):
    importlib.reload(logging_cfg)
    logging_cfg.configure_logging()
    logger = logging.getLogger("test")
    run_id = logging_cfg.new_run_id()
    logger.info("hello", extra={"run_id": run_id, "mode": "test"})
    captured = capsys.readouterr()
    line = captured.err.strip()
    rec = json.loads(line)
    assert {"ts", "level", "msg", "run_id", "mode", "scenario"} <= set(rec.keys())
    assert rec["level"] == "info"
    assert rec["msg"] == "hello"
    assert rec["run_id"] == run_id
    assert rec["mode"] == "test"
    assert rec["scenario"] is None
    assert isinstance(rec["ts"], int)


def test_configure_logging_runs_once():
    importlib.reload(logging_cfg)
    logging_cfg.configure_logging()
    root = logging.getLogger()
    handlers_first = root.handlers
    logging_cfg.configure_logging()
    assert root.handlers is handlers_first
