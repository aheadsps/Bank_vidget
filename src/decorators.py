import logging
import sys
from functools import wraps
from typing import Any, Callable, Dict, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования начала и конца выполнения функции, а также её результатов или возникших ошибок.
    Если filename задан, логи записываются в указанный файл.
    Если filename не задан, логи выводятся в консоль.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Dict[Any, Any]) -> Any:
            print(f"Начало выполнения функции {func.__name__}")
            try:
                result: Any = func(*args, **kwargs)
                print(f"{func.__name__} ok")
                return result
            except Exception as e:
                error_message = f"{func.__name__} завершилась с ошибкой: {e.__class__.__name__}: {e}\
                \nВходные параметры функции: {args}, {kwargs}\n"
                if filename:
                    logging.basicConfig(filename=filename, level=logging.ERROR, filemode="a")
                    logging.error(error_message)
                else:
                    print(error_message, file=sys.stderr)  # Выводим сообщение в stderr

                raise e
            finally:
                print(f"Конец выполнения функции {func.__name__}\n")

        return wrapper

    return decorator


@log()  # Логирование в консоль
def my_function(arg1: int, arg2: int) -> float:
    """Функция, которая задаёт правила работы декоратора log"""
    if arg2 == 0:
        print("Ошибка: деление на ноль")
        raise ZeroDivisionError("division by zero")
    else:
        print("my_function выполнена")
        return arg1 / arg2
