import datetime, json, logging, mimetypes, os

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse
from reserves_files_app import settings_app
from reserves_files_app.lib import version_helper
from wsgiref.util import FileWrapper

log = logging.getLogger(__name__)


# ===========================
# main urls
# ===========================


def file_manager( request, course_code: str, file_name: str ):
    """ Proof of concept... """
    log.debug( '\n\nstarting file_manager()' )
    ## setup --------------------------------------------------------
    filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
    chunk_size = 512
    response = StreamingHttpResponse(
        FileWrapper( open(filepath, 'rb'), chunk_size ),
        content_type=mimetypes.guess_type(filepath)[0]
        )
    response['Content-Length'] = os.path.getsize(filepath)    
    return response


# def file_manager( request, course_code: str, file_name: str ):
#     """ Proof of concept... """
#     log.debug( '\n\nstarting file_manager()' )
#     ## setup --------------------------------------------------------
#     filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
#     chunk_size = 512
#     guessed_mimetype = 'application/pdf'
#     guessed_mimetypes: tuple = mimetypes.guess_type(filepath)  # eg ('application/pdf', None)
#     log.debug( f'type(guessed_mimetypes), ``{type(guessed_mimetypes)}``' )
#     log.debug( f'guessed_mimetypes, ``{guessed_mimetypes}``' )
#     if guessed_mimetypes[0]:
#         guessed_mimetype: str = guessed_mimetypes[0]
#     log.debug( f'guessed_mimetype, ``{guessed_mimetype}``' )
#     content_size: int = os.path.getsize( filepath )
#     ## the response -------------------------------------------------
#     response = StreamingHttpResponse(
#         FileWrapper( open(filepath, 'rb'), chunk_size ),
#         content_type=guessed_mimetype
#         )
#     response['Content-Length'] = content_size    
#     return response


# def file_manager( request, course_code: str, file_name: str ):
#     """ Proof of concept... """
#     log.debug( '\n\nstarting file_manager()' )
#     # filepath = f'{settings_app.FILES_DIR_PATH}/{course_code}/{file_name}/'
#     filepath = f'{settings_app.FILES_DIR_PATH}/{file_name}'
#     log.debug( f'filepath, ``{filepath}``' )
#     def file_iterator( path: str, chunk_size=512 ):
#         print( 'hereA' )
#         with open( path, 'rb' ) as f:
#             while True:
#                 c = f.read(chunk_size)
#                 if c:
#                     yield c
#                 else:
#                     break
#         f.close()
#     response = StreamingHttpResponse( file_iterator(filepath) )
#     response['Content-Type'] = 'application/pdf'
#     # response['Content-Type'] = 'application/octet-stream'
#     # except:
#     #     log.exception( 'problem with request; see logs' )
#     #     response = HttpResponseNotFound( 'z404 / Not Found' )
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
