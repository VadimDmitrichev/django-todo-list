# Generated by Django 4.1.5 on 2023-01-10 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0003_rename_importance_todo_important"),
    ]

    operations = [
        migrations.RenameField(
            model_name="todo", old_name="description", new_name="memo",
        ),
    ]
