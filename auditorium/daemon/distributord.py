from .. import config
from math import ceil
from socket import socket
from threading import Thread
from json import dumps
from ..components import decorators
from select import select
from ..db.session import DBSession
from ..db.models import Camera


class DistributorDaemon:
    """
    Distributor daemon
    """
    def __init__(self):
        self.connections = []
        self.sock = None
        self.connection_states = [(), (), ()]
        self.cameras = self.get_cameras()

    @decorators.inf
    @decorators.no_exceptions
    def receive_connections(self):
        """
        Receive connections
        :return:
        """
        conn, addr = self.sock.accept()
        self.connections.append(conn)

    def get_cameras(self):
        """
        Get camera list
        :return:
        """
        with DBSession() as session:
            cameras = [camera.ip for camera in session.query(Camera).all()]

        return cameras or []

    @decorators.inf
    @decorators.sleep_after(config.DISTRIBUTOR_CHECK_CONNECTIONS_TIMEOUT)
    @decorators.no_exceptions
    def update_connections(self):
        """
        Check client list and update if it's necessary
        :return:
        """
        self.connection_states = select(
            self.connections,
            self.connections,
            self.connections,
            config.DISTRIBUTOR_CHECK_CONNECTIONS_TIMEOUT
        )

        # exclude readable & exception sockets
        self.connections = list(
            set(self.connection_states[1]) - (set(self.connection_states[0]) | set(self.connection_states[2]))
        )

        if config.DEBUG:
            print("Current client count: {}\n".format(len(self.connections)))
            print("Connection states: {}".format(self.connection_states))
            print("Connections: {}".format(self.connections))

    @decorators.inf
    @decorators.sleep_after(config.DISTRIBUTOR_HOST_UPDATE_TIMEOUT)
    @decorators.no_exceptions
    def distribute(self):
        """
        Distribute cameras list between clients
        """
        cam_count = len(self.cameras)

        if self.connections and cam_count:
            step = ceil(cam_count / len(self.connections))

            cam_collections = [self.cameras[i:i + step] for i in range(0, cam_count, step)]

            for conn, cams in zip(self.connections, cam_collections):
                conn.send(bytes(dumps(cams) + "\n", encoding="utf-8"))

    def start(self):
        """
        Start daemon
        :return:
        """
        with socket() as self.sock:
            self.sock.bind((config.DISTRIBUTOR_HOST, config.DISTRIBUTOR_PORT))
            self.sock.listen(config.DISTRIBUTOR_INCOME_LIMIT)

            update_connections_thread = Thread(target=self.update_connections)
            update_connections_thread.start()

            distr_thread = Thread(target=self.distribute)
            distr_thread.start()

            connections_thread = Thread(target=self.receive_connections)
            connections_thread.start()
            connections_thread.join()
