# Generated by Django 4.1.5 on 2023-01-10 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0002_alter_todo_datecompleted"),
    ]

    operations = [
        migrations.RenameField(
            model_name="todo", old_name="importance", new_name="important",
        ),
    ]
