import multiprocessing as mp
import json
from time import sleep
from threading import Thread
from auditorium.grabber import FrameGrabber
from concurrent.futures import ProcessPoolExecutor
from auditorium.components.common import valid_ip, build_host_path
from functools import partial
from math import ceil
from auditorium import config
from os import path, mkdir, mknod, remove
from ..components import decorators
from socket import socket


class GrabDaemon:
    """
    Grab daemon
    """
    def __init__(self):
        """
        Constructor
        :param hosts:
        """
        if config.GRAB_DAEMON_TIMEOUT < 60:
            raise Exception("Invalid grab daemon's timeout.")

        if not path.exists(config.GRAB_DAEMON_OUTPUT_DIR):
            mkdir(config.GRAB_DAEMON_OUTPUT_DIR, 0o777)

        self.hosts = []
        self.socket = None
        self.ppexecutor = None
        self.connect_to_distributor()

        hosts_thread = Thread(target=self.update_hosts)
        hosts_thread.start()

    def connect_to_distributor(self):
        """
        Connect to distibutor daemon
        :return:
        """
        self.socket = socket()
        self.socket.connect((config.DISTRIBUTOR_HOST, config.DISTRIBUTOR_PORT))

    def grab(self, hosts):
        """
        Start grabbing threads
        :param hosts:
        :return:
        """
        while True:
            for host in hosts:
                if config.DEBUG:
                    print("PROCESSING HOST: {}".format(host))

                grabber = FrameGrabber(
                    host,
                    config.GRAB_DEFAULT_LOGIN,
                    config.GRAB_DEFAULT_PASSWORD,
                    build_host_path(host)
                )
                grabber.start()

            if self.check_restart():
                if config.DEBUG:
                    print("RESTARTING PROCESS\n")

                break

            sleep(config.GRAB_DAEMON_TIMEOUT)

    @decorators.inf
    @decorators.sleep_after(config.DISTRIBUTOR_HOST_UPDATE_TIMEOUT)
    def update_hosts(self):
        data = self.socket.recv(2 ** 20)

        if not data:
            self.hosts = []
            self.set_restart()
            raise Exception("Invalid hosts list.")

        data = data.decode("utf-8").strip()
        hosts = json.loads(data)

        for host in hosts:
            if not valid_ip(host):
                raise Exception("Invalid hosts list.")

        if set(hosts) != set(self.hosts):
            if config.DEBUG:
                print("HOST LIST CHANGED!\n")

            self.set_restart()
            self.hosts = hosts

        if config.DEBUG:
            print("NEW HOSTS: {}".format(self.hosts))

        return hosts

    def set_restart(self, f=True):
        """
        Restart toggles
        :param f:
        :return:
        """
        if f and not path.exists(config.GRAB_DAEMON_RESTART_FLAG_PATH):
            mknod(config.GRAB_DAEMON_RESTART_FLAG_PATH)
        elif not f and path.exists(config.GRAB_DAEMON_RESTART_FLAG_PATH):
            remove(config.GRAB_DAEMON_RESTART_FLAG_PATH)

    def check_restart(self):
        """
        Check if it's time to restart!
        :return:
        """
        return path.exists(config.GRAB_DAEMON_RESTART_FLAG_PATH)

    @decorators.inf
    @decorators.sleep_after(config.GRAB_DAEMON_RESTART_TIMEOUT)
    def start(self):
        """
        Start daemon
        :return:
        """
        if self.hosts:
            with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
                self.set_restart(False)

                if config.DEBUG:
                    print("\n\nSTARTING\n\n")

                host_count = len(self.hosts)
                cpu_count = mp.cpu_count()
                step = ceil(host_count / cpu_count)
                spawn = partial(executor.submit, self.grab)
                [spawn(self.hosts[i:i + step]) for i in range(0, len(self.hosts), step)]
