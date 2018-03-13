from auditorium.daemon import grabd, recognized, distributord, darkflowd
from auditorium import config

if __name__ == "__main__":
    if config.ROLE_GRABBER in config.CURRENT_ROLES:
        gd = grabd.GrabDaemon()
        gd.start()

    if config.ROLE_RECOGNIZE in config.CURRENT_ROLES:
        rd = recognized.RecognizeDaemon()
        rd.start()

    if config.ROLE_DISTRIBUTOR in config.CURRENT_ROLES:
        dd = distributord.DistributorDaemon()
        dd.start()

    if config.ROLE_DARKFLOW in config.CURRENT_ROLES:
        darkd = darkflowd.DarkflowDaemon()
        darkd.start()

