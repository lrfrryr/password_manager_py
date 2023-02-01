import random
import string


def generate_password(long):
    passw = ''.join([random.choice(string.ascii_letters +
                                   string.digits + string.punctuation)
                     for n in range(long)])
    return passw

