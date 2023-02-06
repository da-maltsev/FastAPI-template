import datetime
import logging


def do_something() -> None:
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=1)
    try:
        logging.info(f"Плановая задача. Начало периода:{start} Конец периода:{end}")
    except Exception as e:
        logging.error(f"Ошибка при выполнении плановой задачи. Тело ошибки:\n{e}")
