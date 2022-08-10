import json, logging, os

log = logging.getLogger(__name__)


FILES_DIR_PATH = os.environ['RES_FILES__FILE_DIR_PATH']

LOCALDEV_TEST_META_INFO: dict = json.loads( os.environ['RES_FILES__TEST_META_DCT_JSON'] )
