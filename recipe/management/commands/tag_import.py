import csv
import os
from collections import namedtuple
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser

from ...models import Tag


class Command(BaseCommand):
    help = "Help us to import tag in db"

    def add_arguments(self, parser: CommandParser) -> None:
        """here we define default path of our file with a key word"""

        parser.add_argument(
            "import_tag_file",
            type=str,
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "data/tags.csv"),
        )

    def handle(self, *args, **options) -> Optional[str]:
        """define action to do while parsing command"""

        try:
            list_tags = []
            file_path = options.get("import_tag_file")
            if file_path and file_path.endswith(".csv"):
                with open(file_path, "r") as file:
                    reader = csv.DictReader(file)
                    for line in reader:
                        list_tags.append(
                            Tag(name=line["name"], description=line["description"])
                        )
                    Tag.objects.bulk_create(list_tags, batch_size=100)
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Successfully created "%d"' % len(list_tags) + "tags"
                        )
                    )
            else:
                raise FileNotFoundError
        except Exception:
            self.stdout.write(
                self.style.ERROR("Something wrong while processing the action")
            )
            raise Exception
