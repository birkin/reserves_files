import datetime, json, logging

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from reserves_files_app.lib import version_helper

log = logging.getLogger(__name__)


# ===========================
# main urls
# ===========================


def file_manager( request, course_code: str, file_name: str ):
    log.debug( '\n\nstarting file_manager()' )
    combined = f'{course_code}/{file_name}'
    return HttpResponse( f'file-manager coming for ``{combined}``' )


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
