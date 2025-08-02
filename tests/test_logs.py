import logs
import logging
import pytest

def test_info_level_logs(caplog):
    """
    Test to validate output for logs
    """
    caplog.set_level(logging.DEBUG)

    my_test_logger = logs.Logs(name='test_logs',level=logging.INFO)
    my_test_logger._logger.addHandler(caplog.handler)
    my_test_logger.info("INFO level test message")
    my_test_logger.debug("DEBUG level test message")
    my_test_logger.warning("WARNING level test message")
    my_test_logger.error("ERROR level test message")
    my_test_logger.critical("CRITICAL level test message")

    my_test_logger._logger.removeHandler(caplog.handler)
    my_test_logger.close()

    assert "INFO level test message" in caplog.text
    assert "WARNING level test message" in caplog.text
    assert "ERROR level test message" in caplog.text
    assert "CRITICAL level test message" in caplog.text
    assert "DEBUG level test message" not in caplog.text


