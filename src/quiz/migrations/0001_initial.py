# Generated by Django 5.0.4 on 2024-05-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        max_length=300, unique=True, verbose_name="Текст вопроса"
                    ),
                ),
                (
                    "correct_answer",
                    models.BooleanField(
                        choices=[(True, "ДА"), (False, "НЕТ")],
                        verbose_name="Правильный ответ",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
    ]
