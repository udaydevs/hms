import re

def check_regex(regex, value):
    x = re.fullmatch(regex, value)
    return x
