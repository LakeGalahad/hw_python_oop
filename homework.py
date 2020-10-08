import datetime as dt

class Calculator:
    # Инициализация данных. 
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Метод для добавления записей.
    def add_record(self, record):
        self.records.append(record)
    
    # Метод для вычисления затрат на текущий день.
    def get_today_stats(self):
        today_sum = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                today_sum = today_sum + record.amount
        return today_sum

    # Метод для вычисления затрат за неделю.
    def get_week_stats(self):
        week_sum = 0
        for record in self.records:
            # Проверка на попадание записи в недельный интервал.
            if (record.date > dt.datetime.now().date() - dt.timedelta(days=7)
            and record.date <= dt.datetime.now().date()):
                week_sum = week_sum + record.amount
        return week_sum


class Record:
    # Инициализация данных. 
    def __init__(self, amount, comment, date=dt.datetime.today().date()):
        self.amount = amount
        self.comment = comment
        if type(date) == str:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = date


class CaloriesCalculator(Calculator):
    # Метод для вычисления оставшихся каллорий.
    def get_calories_remained(self):
        # Количество потраченных каллорий.
        calories_spent = self.get_today_stats()
        # Количество оставшихся каллорий.
        calories_left = self.limit - calories_spent
        if calories_left > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                        f'калорийностью не более {calories_left} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    # Константы курсов валют
    USD_RATE = 78.00
    EURO_RATE = 91.00

    # Метод для вычисления оставшихся денег.
    def get_today_cash_remained(self, currency):
        str_currency = ''
        # Количество потраченных денег.
        cash_spent = self.get_today_stats()
        # Количество оставшихся денег.
        cash_left = self.limit - cash_spent
        # Определение валюты.
        if currency == 'rub':
            str_currency = 'руб'
        elif currency == 'usd':
            cash_left = round(cash_left / self.USD_RATE, 2)
            str_currency = 'USD'
        elif currency == 'eur':
            cash_left = round(cash_left / self.EURO_RATE, 2)
            str_currency = 'Euro'
        else:
            raise ValueError
        if cash_left > 0:
            return f'На сегодня осталось {cash_left} {str_currency}'
        if cash_left == 0:
            return 'Денег нет, держись'
        cash_left = abs(cash_left)
        return f'Денег нет, держись: твой долг - {cash_left} {str_currency}'