import secrets
import string
import random


class GeneratePassword(object):
    """Генерация случайного пароля"""
    def __init__(self):
        self.letters = True
        self.digits = True
        self.chars = True
        self.min_len = 6
        self.max_len = 12
        self.count_chars = 2

    def get_len_pwd(self):
        """Получаем рандомную длину пароля"""
        length = random.randrange(self.min_len, self.max_len)
        length -= self.count_chars

        # проверяем длину пароля
        if length <= self.min_len:
            length = self.min_len
        return length

    def generate_symbol(self):
        characters = ''
        symbol = ''

        if self.letters:
            characters += string.ascii_letters
        if self.digits:
            characters += string.digits
        if self.chars:
            symbol += string.punctuation

        # Генерация случайных цифр и букв
        letter_and_digit = ''.join(secrets.choice(characters) for _ in range(self.get_len_pwd()))
        # Генерация случайных символов
        symbol = ''.join(secrets.choice(string.punctuation) for _ in range(self.count_chars))
        return letter_and_digit + symbol

    def generate(self):
        # Преобразование строки в список символов
        char_list = list(self.generate_symbol())
        # Перемешивание символов в списке
        random.shuffle(char_list)
        # Преобразование списка обратно в строку
        shuffled_string = ''.join(char_list)
        return shuffled_string
