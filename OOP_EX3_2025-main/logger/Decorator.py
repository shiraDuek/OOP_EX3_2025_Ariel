import functools
from logger.logging_config import logger

def log_action(action, log_args=[]):
    """
    A decorator to log the action performed by a function.

    Args:
        action (str): The action description to log.
        log_args (list): List of argument names to include in the log message.

    Returns:
        function: The wrapped function with logging.
    """
    def decorator_log_action(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            action_with_args = action
            try:
                # Capture the actual argument values
                arg_values = {arg: kwargs.get(arg, 'N/A') for arg in log_args}
                for i, arg in enumerate(func.__code__.co_varnames):
                    if arg in log_args and i < len(args):
                        arg_values[arg] = args[i]

                # Replace placeholders in the action string with actual argument values
                action_with_args = action.format(**arg_values)
                result = func(*args, **kwargs)
                params = ', '.join(f"{arg}={arg_values.get(arg, 'N/A')}" for arg in log_args)
                result_type = type(result)
                from User import User
                log_cases = {
                    int: lambda res: logger.info(f"{action_with_args} successfully") if res == 1 else logger.error(f"{action_with_args} failed"),
                    bool: lambda res: logger.info(f"{action_with_args} successfully") if res else logger.error(f"{action_with_args} failed"),
                    list: lambda res: logger.info(f"{action_with_args} successfully") if len(res) > 0 else logger.error(f"{action_with_args} with {params} failed"),
                    User: lambda res: logger.info(f"{action_with_args} successfully") if res else logger.error(f"{action_with_args} with {params} failed")
                }
                log_cases.get(result_type, lambda res: logger.error(f"{action_with_args} failed"))(result)
                return result
            except KeyError as e:
                logger.error(f"Failed to format action string: {e}")
                raise
            except Exception as e:
                logger.error(f"{action_with_args} failed: {e}")
                raise
        return wrapper
    return decorator_log_action