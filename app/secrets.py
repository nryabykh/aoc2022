import os


def get_session_id():
    return os.getenv('AOC_SESSION')
