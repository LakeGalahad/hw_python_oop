import datetime as dt


class Calculator:
    def __init__(self, limit):
        """Инициализировать данные создаваемого объекта."""
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Добавить запись."""
        self.records.append(record)
    
    def get_today_stats(self):
        """Возвращает затраты на текущий день."""
        # Текущий день.
        today = dt.date.today()
        today_sum = sum([record.amount for record in self.records 
                            if record.date == today])
        return today_sum

    def get_week_stats(self):
        """Возвращает затраты за неделю."""
        # Текущий день.
        today = dt.date.today()
        # Недельный интервал.
        week_interval = today - dt.timedelta(days=7)
        week_sum = sum([record.amount for record in self.records 
                            if week_interval < record.date <= today])
        return week_sum

    def get_amount_left(self):
        """Возвращает количество оставшихся ресурсов."""
        # Количество потраченных ресурсов.
        amount_spent = self.get_today_stats()
        # Количество оставшихся ресурсов.
        amount_left = self.limit - amount_spent
        return amount_left


class Record:
    def __init__(self, amount, comment, date=None):
        """Инициализация данных."""
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Возвращает информацию об оставшихся каллориях."""
        calories_left = self.get_amount_left()
        if calories_left > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                        f'калорийностью не более {calories_left} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    # Константы курсов валют
    USD_RATE = 78.00
    EURO_RATE = 91.00

    def get_today_cash_remained(self, currency):
        """Возвращает информацию об оставшихся деньгах."""
        cash_left = self.get_amount_left()
        if cash_left == 0:
            return 'Денег нет, держись'
        # Определение валюты.
        RATE_DICT = {
            'rub': ('руб', 1.00),
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE)
        }
        if currency in RATE_DICT:
            str_currency, rate = RATE_DICT[currency]
            cash_left = round(cash_left / rate, 2)
        else:
            raise ValueError
        if cash_left > 0:
            return f'На сегодня осталось {cash_left} {str_currency}'
        cash_left = abs(cash_left)
        return f'Денег нет, держись: твой долг - {cash_left} {str_currency}'