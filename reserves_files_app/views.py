import datetime, json, logging

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from easyborrow_stats_app.lib import version_helper
from easyborrow_stats_app.lib.stats_helper import Validator, Prepper

log = logging.getLogger(__name__)


# ===========================
# main urls
# ===========================


def root( request ):
    return HttpResponseRedirect( reverse('info_url') )


def info( request ):
    return HttpResponse( 'Hello, world. You\'re at the info page.' )


def stats( request ):
    log.debug( '\n\nstarting stats()' )
    request_now_time = datetime.datetime.now()
    validator = Validator()
    prepper = Prepper()
    params_valid = validator.validate_params( dict(request.GET) )
    assert type( params_valid ) == bool
    if params_valid:
        data = prepper.make_data( request.GET['start_date'], request.GET['end_date'] )
        # resp = HttpResponse( 'stats response coming' )
        resp = HttpResponse( data, content_type='application/json; charset=utf-8' )
    else:
        host = request.META.get( 'HTTP_HOST', '127.0.0.1' )  # HTTP_HOST doesn't exist for client-tests
        path = request.META.get('REQUEST_URI', request.META['PATH_INFO'] )
        message = validator.build_bad_param_message( request_now_time, request.scheme, host, path, request.META['QUERY_STRING'] )
        assert type(message) == str
        resp = HttpResponseBadRequest( message, content_type='application/json; charset=utf-8' )
    return resp


def feed( request ):
    return HttpResponse( 'feed response coming' )


# ===========================
# support urls
# ===========================


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
