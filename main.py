import datetime
import logging
import sched, time
import notify2
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from config import USER, PASSWORD, DELAY

notify2.init('gmail')
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)


def parse_timestamp(ts):
    return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")


class GMail:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.last_one = None

    def check(self):
        res = requests.get(
            'https://mail.google.com/mail/feed/atom/',
            auth=HTTPBasicAuth(self.user, self.password))
        if res.status_code != 200:
            raise RuntimeError(res.text)
        bs = BeautifulSoup(res.content, features='xml')

        last_one = bs.find('entry')

        # is it the same one we checked before
        if self.last_one and parse_timestamp(self.last_one.modified.text) >= \
                parse_timestamp(last_one.modified.text):
            return

        # don't show it the first time, since it's
        # not new, just the last one in the box
        if self.last_one:
            title = '{} ({}): {}'.format(
                last_one.author.find('name').text,
                last_one.author.email.text,
                last_one.title.text)

            n = notify2.Notification(title, last_one.summary.text)
            n.show()

        # but update it
        self.last_one = last_one


g = GMail(USER, PASSWORD)
s = sched.scheduler()

def check_mail():
    logging.info('checking')
    try:
        g.check()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        logging.error(e)
    logging.info('checked')
    s.enter(DELAY, 1, check_mail)

check_mail()
s.run()
