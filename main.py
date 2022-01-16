import argparse

from src.utils import read_settings, check_required_keys, send_webhook_messages
from src.cert_reminder import run_cert_reminder
from src.start_scheduler import set_cronjob

parser = argparse.ArgumentParser(description='Cert reminder')

parser.add_argument('--settings', type=str, help='Path to settings file')

parser.add_argument('--urls', '-u', type=str, nargs='+', help='List of domains to check')
parser.add_argument('--days_buffer', '-d', type=int, help='Days buffer')
parser.add_argument('--webhook_urls', '-w', type=str, nargs='+', help='List of webhook urls')
parser.add_argument('--message', '-m', type=str, help='Message text to send')

parser.add_argument('--no-message', '-nm', action='store_true', help='Do not send a webhook message')

parser.add_argument('--cronjob', '-c', action='store_true', help='Set cronjob')

args = parser.parse_args()


def get_or_create_settings() -> dict:
    """
    Get or create settings
    :return: dict
    """
    if args.settings:
        print('Reading settings from file. Ignore other arguments.')
        settings_path = args.settings
        return read_settings(settings_path)
    else:
        settings = {}

        if args.urls:
            settings['URLS'] = args.urls

        if args.message:
            settings['MESSAGE'] = args.message

        if args.days_buffer:
            settings['DAYS_BUFFER'] = args.days_buffer

        if args.webhook_urls:
            settings['WEBHOOK_URLS'] = args.webhook_urls


        return settings


if __name__ == '__main__':

    settings = get_or_create_settings()
    check_required_keys(settings)

    if not args.no_message:
        send_webhook_messages(message='**Cert reminder** :calendar: by [skowronskij](https://github.com/skowronskij/cert-reminder) started!',
                                webhook_urls=settings.get('WEBHOOK_URLS', []))

    run_cert_reminder(
        urls=settings.get('URLS'),
        message=settings.get('MESSAGE', '{url} certificate expires in {days_left} days'),
        days_buffer=settings.get('DAYS_BUFFER'),
        webhook_urls=settings.get('WEBHOOK_URLS', [])
    )

    if args.cronjob:

        if not args.settings:
            print('--settings is required when using --cronjob')
            exit(1)

        set_cronjob(
            cron_schedule=settings.get('CRON_SCHEDULE', '0 0 * * *'),
            python_path=settings.get('PYTHON_PATH', 'python3'),
            settings=args.settings
        )