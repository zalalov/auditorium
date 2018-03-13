from datetime import datetime
from os import path
from time import sleep
from auditorium import config
from sqlalchemy import and_, inspect
from ..visitorcounter import VisitorCounter
from ..db.models import RoomEvent, Room, Camera
from ..db.session import DBSession
from ..components.common import build_host_path


class RecognizeDaemon:
    """
    Grab daemon
    """
    def get_event_data(self):
        """
        Get room events data from DB
        :return:
        """
        now = datetime.now()

        event_data = []

        with DBSession() as session:
            events = session.query(RoomEvent).filter(and_(RoomEvent.start_time <= now, RoomEvent.end_time >= now)).all()

            for event in events:
                if event.room.cameras:
                    visitor_list = event.visitor_list.split(",") if event.visitor_list else []
                    visitor_list = list(map(int, visitor_list))

                    event_data.append({
                        "start_time": event.start_time,
                        "end_time": event.end_time,
                        "host": event.room.cameras[0].ip,
                        "visitor_list": visitor_list,
                        "room": event.room.name,
                        "building": event.room.building_id,
                        "id": event.id
                    })

        return event_data

    def start(self):
        """
        Start daemon
        :return:
        """
        while True:
            for event_data in self.get_event_data():
                if config.DEBUG:
                    print("\n\n{}\n".format("-" * 20))

                source = build_host_path(event_data["host"])

                if not path.exists(source):
                    continue

                count = None

                try:
                    count = VisitorCounter(
                        source,
                        start_time=event_data["start_time"],
                        end_time=event_data["end_time"],
                        visitor_list=event_data["visitor_list"]
                    ).count()
                except Exception as e:
                    print(str(e))

                if not count:
                    continue

                self.save(event_data["id"], count[0], count[1])

                if config.DEBUG:
                    print("EVENT_ID: {}".format(event_data["id"]))
                    print("BUILDING_ID: {}".format(event_data["building"]))
                    print("ROOM: {}".format(event_data["room"]))
                    print("START_TIME: {}".format(event_data["start_time"]))
                    print("END_TIME: {}".format(event_data["end_time"]))
                    print("VISITORS: {}".format(count[0]))
                    print("VISITOR_LIST: {}".format(count[1]))
                    print("\n{}\n\n".format("-" * 20))

            sleep(config.RECODNIZE_DAEMON_TIMEOUT)

    def save(self, event_id, visitors, visitor_list):
        """
        Store values to DB
        :param event_id:
        :param visitors:
        :param visitor_list:
        :return:
        """
        with DBSession() as session:
            event = session.query(RoomEvent).get(event_id)

            if not event:
                raise Exception("Room event doesn't exists!")

            event.visitors = visitors
            event.visitor_list = ",".join(map(str, visitor_list))
            inspect(event).session.commit()
