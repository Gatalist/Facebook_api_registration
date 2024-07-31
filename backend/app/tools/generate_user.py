from faker import Faker
import random


class GenerateUser:
    def __init__(self):
        self.faker = Faker()
        self.gender = ['male', 'female']
        self.years = [item for item in range(1970, 2000)]
        self.months = [item for item in range(1, 12)]
        self.days = [item for item in range(1, 28)]

    @staticmethod
    def random_choice(list_data: list) -> any:
        "Выбираем рандомное значение из списка"
        choice = random.choice(list_data)
        return choice

    def generate_female_name(self) -> tuple:
        "Генерируем Женское имя"
        first_name = self.faker.first_name_female()  # Имя
        last_name = self.faker.last_name_female()  # Фамилия
        return first_name, last_name

    def generate_male_name(self) -> tuple:
        "Генерируем Мужское имя"
        first_name = self.faker.first_name_male()  # Имя
        last_name = self.faker.last_name_male()  # Фамилия
        return first_name, last_name

    def generate_user(self):
        # Генерация случайного полного имени пользователя
        day = self.random_choice(self.days)
        month = self.random_choice(self.months)
        year = self.random_choice(self.years)
        gender = self.random_choice(self.gender)
        first_name, last_name = '', ''
        if gender == 'male':
            first_name, last_name = self.generate_male_name()
        elif gender == 'female':
            first_name, last_name = self.generate_female_name()

        result = {
            "day": day,
            "month": month,
            "year": year,
            "full_date": f'{year}-{month}-{day}',
            "gender": gender,
            "first_name": first_name,
            "last_name": last_name,
        }
        return result
