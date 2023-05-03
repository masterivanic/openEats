import csv
import os
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser

from recipe.models import Ingredient


class Command(BaseCommand):
    help = "Help us to import ingredient in db"

    def add_arguments(self, parser: CommandParser) -> None:
        """here we define default path of our file with a key word"""

        parser.add_argument(
            "import_ingredient_file",
            type=str,
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "data/ingredients.csv"),
        )

    def handle(self, *args, **options) -> Optional[str]:
        try:
            list_ingredient = []
            file_path = options.get("import_ingredient_file")
            if file_path and file_path.endswith(".csv"):
                with open(file_path, "r") as file:
                    reader = csv.DictReader(file)
                    for line in reader:
                        list_ingredient.append(
                            Ingredient(
                                name=line["name"], description=line["description"]
                            )
                        )
                    Ingredient.objects.bulk_create(list_ingredient, batch_size=100)
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Successfully created "%d"' % len(list_ingredient)
                            + "ingredients"
                        )
                    )
            else:
                raise FileNotFoundError

        except Exception:
            self.stdout.write(
                self.style.ERROR("Something wrong while processing the action")
            )
            raise Exception
