import pytest

from src.decorators import log, my_function


@log()
def test_log_is_None_negative_zero_console(capsys):
    with pytest.raises(ZeroDivisionError) as excinfo:
        my_function(1, 0)

    captured = capsys.readouterr()

    # Проверка сообщений об ошибке
    assert "my_function завершилась с ошибкой: ZeroDivisionError: division by zero" in captured.err
    assert "Входные параметры функции: (1, 0), {}" in captured.err

    # Проверка текста исключения
    assert str(excinfo.value) == "division by zero"




if __name__ == "__main__":
    pytest.main(["-vv"])
