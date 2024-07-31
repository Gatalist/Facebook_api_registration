# Generated by Django 5.0.7 on 2024-07-29 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('sorted', models.IntegerField(default=100, verbose_name='Сортировка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('email', models.CharField(db_index=True, max_length=250, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('poster', models.ImageField(null=True, upload_to='user_fb/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Имя и Фамилия',
                'verbose_name_plural': 'Аккаунты Facebook',
            },
        ),
    ]
