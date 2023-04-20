import csv
from collections import namedtuple

from django.core.management.base import BaseCommand

from ...models import Tag


class TagModel:
    """model use for define our csv file header (structure)"""

    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description


class Command(BaseCommand):
    help = "Help us to import tag in db"

    def add_arguments(self, parser) -> None:
        """here we define args for our command"""

        parser.add_argument("import_tag_file", type=str, nargs="?")

    def handle(self, *args, **options):
        """define action to do while parsing command"""

        try:
            list_tags = []
            with open("data/tags.csv", "r") as file:
                read = csv.reader(file)
                TagModel = namedtuple("TagModel", next(read))
                for line in read:
                    tag = TagModel(*line)
                    list_tags.append(Tag(name=tag.name, description=tag.description))
                Tag.objects.bulk_create(list_tags, batch_size=100)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully created "%d"' % len(list_tags) + "tags"
                    )
                )
        except Exception:
            self.stdout.write(
                self.style.ERROR("Something wrong while processing the action")
            )
            raise Exception
