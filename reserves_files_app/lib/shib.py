import logging, pprint

log = logging.getLogger(__name__)


def extract_info( meta_info: dict ) -> dict:
    log.debug( f'meta_info, ``{pprint.pformat(meta_info)}``' )
    shib_info = {}
    return shib_info