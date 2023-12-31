# Generated by Django 4.2 on 2023-05-03 14:13
import django.db.models.functions.text
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Upper("name"),
                name="unique_ingredient_upper_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="tag",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Upper("name"),
                name="unique_tag_upper_name",
            ),
        ),
    ]
