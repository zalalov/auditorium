import asyncore
import socket
from os import path
from .. import config
from ..components.darkflow.net.build import TFNet
import mimetypes
import cv2
import threading
import tempfile


class PersonsSumming(threading.Thread):
    """
    Class for working with NN by multithreading
    """
    def __init__(self, tfnet, img):
        """
        Persons Summing Constructor
        :param img:
        """
        super(PersonsSumming, self).__init__()

        self.tfnet = tfnet
        self.img = img
        self.count = 0

    def run(self):
        """
        Run
        :return:
        """
        if config.DEBUG:
            print("DARKFLOW THREAD #{} STARTED...".format(threading.get_ident()))

        if config.DARKFLOW_SCALING:
            self.img = cv2.resize(self.img, (0, 0), fx=2, fy=2)

        if config.DARKFLOW_EQUILIZING:
            img_yuv = cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            self.img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        result = self.tfnet.return_predict(self.img)
        persons = [x for x in result if x["label"] == "person"]

        # for person in persons:
        #     cv2.rectangle(
        #         self.img,
        #         (person["topleft"]["x"], person["topleft"]["y"]),
        #         (person["bottomright"]["x"], person["bottomright"]["y"]),
        #         (255, 0, 0),
        #         2
        #     )
        # cv2.imwrite(tempfile.NamedTemporaryFile(prefix="prediction_", dir="/Users/ruslan/tmp/", suffix=".jpg").name, self.img)

        self.count = len(persons)


class DarkflowReadHandler(asyncore.dispatcher_with_send):
    """
    Darkflow server's read handler
    """
    debug = True

    def __init__(self, sock, checking_tfnet, tfnet):
        """
        Read handler constructor
        :param tfnet:
        """
        super().__init__(sock)
        self.checking_tfnet = checking_tfnet
        self.tfnet = tfnet

    def handle_read(self):
        """
        Read handler method
        :return:
        """
        try:
            data = self.recv(1024)
            filepath = str(data, encoding="utf-8").strip()

            if not filepath:
                raise Exception("Empty data received.")

            if config.DEBUG:
                print("Received data: {}".format(filepath))

            if path.exists(filepath):
                mimetype = mimetypes.guess_type(filepath)

                if mimetype[0] and mimetype[0].split("/")[0] == "image":
                    imgcv = cv2.imread(filepath)
                    persons = 0

                    if self.check_existing(imgcv):
                        persons = self.get_persons_count(imgcv)

                    if config.DEBUG:
                        print("{} : {}\n".format(filepath, persons))

                    self.send(str(persons).encode())
                else:
                    raise Exception("File is not an image.")
            else:
                raise Exception("Invalid path.")
        except Exception as e:
            if config.DEBUG:
                print(str(e))

            self.send("0".encode())

        self.close()

    def slice_img(self, img):
        """
        Slice image to small ones
        :param img:
        :return:
        """
        height, width, _ = img.shape
        # cut 5% of picture
        delta_w = width // 100 * 3
        delta_h = height // 100 * 3

        border_y = [
            height // 2 - delta_h,
            height // 2 + delta_h,
        ]
        border_x = [
            width // 2 - delta_w,
            width // 2 + delta_w,
        ]

        return [
            img[0:border_y[0], 0:border_x[0]],
            img[0:border_y[0], border_x[1]:width],
            img[border_y[1]:height, 0:border_x[0]],
            img[border_y[1]:height, border_x[1]:width],
        ]

    def check_existing(self, imgcv):
        """
        Check existing persons on image
        :param imgcv:
        :return:
        """
        t = PersonsSumming(self.checking_tfnet, imgcv)
        t.start()
        t.join()

        return t.count > 0

    def get_persons_count(self, imgcv):
        """
        Get persons count
        :param imgcv:
        :return:
        """
        threads = []

        if config.DARKFLOW_SLICING:
            for part in self.slice_img(imgcv):
                thread = PersonsSumming(self.tfnet, part)
                threads.append(thread)
        else:
            threads = [PersonsSumming(self.tfnet, imgcv)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return sum([x.count for x in threads])



class DarkflowServer(asyncore.dispatcher):
    """
    Darkflow server
    """
    def __init__(self, host, port, checking_tfnet, tfnet):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.checking_tfnet = checking_tfnet
        self.tfnet = tfnet

    def handle_accept(self):
        pair = self.accept()

        if pair is not None:
            sock, addr = pair
            print('Incoming connection from {}'.format(repr(addr)))
            DarkflowReadHandler(sock, self.checking_tfnet, self.tfnet)


class DarkflowDaemon:
    """
    Darkflow daemon
    """
    def start(self):
        """
        Start daemon
        :return:
        """
        options = {
            "model": config.DARKFLOW_MODEL,
            "load": config.DARKFLOW_WEIGHTS,
            "binary": config.DARKFLOW_BIN_PATH,
            "config": config.DARKFLOW_CFG_PATH,
            "threshold": config.DARKFLOW_THRESHOLD
        }

        tfnet = TFNet(options)

        options.update({"threshold": config.DARKFLOW_EXISTING_CHECK_THRESHOLD})
        checking_tfnet = TFNet(options)

        DarkflowServer(config.DARKFLOW_HOST, config.DARKFLOW_PORT, checking_tfnet, tfnet)
        asyncore.loop()
