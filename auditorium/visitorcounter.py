from os import listdir, path
import mimetypes
from natsort import natsorted
from auditorium import config
from datetime import datetime
import socket


class VisitorCounter:
    """
    Visitor counter class
    """

    def __init__(self, dir, **kwargs):
        """
        Constructor
        :param dir:
        """
        self.images = []
        self.start_time = None
        self.end_time = None
        self.visitor_list = []

        if "visitor_list" not in kwargs:
            raise Exception("Visitor list should be specified.")

        files = [path.join(dir, f) for f in listdir(dir)]

        self.visitor_list = kwargs["visitor_list"]

        if "start_time" in kwargs:
            self.start_time = kwargs["start_time"]

        if "end_time" in kwargs:
            self.end_time = kwargs["end_time"]

        for f in files:
            mimetype = mimetypes.guess_type(f)

            if not mimetype[0]:
                continue

            if mimetype[0].split("/")[0] != "image":
                continue

            if self.start_time and self.end_time:
                if self.start_time <= datetime.fromtimestamp(path.getmtime(f)) <= self.end_time:
                    self.images.append(f)
            else:
                self.images.append(f)

        if len(self.images) < 1:
            raise Exception("Images count is not enough.")

        self.images = natsorted(self.images, key=lambda x: path.basename(x))

    def count(self):
        """
        Get people count
        :return:
        """
        image_count = len(self.images)
        counted_length = len(self.visitor_list)

        if counted_length != 0 and counted_length == image_count:
            if config.DEBUG:
                print("Recognize for that event had already done.")

            return self.get_total(self.visitor_list), self.visitor_list

        if counted_length > image_count:
            self.visitor_list = []
            counted_length = 0

        for image in self.images[counted_length:len(self.images)]:
            if config.DEBUG:
                print("Image to recognize: {}".format(image))

            self.visitor_list.append(int(self.get_persons_on_image(image)))

        return self.get_total(self.visitor_list), self.visitor_list

    def get_total(self, visitor_list):
        """
        Get total value of visitors
        :param visitor_list:
        :return:
        """
        total = max(self.visitor_list)

        if config.COUNT_SMOOTHING:
            avg = sum(self.visitor_list) / len(self.visitor_list)

            if config.DEBUG:
                print("AVERAGE: {}".format(avg))

            if avg <= .5:
                total = 0

        return total

    def get_persons_on_image(self, filepath):
        """
        Get person count on image by darkflow server
        :param filepath:
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((config.DARKFLOW_HOST, config.DARKFLOW_PORT))
        s.send(filepath.encode())
        persons = s.recv(1024).decode()
        s.close()

        if not persons:
            persons = 0

        return persons

