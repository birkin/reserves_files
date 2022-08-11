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


def authz_check( shib_info: dict, course_code: str ) -> bool:
    shib_is_valid = False
    eppn: str = shib_info['eppn']
    groups: list = shib_info['groups']
    course_code_to_check = course_code.replace( '-', ':' )
    log.debug( f'course_code_to_check' )
    ( eppn_check_ok, staff_check_ok, course_code_check_ok ) = ( False, False, False )
    if eppn[-10:] == '@brown.edu':
        eppn_check_ok = True
    for entry in groups:
        group: str = entry  # for type-annotation
        if settings_app.STAFF_GROUP in group:
            staff_check_ok = True
            break
        if course_code_to_check.lower() in group.lower():
            course_code_check_ok = True
            break
    log.debug( f'eppn_check_ok, ``{eppn_check_ok}``; staff_check_ok, ``{staff_check_ok}``; course_code_check_ok, ``{course_code_check_ok}``' )
    if eppn_check_ok:
        if staff_check_ok or course_code_check_ok:
            shib_is_valid = True
    log.debug( f'shib_is_valid, ``{shib_is_valid}``' )
    return shib_is_valid
    