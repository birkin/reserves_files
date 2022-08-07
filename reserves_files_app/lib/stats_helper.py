import datetime, json, logging, pprint

from django.urls import reverse
from easyborrow_stats_app.models import HistoryEntry, RequestEntry


log = logging.getLogger(__name__)


class Prepper():
    """ Prepares data. """

    def __init__( self ):
        self.date_start = None
        self.date_end = None

    def make_data( self, start_param, end_param ):
        try:
            log.debug( 'starting make_data()' )

            ## get processed history entries ------------------------
            assert type(start_param) == str
            assert type(end_param) == str
            self.date_start = f'{start_param} 00:00:00'
            self.date_end = f'{end_param} 23:59:59'
            log.debug( f'self.date_start, ``{self.date_start}``')
            log.debug( f'self.date_end, ``{self.date_end}``')
            hist_ents = HistoryEntry.objects.using('ezborrow_legacy').filter(
                    working_timestamp__gte=self.date_start).filter(
                    working_timestamp__lte=self.date_end).filter(
                    svc_result__iexact=u'request_successful'
                ).order_by('working_timestamp')
            log.debug( f'len(hist_ents), ``{len(hist_ents)}``' )
            # for hist_ent in hist_ents:
            #     log.debug( f'hist_ent.working_timestamp, ``{hist_ent.working_timestamp}``')

            ## get history-entry counts by service-name -------------
            disposition_dict = {}
            distinct_service_names = hist_ents.values( 'svc_name' ).order_by('svc_name').distinct()
            for entry in distinct_service_names:
                key = entry['svc_name']
                value = hist_ents.filter(svc_name=key).count()
                disposition_dict[key] = value

            ## get requests entries ---------------------------------
            requests = RequestEntry.objects.using('ezborrow_legacy').filter(
                created__gte=self.date_start).filter(
                created__lte=self.date_end
                )
            requests_total = requests.count()

            ## get relevant request-entry counts --------------------
            distinct_status_names = {}
            dispositional_request_statuses = [
                'cancelled',
                'illiad_block_user_em',
                'illiad_block_user_emailed',
                'in josiah',
                'in_josiah',
                'in_josiah_via_isbn',
                'in_josiah_via_oclc',
                'manually_processed'
                ]
            dispositions_all_total = 0
            distinct_status_names_qset = requests.values( u'request_status' ).order_by(u'request_status').distinct()
            for entry in distinct_status_names_qset:
                log.debug( f'entry, ``{entry}``' )
                log.debug( f'type(entry), ``{type(entry)}``' )
                key = entry['request_status']
                value = requests.filter(request_status=key).count()
                distinct_status_names[key] = value
                if key in dispositional_request_statuses:
                    disposition_dict[key] = value
            for count in disposition_dict.values():
                dispositions_all_total += count

            ## build response ---------------------------------------
            output = self.build_response( dispositions_all_total, disposition_dict )
            return output
        except Exception as e:
            msg = f'problem preparing data, ``{repr(e)}``'
            log.exception( msg )
            raise Exception( msg )

        ## end def make_data()

    def build_response( self, dispositions_all_total, disposition_dict ):
        output_dict = { u'request': {}, u'response': {} }
        output_dict['request'] = {
            'date_begin': self.date_start,
            'date_end': self.date_end
            }
        if dispositions_all_total == 0:
            output_dict['response'] = 'no data found for period'
            output = json.dumps( output_dict, sort_keys=True, indent=2 )
            return output
        output_dict[u'response'] = {
            'disposition': disposition_dict,
            'disposition_total': dispositions_all_total,
            }
        # if self.detail == 'yes':
        #     output_dict['response']['xtra'] = {
        #         'request_statuses_found': self.distinct_status_names,
        #         'request_statuses_counted': self.dispositional_request_statuses,
        #         'requests_total': self.requests_total,
        #         }
        output = json.dumps( output_dict, indent=2 )
        log.debug( f'output, ``{pprint.pformat(output)}``' )
        return output

    ## end Prepper()



class Validator():
    """ Checks params & handles bad request. """

    def __init__( self ):
        self.start_date = ''
        self.end_date = ''

    def validate_params( self, params ):
        """ Checks for proper parameters & updates dates
            Called by views.stats() """
        log.debug( f'starting validate_request()' )
        log.debug( f'params, ``{params}``; type(params), ``{type(params)}``' )
        assert type(params) == dict
        params_valid = False
        if 'start_date' in params.keys() and 'end_date' in params.keys():
            if self.good_date( params['start_date'] ) and self.good_date( params['end_date'] ):
                if self.date_order_ok( params['start_date'], params['end_date'] ):
                    self.start_date = params['start_date']
                    self.end_date = params['end_date']
                    params_valid = True
        log.debug( f'params_valid, ``{params_valid}``' )
        return params_valid

    def good_date( self, submitted_param ):
        """ Checks for valid date.
            Called by validate_params() """
        assert type(submitted_param) == list, type(submitted_param)
        submitted_date = submitted_param[0]
        assert type(submitted_date) == str, type(submitted_date)
        is_good_date = False
        try:
            datetime_obj = datetime.datetime.strptime( submitted_date, '%Y-%m-%d' )
            assert type(datetime_obj) == datetime.datetime
            is_good_date = True
        except:
            log.exception( 'problem with date; processing continues' )
        log.debug( f'is_good_date, ``{is_good_date}``' )
        return is_good_date

    def date_order_ok( self, start_param, end_param ):
        """ Ensures start-date is less than end-date.
            Called by validate_params() """
        assert type(start_param) == list
        assert type(end_param) == list
        start_str = start_param[0]
        end_str = end_param[0]
        assert type(start_str) == str
        assert type(end_str) == str
        order_ok = False
        start_dt_obj = datetime.datetime.strptime( start_str, '%Y-%m-%d' )
        end_dt_obj = datetime.datetime.strptime( end_str, '%Y-%m-%d' )
        if start_dt_obj <= end_dt_obj:
            order_ok = True
        log.debug( f'order_ok, ``{order_ok}``' )
        return order_ok

    def build_bad_param_message( self, request_now_time, scheme, host, path, querystring ):
        """ Builds helpful bad-param text.
            Called by views.stats() """
        log.debug( f'scheme, ``{scheme}``; host, ``{host}``; path, ``{path}``; querystring, ``{querystring}``' )
        log.debug( f'reverse("stats_api_v2_url"), ``{reverse("stats_api_v2_url")}``' )
        assert type(request_now_time) == datetime.datetime
        assert type(scheme) == str, type(scheme)
        assert type(host) == str, type(host)
        assert type(path) == str, type(path)
        assert type(querystring) == str, type(querystring)
        if querystring:
            submitted_url = f'{scheme}://{host}{path}?{querystring}'
        else:
            submitted_url = f'{scheme}://{host}{path}'
        log.debug( f'submitted_url, ``{submitted_url}``' )
        data = {
            'request': {
                'url': submitted_url,
                'timestamp': str( request_now_time )
            },
            'response': {
                'status': '400 / Bad Request',
                'message': f'example url: {scheme}://{host}{path}?start_date=2010-01-20&end_date=2010-01-30',
                'timetaken': str( datetime.datetime.now() - request_now_time )
            }
        }
        jsn = json.dumps( data, sort_keys=True, indent=2 )
        log.debug( f'jsn, ``{jsn}``' )
        return jsn

    ## end class Validator()
