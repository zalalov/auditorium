import cv2 as cv

DB_CONNECTION = "postgresql://auditorium:123@localhost/auditorium"

# Threshold
THRESHOLD_TYPE = cv.THRESH_BINARY_INV
THRESHOLD_DEFAULT_VALUE = 100

# Blur
MEDIAN_BLUR_APERTURE_SIZE = 15

# Blob area to exclude nearby points (percents)
BLOB_NEARBY_POINT_AREA = 3

BLOB_FILTER_BY_AREA = True
BLOB_MIN_AREA_DEFAULT_VALUE = 100

BLOB_FILTER_BY_CIRCULARITY = False
BLOB_MIN_CIRCULARITY = 0.1

BLOB_FILTER_BY_CONVEXITY = False
BLOB_MIN_CONVEXITY = 0.87

BLOB_FILTER_BY_INERTIA = False
BLOB_MIN_INTERTIA_RATIO = 0.01

DEBUG = True

# Frame grabber's config
GRAB_DEFAULT_LOGIN = "userlog"
GRAB_DEFAULT_PASSWORD = "l0gin"
GRAB_DAEMON_OUTPUT_DIR = "/tmp/frames/"
GRAB_DAEMON_TIMEOUT = 300
GRAB_DAEMON_RESTART_TIMEOUT = 5

# SHOULD BE DIFFERENT FOR EVERY GRABBER INSTANCE!
GRAB_DAEMON_RESTART_FLAG_PATH = "./grab_restart"

# People recognazing daemon timeout
RECODNIZE_DAEMON_TIMEOUT = 10

# Filepath for hosts
HOSTS_PATH = "./hosts"

# Distributor daemon params
DISTRIBUTOR_HOST = "0.0.0.0"
DISTRIBUTOR_PORT = 9090
DISTRIBUTOR_INCOME_LIMIT = 100
DISTRIBUTOR_CHECK_CONNECTIONS_TIMEOUT = 5
DISTRIBUTOR_HOST_UPDATE_TIMEOUT = 5

# YOLO_REGULAR
DARKFLOW_HOST = "0.0.0.0"
DARKFLOW_PORT = 7777
DARKFLOW_MODEL = "auditorium/components/darkflow/cfg/yolo.cfg"
DARKFLOW_WEIGHTS = "auditorium/components/darkflow/weights/yolo.weights"
DARKFLOW_BIN_PATH = "auditorium/components/darkflow/weights"
DARKFLOW_CFG_PATH = "auditorium/components/darkflow/cfg"
# Frame will be processed by EXISTING_CHECK_THRESHOLD first
# for checking existing persons on frame
# Then if persons > 0, NN with other configuration
# will be executed for getting more accurate result
DARKFLOW_THRESHOLD = .18
DARKFLOW_EXISTING_CHECK_THRESHOLD = .3

# Additional Recognize Options
DARKFLOW_SLICING = True
DARKFLOW_EQUILIZING = False
DARKFLOW_SCALING = False
DARKFLOW_SHARPENING = False

# in case of 70% of frames has 0 persons
# total visitor count will be 0
# for preventing false positive of NN
COUNT_SMOOTHING = False

# Roles
ROLE_DISTRIBUTOR = 100
ROLE_GRABBER = 200
ROLE_RECOGNIZE = 300
ROLE_DARKFLOW = 400

# Roles of current server
CURRENT_ROLES = (
    # ROLE_DISTRIBUTOR,
    # ROLE_GRABBER,
    # ROLE_RECOGNIZE,
    ROLE_DARKFLOW,
)
