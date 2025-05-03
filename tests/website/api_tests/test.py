from datetime import datetime, timedelta
import random

# Текущая дата и дата 6 месяцев назад
end_date = datetime.now()
start_date = end_date - timedelta(days=28 * 6)

# Разница в днях между start_date и end_date
total_days = (end_date - start_date).days

# Генерируем две случайные даты
start = start_date + timedelta(days=random.randint(0, total_days))
end = start + timedelta(days=random.randint(0, (end_date - start).days))

random_start_str = start.strftime('%d-%m-%Y')
random_end_str = end.strftime('%d-%m-%Y')

print(random_start_str)
print(random_end_str)