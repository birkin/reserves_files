import datetime, json, logging, mimetypes, os, pathlib

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, StreamingHttpResponse
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
    """ Streams file to browser. """
    log.debug( '\n\nstarting file_manager()' )
    filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
    ## check existence ----------------------------------------------
    path_obj = pathlib.Path( filepath )
    if path_obj.is_file() == False:
        return HttpResponseNotFound( f'404 / Not Found' )
    ## check shib ---------------------------------------------------
    shib_info: dict = shib.extract_info( request.META )
    ## check match --------------------------------------------------
    try: 
        Match.objects.get( filename=file_name, course_code=course_code )
    except:
        return HttpResponseNotFound( f'404 / File-Course-Match Not Found' )
    ## all good -----------------------------------------------------
    chunk_size = 512
    response = StreamingHttpResponse(
        FileWrapper( open(filepath, 'rb'), chunk_size ),
        content_type=mimetypes.guess_type(filepath)[0]
        )
    response['Content-Length'] = os.path.getsize(filepath)    
    return response


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


# def file_manager( request, course_code: str, file_name: str ):
#     """ Proof of concept... """
#     log.debug( '\n\nstarting file_manager()' )
#     ## setup --------------------------------------------------------
#     filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
#     chunk_size = 512
#     response = StreamingHttpResponse(
#         FileWrapper( open(filepath, 'rb'), chunk_size ),
#         content_type=mimetypes.guess_type(filepath)[0]
#         )
#     response['Content-Length'] = os.path.getsize(filepath)    
#     return response


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
