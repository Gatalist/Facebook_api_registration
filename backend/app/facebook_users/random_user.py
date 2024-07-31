from django.db import IntegrityError
from tools.extensions import random_user, random_password, new_email_ready, random_mail
from tools.playwright_dev import PlaywrightManager

from .models import FacebookUsers, GenderUsers

playwright_manager = PlaywrightManager()


def create_random_user():
    """Генерируем рандомно пользователя в базе"""
    email = random_mail.create_new_email()
    # email = new_email_ready
    new_email = email.get('emailAddress')

    new_user = random_user.generate_user()
    random_pwd = random_password.generate()

    new_user['email'] = new_email
    new_user['inboxId'] = new_email.split('@')[0]  # получаем inboxId с email
    new_user['password'] = random_pwd
    return new_user


def save_random_user(user_data):
    """Сохраняем рандомно созданого пользователя в базе"""

    # Получаем или создаем экземпляр GenderUsers
    gender_name = user_data.get('gender', None)
    if gender_name:
        if GenderUsers.objects.get(name=gender_name):
            gender_instance = GenderUsers.objects.get(name=gender_name)
        else:
            gender_instance = GenderUsers.objects.create(name=gender_name)
    else:
        gender_instance = None

    try:
        # Сохраняем пользователя в базе
        new_user = FacebookUsers.objects.create(
            first_name=user_data.get('first_name', None),
            last_name=user_data.get('last_name', None),
            email=user_data.get('email', None),
            password=user_data.get('password', None),
            birthday=user_data.get('full_date'),
            gender=gender_instance,
            # is_register_fb=True
        )
        print("SAVE USER")
        return new_user
    except IntegrityError as e:
        if 'unique constraint' in str(e):
            print(f"Error: Email {user_data.get('email')} is already in use.")
        else:
            print("An unexpected error occurred.")


def register_user_on_facebook(user_data):
    if user_data:
        print(user_data)
        # Запускаем парсер геристрации
        playwright_manager.open_browser()
        page = playwright_manager.open_page("https://www.facebook.com/reg/")
        playwright_manager.register_facebook_user(page, user_data)


def start_task(count_create_user):
    for i in range(1, count_create_user + 1):
        user_data = create_random_user()
        print(user_data)
        user_obj = save_random_user(user_data)
        print()
        if user_obj:
            if register_user_on_facebook(user_data):
                user_obj.is_register_fb = True
                user_obj.save()
                print("--- FINISH TASK ----")
            else:
                print("--- Failed to register ----")
        else:
            print("--- Failed save USER ----")
