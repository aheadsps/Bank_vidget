import os
import logging

# абсолютный путь к файлу логов
log_dir = "/Users/anaabramova/PycharmProjects/Bank_vidget/logs"
log_file = os.path.join(log_dir, "masks.log")

# Создаю директорию, если её нет
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number_card: int) -> str | None:
    """Функиця, которая принимает номер карты и возвращает его маску
    в формате XXXX XX** **** XXXX"""
    logger.info("Старт функции get_mask_card_number")
    try:
        if len(str(number_card)) == 16 and number_card > 0 and isinstance(number_card, int):
            logger.debug(f'номер карты прошел фильтрацию: 0 < {number_card} and == 16')

            number_card_str = str(number_card)
            logger.debug(f'номер карты переведен в стоку: {number_card_str}')

            number_card_formatted = f"{number_card_str[:4]} {number_card_str[4:6]}** **** {number_card_str[-4:]}"
            logger.debug(f'номер карты приведен к формату карт: {number_card_formatted}')

            logger.info("Успешное завершение функции get_mask_card_number")
            return number_card_formatted
        else:
            raise ValueError("Некорректный номер карты")

    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print("Номер карты не верен")
        raise ex


def get_mask_account(account_number: int) -> str:
    """Функция, которая прнимает номер счёта и возвращает маску с последними 4 цифрами
    и звездочками перед ними"""
    logger.info("Старт функции get_mask_account")
    try:
        if len(str(account_number)) == 20 and account_number > 0 and isinstance(account_number, int):
            logger.debug(f'номер счета прошел фильтрацию: 0 < {account_number} and == 20')

            account_number_str = str(account_number)
            logger.debug(f'номер счета переведён в строку {account_number_str}')

            account_number_formatted = f"**{account_number_str[-4:]}"
            logger.debug(f'номер счета приведен к формату счета: {account_number_formatted}')

            logger.info("Успешное завершение функции get_mask_card_number")
            return account_number_formatted
        else:
            raise ValueError("Номер счета не верен")

    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print("Номер cчета не верен")
        raise ex

if __name__ == "__main__":
    # input_card_number = input('Введите номер карты: ')
    # get_mask_card_number(int(input_card_number))

    input_account_number = input('Введите номер счета: ')
    get_mask_account(int(input_account_number))