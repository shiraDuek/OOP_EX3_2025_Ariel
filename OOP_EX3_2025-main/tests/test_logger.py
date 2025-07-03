import unittest
from unittest.mock import patch, MagicMock
from logger.Decorator import log_action
from logger.logging_config import logger

class TestLogger(unittest.TestCase):

    @patch('logger.logging_config.logger.info')
    @patch('logger.logging_config.logger.error')
    def test_log_action_success(self, mock_error, mock_info):
        @log_action("action performed")
        def sample_function(success=True):
            return success

        # Test successful action
        sample_function(success=True)
        mock_info.assert_called_with("action performed successfully")
        mock_error.assert_not_called()

    @patch('logger.logging_config.logger.info')
    @patch('logger.logging_config.logger.error')
    def test_log_action_failure(self, mock_error, mock_info):
        @log_action("action performed")
        def sample_function(success=True):
            return success

        # Test failed action
        sample_function(success=False)
        mock_error.assert_called_with("action performed failed")
        mock_info.assert_not_called()

    @patch('logger.logging_config.logger.info')
    @patch('logger.logging_config.logger.error')
    def test_log_action_with_args(self, mock_error, mock_info):
        @log_action("action with args {arg1} and {arg2}", log_args=['arg1', 'arg2'])
        def sample_function(arg1, arg2, success=True):
            return success

        # Test successful action with arguments
        sample_function("value1", "value2", success=True)
        mock_info.assert_called_with("action with args value1 and value2 successfully")
        mock_error.assert_not_called()

    @patch('logger.logging_config.logger.info')
    @patch('logger.logging_config.logger.error')
    def test_log_action_with_args_failure(self, mock_error, mock_info):
        @log_action("action with args {arg1} and {arg2}", log_args=['arg1', 'arg2'])
        def sample_function(arg1, arg2, success=True):
            return success

        # Test failed action with arguments
        sample_function("value1", "value2", success=False)
        mock_error.assert_called_with("action with args value1 and value2 failed")
        mock_info.assert_not_called()

    @patch('logger.logging_config.logger.info')
    @patch('logger.logging_config.logger.error')
    def test_log_action_exception(self, mock_error, mock_info):
        @log_action("action with exception")
        def sample_function():
            raise ValueError("An error occurred")

        # Test action that raises an exception
        with self.assertRaises(ValueError):
            sample_function()
        mock_error.assert_called_with("action with exception failed: An error occurred")
        mock_info.assert_not_called()

if __name__ == '__main__':
    unittest.main()