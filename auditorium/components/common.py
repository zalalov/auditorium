import re
from os import path
from .. import config


def valid_ip(a):
    """
    Validate ip address
    :param a:
    :return:
    """
    return re.fullmatch("(\d{1,3}\.){3}\d{1,3}", a)


def build_host_path(host):
    """
    Build path for frame
    :param host:
    :return:
    """
    if not valid_ip(host):
        raise Exception("Invalid host.")

    return path.join(config.GRAB_DAEMON_OUTPUT_DIR, "{}".format(host))


def pwd():
    """
    Get dir of script
    :return:
    """
    return path.dirname(path.abspath(__file__))