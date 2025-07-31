import logs
import logging
import pytest

def test_info_level_logs(capsys):
    """
    Test to validate output for logs
    """
    my_test_logger = logs.Logs(name="test_name",level=logging.INFO)
    my_test_logger.info("This test is for INFO level logging")
    my_test_logger.warning("This test is for WARNING level logging")
    my_test_logger.critical("This test is for CRITICAL level logging")
    my_test_logger.error("This test is for ERROR level logging")
    my_test_logger.debug("This test is for DEBUG level logging:should not show")
    my_test_logger.close()
    captured_output = capsys.readouterr()
    assert "This test is for INFO level logging" in captured_output.out
    assert "This test is for CRITICAL level logging" in captured_output.err
