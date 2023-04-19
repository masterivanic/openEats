# Generated by Django 4.2 on 2023-04-18 22:37
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("recipe", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(blank=True, max_length=120)),
                ("description", models.CharField(blank=True, max_length=120)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.recipe",
                        verbose_name="the related recipe",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tag",
                "db_table_comment": "Tag table",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
    ]
