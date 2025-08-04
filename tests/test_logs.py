import collections

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




