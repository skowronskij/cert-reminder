import ssl
import socket
from typing import List

from dateutil.parser import parse
from datetime import datetime, timedelta

from .utils import send_webhook_messages


def get_certificate_expiration_date(host: str, port: int = 443) -> str:
    """
    Get the certificate expiration date of a host.
    :param host: hostname
    :param port: port
    :return: expiration date
    """
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=host
    )
    conn.connect((host, port))
    certificate = conn.getpeercert()
    return certificate['notAfter']


def check_certificate_days_left(date: str) -> timedelta:
    """
    Check how many days left in certificate
    :param date: str
    :return: timedelta
    """
    return parse(date).replace(tzinfo=None) - datetime.now()


def cert_is_about_to_expire(days_left: timedelta, days_buffer: int) -> bool:
    """
    Check if a certificate is about to expire
    :param days_left: timedelta
    :param days_buffer: int
    :return: bool
    """
    days_buffer = timedelta(days=days_buffer)
    return days_left <= days_buffer


def run_cert_reminder(urls: List[str], message: str, days_buffer: int, webhook_urls: List[str]) -> None:
    """
    Run the cert reminder
    :param urls: List[str]
    :param message: str
    :param days_buffer: int
    :param webhook_urls: List[str]
    :return: None
    """        
    print('--------------------------------------------')
    print('-* Checking certificates expiration dates *-')
    print('--------------------------------------------')

    for url in urls:

        print(f'Checking {url}...')

        cert_expiration_date = get_certificate_expiration_date(url)
        print(f'Certificate expiration date: {cert_expiration_date}')
        
        days_left = check_certificate_days_left(cert_expiration_date)
        if cert_is_about_to_expire(days_left, days_buffer):
            
            print(f'{url} is about to expire!\nTime left: {days_left}')

            formated_message = message.format(url=url, days_left=days_left.days)
            send_webhook_messages(formated_message, webhook_urls)

        print('--------------------------------------------')
