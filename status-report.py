#!/usr/bin/env python


import email.mime.text
import getpass
import optparse
import signal
import socket
import smtplib
import sys


def main ():
    options, to_addresses = parser().parse_args()
    connection = smtplib.SMTP('localhost')
    message = email.mime.text.MIMEText(sys.stdin.read())
    message['Subject'] = 'status-report'
    message['From'] = options.from_address
    message['To'] = ', '.join(to_addresses)
    connection.sendmail(
        options.from_address,
        to_addresses,
        message.as_string(),
    )
    connection.quit()


def parser ():
    parser = optparse.OptionParser()
    parser.add_option('--subject')
    parser.add_option('--from-address')
    parser.add_option('-v', '--verbose', action='store_true')
    fqdn = socket.getfqdn()
    parser.set_defaults(
        from_address = '{user}@{domain}'.format(
            user = getpass.getuser(),
            domain = fqdn,
        ),
        subject = 'status report from {0}'.format(fqdn),
        verbose = False,
    )
    return parser


def install_sigint_handler ():
    signal.signal(signal.SIGINT, sigint_handler)


def sigint_handler (signal, frame):
    sys.exit(-1)


if __name__ == '__main__':
    install_sigint_handler()
    main()
