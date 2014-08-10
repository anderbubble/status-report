#!/usr/bin/env python


import email.mime.text
import getpass
import optparse
import signal
import socket
import smtplib
import sys
import threading


def main ():
    options, to_addresses = parser().parse_args()
    connection = smtplib.SMTP('localhost')
    input_buffer = []
    reader = threading.Thread(target=reader_thread, args=(input_buffer, ))
    reader.start()
    while True:
        reader.join(60)
        message = email.mime.text.MIMEText(''.join(input_buffer))
        message['Subject'] = options.subject
        message['From'] = options.from_address
        message['To'] = ', '.join(to_addresses)
        if options.verbose:
            print >>sys.stderr, 'sending status report'
        connection.sendmail(
            options.from_address,
            to_addresses,
            message.as_string(),
        )
        if not reader.is_alive():
            break
    connection.quit()


def reader_thread (input_buffer):
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        input_buffer.append(line)


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
