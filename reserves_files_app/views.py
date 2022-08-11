import datetime, json, logging, mimetypes, os, pathlib, pprint

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse
from reserves_files_app import settings_app
from reserves_files_app.lib import shib, version_helper
from reserves_files_app.models import Match
from wsgiref.util import FileWrapper

log = logging.getLogger(__name__)


# ===========================
# main urls
# ===========================


def file_manager( request, course_code: str, file_name: str ):
    """ Manages existence-check, and course-to-file matching, and streams file to browser. """
    log.debug( '\n\nstarting file_manager()' )
    filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
    log.debug( f'filepath, ``{filepath}``' )
    ## check existence ----------------------------------------------
    path_obj = pathlib.Path( filepath )
    if path_obj.is_file() == False:
        log.debug( 'filepath not found' )
        return HttpResponseNotFound( f'404 / Not Found' )
    ## check shib ---------------------------------------------------
    # log.debug( f'request.__dict__, ``{pprint.pformat(request.__dict__)}``' )
    shib_info: dict = shib.extract_info( request.META )  # contains eppn (str) and groups (list)
    shib_valid: bool = shib.authz_check( shib_info, course_code )
    if shib_valid == False:
        return HttpResponseForbidden( f'403 / Forbidden. If you believe you should be able to view reserves-files for the class "{course_code}", contact X.' )
    ## check match --------------------------------------------------
    try: 
        Match.objects.get( filename=file_name, course_code=course_code )
    except:
        log.debug( f'no db entry found for course_code, ``{course_code}`` and file_name, ``{file_name}``' )
        return HttpResponseNotFound( f'404 / File-Course-Match Not Found' )
    ## all good -----------------------------------------------------
    log.debug( f'all good; about to stream response' )
    chunk_size = 512
    response = StreamingHttpResponse(
        FileWrapper( open(filepath, 'rb'), chunk_size ),
        content_type=mimetypes.guess_type(filepath)[0]
        )
    response['Content-Length'] = os.path.getsize(filepath)    
    return response

    ## end def file_manager()


# def file_manager( request, course_code: str, file_name: str ):
#     """ Streams file to browser. """
#     log.debug( '\n\nstarting file_manager()' )
#     filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
#     ## check existence ----------------------------------------------
#     path_obj = pathlib.Path( filepath )
#     if path_obj.is_file() == False:
#         return HttpResponseNotFound( f'404 / Not Found' )
#     ## all good -----------------------------------------------------
#     chunk_size = 512
#     response = StreamingHttpResponse(
#         FileWrapper( open(filepath, 'rb'), chunk_size ),
#         content_type=mimetypes.guess_type(filepath)[0]
#         )
#     response['Content-Length'] = os.path.getsize(filepath)    
#     return response


def adder( request ):
    """ Manages adding a match-entry. """
    log.debug( '\n\nstarting adder()' )
    ## check for POST -----------------------------------------------
    if request.method != 'POST':
        log.debug( 'invalid, not POST' )
        return HttpResponseBadRequest( '400 / Bad Request' )
    ## check POST params --------------------------------------------
    course_code = request.POST.get( 'course_code', '' )
    file_name = request.POST.get( 'file_name', '' )
    token = request.POST.get( 'token', '' )
    params_good = False
    course_code_param_good = False if course_code == '' else True
    file_name_param_good = False if file_name == '' else True
    token_param_good = False if token == '' else True
    log.debug( f'course_code_param_good, ``{course_code_param_good}``; file_name_param_good, ``{file_name_param_good}`` ' )
    if course_code_param_good == False or file_name_param_good == False or token_param_good == False:
        log.debug( 'invalid, bad param' )
        return HttpResponseBadRequest( '400 / Bad Request' )
    ## check token --------------------------------------------------
    token_good = False
    incoming_token: str = request.POST['token']
    incoming_ip: str = request.META.get('REMOTE_ADDR', '')
    log.debug( f'incoming_token, ``{incoming_token}``; incoming_ip, ``{incoming_ip}``' )
    legit_adders: list = settings_app.LEGIT_ADDERS
    for entry in legit_adders:
        adder: dict = entry
        legit_token: str = adder['token']
        legit_ip: str = adder['ip']
        if incoming_token == legit_token and incoming_ip == legit_ip:
            token_good = True
            break
    log.debug( f'token_good, ``{token_good}``' )
    if token_good == False:
        return HttpResponseBadRequest( '400 / Bad Request' )
    ## check that file exists ---------------------------------------
    filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
    log.debug( f'filepath, ``{filepath}``' )
    path_obj = pathlib.Path( filepath )
    if path_obj.is_file() == False:
        log.debug( 'filepath not found' )
        return HttpResponseBadRequest( '400 / Bad Request' )
    ## add match ----------------------------------------------------
    from reserves_files_app.models import Match
    match = Match()
    match.course_code = course_code
    match.filename = file_name
    match.save()
    log.debug( 'save successful' )
    return HttpResponse( '200 / OK' )

    ## end def adder()


def info( request ):
    return HttpResponse( 'Hello, world. You\'re at the info page.' )


# ===========================
# support urls
# ===========================


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development)...
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug( f'project_settings.DEBUG, ``{project_settings.DEBUG}``' )
    if project_settings.DEBUG == True:
        log.debug( 'triggering exception' )
        raise Exception( 'Raising intentional exception.' )
    else:
        log.debug( 'returing 404' )
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


def root( request ):
    return HttpResponseRedirect( reverse('info_url') )


def version( request ):
    """ Returns basic branch and commit data. """
    rq_now = datetime.datetime.now()
    commit = version_helper.get_commit()
    branch = version_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    context = version_helper.make_context( request, rq_now, info_txt )
    output = json.dumps( context, sort_keys=True, indent=2 )
    log.debug( f'output, ``{output}``' )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )
