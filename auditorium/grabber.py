import requests
import time
from .components.common import valid_ip
from threading import Thread
from os import path, mkdir
from . import config


class FrameGrabber(Thread):
    """
    Camera's frame grabber class
    """
    def __init__(self, host, login, password, output_dir, port=80, request="/jpg/image.jpg", proto="http", timeout=config.GRAB_DAEMON_TIMEOUT):
        """
        Constructor
        :param host:
        :param port:
        :param request:
        :param proto:
        """
        super().__init__()

        if not valid_ip(host):
            raise Exception("Invalid host.")

        # All possible protos for AXIS
        if proto not in ("http", "rtsp"):
            raise Exception("Invalid protocol.")

        self.uri = "{}://{}:{}{}".format(proto, host,str(int(port)), request)

        if not path.exists(output_dir):
            mkdir(output_dir, 0o777)

        self.output_dir = output_dir
        self.login = login
        self.password = password
        self.timeout = timeout

    def grab(self):
        """
        Grab frame
        :return:
        """
        try:
            req = requests.get(self.uri, auth=requests.auth.HTTPDigestAuth(self.login, self.password), timeout=self.timeout)
            filename = "{}.jpg".format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))

            with open(path.join(self.output_dir, filename), "wb") as f:
                f.write(req.content)
        except Exception:
            print("Frame grabber was not worked properly with: {}".format(self.uri))

    def run(self):
        """
        Run thread
        :return:
        """
        self.grab()


