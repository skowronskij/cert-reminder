import os

from crontab import CronTab
from pathlib import Path
from getpass import getuser


def set_cronjob(cron_schedule: str, python_path: str, settings: str) -> None:
    """
    Set a cronjob
    :param cron_schedule: str
    :param python_path: str
    :return: None
    """

    docker_runmode = os.environ.get('DOCKER_RUNMODE')
    if docker_runmode == 'TRUE':
        python_path = '/usr/local/bin/python'

    file_path = Path(__file__).parent.parent.absolute().joinpath('main.py')

    with CronTab(user=getuser()) as cron:
        job = cron.new(command=f'{python_path} {file_path} --settings {settings} --no-message >> /dev/console')
        job.setall(cron_schedule)
        cron.write()
