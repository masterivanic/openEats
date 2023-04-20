import csv
from collections import namedtuple

from django.core.management.base import BaseCommand

from ...models import Ingredient


class IngredientModel:
    """model use for define our csv file header (structure)"""

    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description


class Command(BaseCommand):
    help = "Help us to import ingredient in db"

    def add_arguments(self, parser) -> None:
        """here we define args for our command"""

        parser.add_argument("import_ingredient_file", type=str, nargs="?")

    def handle(self, *args, **options):
        try:
            list_ingredient = []
            with open("data/ingredients.csv", "r") as file:
                read = csv.reader(file)
                IngredientModel = namedtuple("IngredientModel", next(read))
                for line in read:
                    ingredient = IngredientModel(*line)
                    list_ingredient.append(
                        Ingredient(
                            name=ingredient.name, description=ingredient.description
                        )
                    )
                Ingredient.objects.bulk_create(list_ingredient, batch_size=100)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully created "%d"' % len(list_ingredient)
                        + "ingredients"
                    )
                )
        except Exception:
            self.stdout.write(
                self.style.ERROR("Something wrong while processing the action")
            )
            raise Exception
