#!/bin/bash


## LOCALDEV settings for django `reserves_files_project`
##
## This file is loaded by `env/bin/activate` when running locally...
## ...and by `project/config/passenger_wsgi.py` on our servers.
##
## When deploying on our servers, copy this file to the appropriate place, edit it, 
## ...and point to it from activate and the apache <Location> entry.


## ============================================================================
## standard project-level settings
## ============================================================================

export RES_FILES__SECRET_KEY="example_secret_key"

export RES_FILES__DEBUG_JSON="true"

export RES_FILES__ADMINS_JSON='
    [
      [
        "exampleFirst exampleLast",
        "example@domain.edu"
      ]
    ]
    '

export RES_FILES__ALLOWED_HOSTS='["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "localhost:8000"]'  # must be json

export RES_FILES__DATABASES_JSON='
    {
      "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "HOST": "",
        "NAME": "../DB/dj_res_files.sqlite3",
        "PASSWORD": "",
        "PORT": "",
        "USER": ""
      }
    }
    '

export RES_FILES__STATIC_URL="/static/"
export RES_FILES__STATIC_ROOT="/static/"

export RES_FILES__EMAIL_HOST="localhost"  
export RES_FILES__EMAIL_PORT="1026"  # will be converted to int in settings.py
export RES_FILES__SERVER_EMAIL="donotreply_reserves-files-project@domain.edu"

export RES_FILES__LOG_PATH="../logs/reserves_files.log"
export RES_FILES__LOG_LEVEL="DEBUG"

export RES_FILES__CSRF_TRUSTED_ORIGINS_JSON='["localhost", "127.0.0.1"]'

## https://docs.djangoproject.com/en/1.11/topics/cache/
## - TIMEOUT is in seconds (0 means don't cache); CULL_FREQUENCY defaults to one-third
export RES_FILES__CACHES_JSON='
{
  "default": {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": "../cache_dir",
    "TIMEOUT": 0,
    "OPTIONS": {
        "MAX_ENTRIES": 1000
    }
  }
}
'

## ============================================================================
## app
## ============================================================================

export RES_FILES__README_URL="https://github.com/birkin/reserves_files_project/blob/main/README.md"

export RES_FILES__FILE_DIR_PATH="../files"

## auth -------------------------------------------------------------

export RES_FILES__SUPER_USERS_JSON='[
]'

export RES_FILES__STAFF_USERS_JSON='
[
  "eppn@domain.edu"
]'

export RES_FILES__STAFF_GROUP="admin_editors"

export RES_FILES__TEST_META_DCT_JSON='{
  "Shibboleth-eppn": "eppn@domain.edu",
  "Shibboleth-brownNetId": "First_Last",
  "Shibboleth-mail": "first_last@domain.edu",
  "Shibboleth-givenName": "First",
  "Shibboleth-sn": "Last",
  "Shibboleth-isMemberOf": "aa:bb:cc;dd:ee:ff;gg:hh;ii",
}'

export RES_FILES__LOGIN_PROBLEM_EMAIL="reserves_files_problems@domain.edu"

## basic auth -------------------------------------------------------

export RES_FILES__BROWSE_USERPASS_JSON='[
  { "example_username": "example_password" }
]'

## end --------------------------------------------------------------
