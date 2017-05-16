'''
Command to fill database with yaml dataset
'''

from sys import exc_info
from yaml import YAMLError
from os.path import basename, splitext

from django.core.management.base import BaseCommand, CommandError

from ._utils import get_dataset, exc_parse

from amsite.model import Task, Roadmap, State


class Command(BaseCommand):
    help = 'Fills roadmap with given name with values from given yaml file'

    def add_arguments(self, parser):
        parser.add_argument('dataset')
        parser.add_argument('--roadmap', help='Roadmap name. Default is filename')

    def handle(self, *args, **options):
        filename = options['dataset']
        title = options['roadmap'] if options.get('roadmap') else splitext(basename(filename))[0]

        try:
            roadmap = Roadmap(title=title)
            roadmap.save()

            # parse dataset and fill roadmap with values
            for item in get_dataset(filename):
                task = Task(title=item[0], estimate=item[2], roadmap=roadmap)
                if State(item[1]) == State.ready: task.ready()
                task.save()

        except (ValueError, OSError, YAMLError):
            raise CommandError(
                '{} ({}) in <{}:{}>'.format(*exc_parse(exc_info()))
            )

        self.stdout.write(self.style.SUCCESS('Roadmap "{}" was created using "{}"'.format(roadmap.title, filename)))
