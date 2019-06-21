import shortuuid
import string


def generate_sn(no):
    return (10 - len(str(no))) * '0' + str(no)


def generate_code(length=10):
    return shortuuid.ShortUUID(string.ascii_lowercase + string.digits).random(length=length)
