from common.exceptions import TestFailureException


def test_decorator(message, number, iter=1000):
    def decorator(function):
        def wrapper(*args, **kwargs):
            str_temp = "*" * 80
            test_info_message = ""
            test_result_message = ""
            res = False
            try:
                res = all(function(*args, **kwargs) for _i in range(0, iter))
            except TestFailureException as e:
                test_info_message = "*" + " " * 7 + f"Error: {e}"
            except NotImplementedError as e:
                test_info_message = "*" + " " * 7 + "Testable function not yet implemented"
            finally:
                if res:
                    test_result_message = "*" + " " * 7 + "PASS!"
                else:
                    test_result_message = "*" + " " * 7 + "FAIL!"
                print(
                    f"""
{str_temp}
*       TEST {number}: {message}
{str_temp}
{test_result_message}
{test_info_message}
{str_temp}
"""
                )
                return res

        return wrapper

    return decorator
