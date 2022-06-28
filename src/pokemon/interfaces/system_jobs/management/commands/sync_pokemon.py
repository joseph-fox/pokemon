from django.core import management

from pokemon.domain.creatures import crawlers
from pokemon.tools import loggers


class Command(management.BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('max_task_num', nargs='?', type=int, help='Shop ID')

    def handle(self, *args, **options):
        max_task_num = options['max_task_num']

        try:
            crawlers.update_creatures(max_task_num=max_task_num)
        except Exception as e:
            # Errors happened, leave a trace at the system/machine level.
            # Logs get collected, such as, CloudWatch etc.
            self.stderr.write(
                f'Errors happened while updating creatures - {str(e)}')

            # Also, log it to Sentry to get engineering attention
            # and return early.
            return loggers.app_logger.exception(
                'Failed to schedule a creature sync task')

        # Leave a log at the system/machine level.
        self.stdout.write('Scheduled creature sync task.')
