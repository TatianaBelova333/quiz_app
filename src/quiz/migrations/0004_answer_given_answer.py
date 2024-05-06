# Generated by Django 5.0.4 on 2024-05-04 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0003_attempt_answer"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="given_answer",
            field=models.BooleanField(
                choices=[(True, "ДА"), (False, "НЕТ")],
                null=True,
                verbose_name="Полученный ответ",
            ),
        ),
    ]