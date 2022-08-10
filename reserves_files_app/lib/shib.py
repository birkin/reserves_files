import logging, pprint
from reserves_files_app import settings_app

log = logging.getLogger(__name__)


def extract_info( meta_info: dict ) -> dict:
    log.debug( f'meta_info, ``{pprint.pformat(meta_info)}``' )
    host = meta_info.get( 'HTTP_HOST', '' )
    log.debug( f'host, ``{host}``' )
    if host[0:9] == '127.0.0.1':
        meta_info = settings_app.LOCALDEV_TEST_META_INFO
        log.debug( f'updated meta_info, ``{meta_info}``' )
    eppn: str = meta_info.get( 'Shibboleth-eppn', '' )
    grouper_string: str = meta_info.get( 'Shibboleth-isMemberOf', '' )
    groups: list = grouper_string.split( ';' )
    shib_info = { 'eppn': eppn, 'groups': groups }
    return shib_info


def authz_check( shib_info: dict ) -> bool:
    return False