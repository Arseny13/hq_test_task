# Generated by Django 4.2.5 on 2023-09-20 19:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lesson", "0002_userlesson_unique_user_lesson_userlesson_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userlesson",
            name="status",
        ),
        migrations.AlterField(
            model_name="userlesson",
            name="date_last",
            field=models.DateField(auto_now=True, verbose_name="Дата просмотра"),
        ),
    ]
