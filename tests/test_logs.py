import collections

import logs
import logging
import os
import pytest
from unittest.mock import patch

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
def test_debug_msg(caplog):
    caplog.set_level(logging.DEBUG)
    debug_logger = logs.Logs(name="Debug_test",level=logging.DEBUG)
    debug_logger._logger.addHandler(caplog.handler)
    debug_logger.debug('Debug test message')
    debug_logger._logger.removeHandler(caplog.handler)
    debug_logger.close()
    assert "Debug test message" in caplog.text
def test_warning_msg(caplog):
    """
    Test for WARNING,ERROR,CRITICAL level logs
    """
    caplog.set_level(logging.WARNING)
    warning_level_test = logs.Logs(name='Warning level test',level=logging.WARNING)
    warning_level_test._logger.addHandler(caplog.handler)
    warning_level_test.info('INFO msg should be omitted')
    warning_level_test.debug('DEBUG msg should be omitted')
    warning_level_test.warning('Warning test functional')
    warning_level_test.critical('CRITICAL test functional')
    warning_level_test.error('ERROR test functional')
    warning_level_test._logger.removeHandler(caplog.handler)
    warning_level_test.close()
    assert 'INFO msg should be omitted' not in caplog.text
    assert 'DEBUG msg should be omitted' not in caplog.text
    assert 'Warning test functional' in caplog.text
    assert 'CRITICAL test functional' in caplog.text
    assert 'ERROR test functional' in caplog.text

def test_error_msg(caplog):
    caplog.set_level(logging.ERROR)
    error_level_test = logs.Logs(name='Error level test',level=logging.ERROR)
    error_level_test._logger.addHandler(caplog.handler)
    error_level_test.info('INFO msg should be omitted')
    error_level_test.debug('DEBUG msg should be omitted')
    error_level_test.warning('WARNING msg should be omitted')
    error_level_test.error('ERROR test functional')
    error_level_test.critical('CRITICAL test functional')
    error_level_test._logger.removeHandler(caplog.handler)
    error_level_test.close()
    assert 'INFO msg should be omitted' not in caplog.text
    assert 'DEBUG msg should be omitted' not in caplog.text
    assert 'WARNING msg should be omitted' not in caplog.text
    assert 'ERROR test functional' in caplog.text
    assert 'CRITICAL test functional' in caplog.text
def test_critical_msg(caplog):
    caplog.set_level(logging.CRITICAL)
    critical_level_test = logs.Logs(name='CRITICAL level test', level= logging.CRITICAL)
    critical_level_test._logger.addHandler(caplog.handler)
    critical_level_test.info('INFO msg should be omitted')
    critical_level_test.debug('DEBUG msg should be omitted')
    critical_level_test.warning('WARNING msg should be omitted')
    critical_level_test.error('ERROR msg should be omitted')
    critical_level_test.critical('CRITICAL test functional')
    critical_level_test._logger.removeHandler(caplog.handler)
    critical_level_test.close()
    assert 'INFO msg should be omitted' not in caplog.text
    assert 'DEBUG msg should be omitted' not in caplog.text
    assert 'WARNING msg should be omitted' not in caplog.text
    assert 'ERROR msg should be omitted' not in caplog.text
    assert 'CRITICAL test functional' in caplog.text
def test_exception_value():
    """
    Test for invalid log levels
    """
    with pytest.raises(ValueError) as exc_info:
        logs.Logs(name='test invalid level', level=97)
        assert exc_info.type(ValueError)
        assert 'Invalid level' in str(exc_info.value)
def test_exception_type():
    with pytest.raises(TypeError) as exc_info:
        logs.Logs(name='test invalid type',level ="ERROR")
        assert exc_info.type(TypeError)
        assert 'Incorrect Type for level value' in str(exc_info.value)

def test_dir_path(tmp_path):
    test_file_path = tmp_path/'test_path.log'
    log_path = logs.Logs(name='Test Path',level=logging.INFO,log_file=f'{test_file_path}')

    log_path.info('Stored info msg')
    log_path.error('Stored error msg')
    log_path.debug('Stored DEBUG msg')
    log_path.close()

    with open(test_file_path,'r') as f:
        log_content = f.read()

    assert "Stored info msg" in log_content
    assert "Stored error msg" in log_content
    assert "Stored DEBUG msg" not in log_content
    assert os.path.exists(test_file_path)

def test_default_msg(caplog):

    with patch("os.makedirs",side_effect=OSError("Permission denied")):
         caplog.set_level(logging.DEBUG)
         test_logger = logs.Logs(name="Test default path",level=logging.DEBUG,log_file="/non_writable_path/log.log"

        )
    test_logger._logger.addHandler(caplog.handler)
    test_logger.info("Test console fallback")
    test_logger._logger.removeHandler(caplog.handler)
    test_logger.close()
    assert "Test console fallback" in caplog.text

def test_default_err_msg(caplog):
    with patch("os.makedirs",side_effect=OSError("Permission denied")):
        caplog.set_level(logging.DEBUG)
        test_logger=logs.Logs(
            name="Test default error message",
            level=logging.DEBUG,
            log_file="/non_writable_path/log.log"
        )
    test_logger._logger.addHandler(caplog.handler)
    test_logger.error("Failed to set log path to")
    test_logger._logger.removeHandler(caplog.handler)
    test_logger.close()

    assert "Failed to set log path to" in caplog.text

