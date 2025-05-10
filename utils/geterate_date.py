import random
from datetime import datetime, timedelta


def generate_date():
    # ГЕНЕРАЦИЯ ДАТЫ для формирования отчета
    # Текущая дата и дата 6 месяцев назад
    end_date = datetime.now()
    start_date = end_date - timedelta(days=28 * 6)

    # Разница в днях между start_date и end_date
    total_days = (end_date - start_date).days

    # Генерируем две случайные даты
    start = start_date + timedelta(days=random.randint(0, total_days))
    end = start + timedelta(days=random.randint(0, (end_date - start).days))

    random_start_str = start.strftime('%Y-%m-%d')
    random_end_str = end.strftime('%Y-%m-%d')

    return random_start_str, random_end_str