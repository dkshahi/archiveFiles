# -*- coding: utf-8 -*-
import smtplib
import string
import sys
__author__ = 'Victor Pendleton'


class Email:
    logger =None
    utils = None

    def __init__(self, utils):
        self.utils = utils
        self.logger = utils.get_logging()

    def test_email(self):
        smtp_server = 'smtp.us.exg7.exghost.com'
        port = 587
        try:
            s = smtplib.SMTP(smtp_server, port)
            s.starttls()

        except:
            print(sys.exc_info())

    def send_email(self, config, logger, sub='Backup and Archive notification', msg='', notifyall='no'):
        addresslist = []
        mailserver = None
        recp = []
        sender = None
        try:
            if notifyall.lower() == 'yes':
                addresslist = config.get('smtp', 'errors').split(',')
                for address in addresslist:
                    recp.append(address)

            # Reset addresslist
            addresslist = []

            addresslist = config.get('smtp', 'info').split(',')
            for address in addresslist:
                recp.append(address)

            # Reset addresslist
            addresslist = []

            sender = config.get('smtp', 'from')
            mailserver = smtplib.SMTP(config.get('smtp', 'server'))
            if config.get('smtp', 'debug').lower() == 'true':
                mailserver.set_debuglevel(config.get('smtp', 'debug'))

            msg = string.join(("From: {sender}".format(sender=sender), "To:", "Subject: {sub}".format(sub=sub), "", msg), "\r\n")
            mailserver.sendmail(sender, recp, msg)
            mailserver.quit()
        except:
            self.utils.captureException("Error sending email notification", sys.exc_info(), logger)
        finally:
            mailserver = None
