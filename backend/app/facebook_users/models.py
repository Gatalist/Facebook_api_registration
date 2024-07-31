from django.db import models
from django.urls import reverse
from datetime import date


class BaseModel(models.Model):
    is_active = models.BooleanField("Активен", default=True)
    sorted = models.IntegerField("Сортировка", default=100)
    created = models.DateTimeField("Создан", auto_now_add=True)
    updated = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        abstract = True


class GenderUsers(BaseModel):
    """Пол"""
    name = models.CharField('Имя', max_length=20, default="Другое")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Пол"
        verbose_name_plural = "Пол"


class FacebookUsers(BaseModel):
    """Категория"""
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.CharField('Email', max_length=250, unique=True, db_index=True)
    password = models.CharField('Пароль', max_length=50)
    birthday = models.DateField("Дата рождения", null=True, blank=True)
    gender = models.ForeignKey(GenderUsers, on_delete=models.CASCADE, null=True, blank=True)
    poster = models.ImageField("Изображение", upload_to='user_fb/', null=True, blank=True)
    is_register_fb = models.BooleanField("Прошел регистрацию на Fb", default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Имя и Фамилия"
        verbose_name_plural = "Аккаунты Facebook"
