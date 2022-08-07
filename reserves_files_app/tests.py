import json, logging

from django.conf import settings as project_settings
from django.test import TestCase
from django.test.utils import override_settings
from easyborrow_stats_app.lib.stats_helper import Validator


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class ClientTest( TestCase ):
    """ Checks urls. """

    def test_stats_missing_params(self):
        """ Checks `/stats_api/v2/` with missing params. """
        response = self.client.get( '/stats_api/v2/' )
        self.assertEqual( 400, response.status_code )  # HttpResponseBadRequest()
        resp_dct = json.loads( response.content )
        self.assertEqual(
            'example url: http://127.0.0.1/stats_api/v2/?start_date=2010-01-20&end_date=2010-01-30',  # true for runserver _client_ test (no port)
            resp_dct['response']['message']
            )

    ## removing test for now to avoid legacy-database/testing problem
    # def test_stats_good_params(self):
    #     """ Checks `/stats_api/v2/` with good params. """
    #     response = self.client.get( '/stats_api/v2/?start_date=2010-01-20&end_date=2010-01-30' )
    #     self.assertEqual( 200, response.status_code )

    def test_feed(self):
        """ Checks `/feeds/latest_items/`. """
        response = self.client.get( '/feeds/latest_items/' )
        self.assertEqual( 200, response.status_code )

    @override_settings(DEBUG=True)  # for tests, DEBUG is normally autoset to False
    def test_dev_errorcheck(self):
        """ Checks that dev error_check url triggers error.. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        try:
            log.debug( 'about to initiate client.get()' )
            response = self.client.get( '/error_check/' )
        except Exception as e:
            log.debug( f'e, ``{repr(e)}``' )
            self.assertEqual( "ZeroDivisionError('division by zero')", repr(e) )

    def test_prod_errorcheck(self):
        """ Checks that production error_check url returns 404. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        response = self.client.get( '/error_check/' )
        self.assertEqual( 404, response.status_code )


class ValidatorTest( TestCase ):
    """ Checks stats_helper.py """

    def setUp(self):
        self.validator = Validator()

    def test_params_valid__no_params(self):
        """ Checks params handling; no params sent. """
        params = {}
        self.assertEqual( False, self.validator.validate_params( params ) )
        self.assertEqual( '', self.validator.start_date )
        self.assertEqual( '', self.validator.end_date )

    def test_params_valid__good_params_but_invalid_date(self):
        """ Checks params handling; date sent but invalid. """
        # params = { 'start_date': 'foo', 'end_date': 'bar' }
        params = { 'start_date': ['foo'], 'end_date': ['bar'] }
        self.assertEqual( False, self.validator.validate_params( params ) )
        self.assertEqual( '', self.validator.start_date )
        self.assertEqual( '', self.validator.end_date )

    def test_params_valid__good_params_and_out_of_order_dates(self):
        """ Checks params handling; good dates sent, but out-of-order. """
        params = { 'start_date': ['2020-01-30'], 'end_date': ['2020-01-20'] }
        self.assertEqual( False, self.validator.validate_params( params ) )
        self.assertEqual( '', self.validator.start_date )
        self.assertEqual( '', self.validator.end_date )

    def test_params_valid__good_params_and_good_dates(self):
        """ Checks params handling; all good. """
        params = { 'start_date': ['2020-01-20'], 'end_date': ['2020-01-30'] }
        self.assertEqual( True, self.validator.validate_params( params ) )
        self.assertEqual( ['2020-01-20'], self.validator.start_date )
        self.assertEqual( ['2020-01-30'], self.validator.end_date )
