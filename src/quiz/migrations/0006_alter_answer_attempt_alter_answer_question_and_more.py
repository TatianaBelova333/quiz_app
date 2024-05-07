# Generated by Django 5.0.4 on 2024-05-07 10:23

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0005_alter_attempt_options_attempt_result_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="attempt",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="quiz.attempt",
                verbose_name="Попытка",
            ),
        ),
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="quiz.question",
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="attempt",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attempts",
                to="quiz.quiz",
                verbose_name="Попытка",
            ),
        ),
        migrations.AlterField(
            model_name="attempt",
            name="result",
            field=models.PositiveSmallIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(
                        limit_value=0, message="Результат не может быть меньше 0."
                    ),
                    django.core.validators.MaxValueValidator(
                        limit_value=100, message="Результат не может быть больше 100."
                    ),
                ],
                verbose_name="Результат попытки",
            ),
        ),
    ]
