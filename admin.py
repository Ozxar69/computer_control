import os

from dotenv import load_dotenv

from data import ADMIN_IDS

load_dotenv()

ADMIN = os.getenv(ADMIN_IDS)


def check_user(id):
    if id == int(ADMIN):
        return True
    return False
