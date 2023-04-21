# Generated by Django 4.2 on 2023-04-21 09:43
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0004_delete_applicationconfiguration_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ingredient",
            name="recipe",
        ),
        migrations.RemoveField(
            model_name="tag",
            name="recipe",
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredient",
            field=models.ManyToManyField(
                null=True, to="recipe.ingredient", verbose_name="the related ingredient"
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tag",
            field=models.ManyToManyField(
                blank=True, null=True, to="recipe.tag", verbose_name="the related tag"
            ),
        ),
    ]