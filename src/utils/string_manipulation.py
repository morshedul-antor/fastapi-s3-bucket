import string
import random
import time


class StringManipulation:

    @staticmethod
    def random_str(size=6, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def current_millisecond():
        return round(time.time() * 1000)
