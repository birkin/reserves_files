"""
Contains support functions for views.adder()
"""

import logging, pprint

log = logging.getLogger(__name__)


# def check_post_params( post_request_obj: dict ): 
#     log.debug( f'post_request_obj, ``{pprint.pformat(post_request_obj)}``' )
#     course_code = post_request_obj.get( 'course_code', '' )
#     file_name = post_request_obj.get( 'file_name', '' )
#     token = post_request_obj.get( 'token', '' )
#     params_good = False
#     course_code_param_good = False if course_code == '' else True
#     file_name_param_good = False if file_name == '' else True
#     token_param_good = False if token == '' else True
#     post_params_check = {
#         'course_code_param_good': course_code_param_good,
#         'file_name_param_good': file_name_param_good,
#         'token_param_good': token_param_good
#     }
#     log.debug( f'post_params_check, ``{pprint.pformat(post_params_check)}``' )
#     return post_params_check


# def check_post_params( post_request_obj ) -> dict:
#     log.debug( f'post_request_obj, ``{pprint.pformat(post_request_obj)}``' )
#     course_code = post_request_obj.get( 'course_code', '' )
#     file_name = post_request_obj.get( 'file_name', '' )
#     token = post_request_obj.get( 'token', '' )
#     params_good = False
#     course_code_param_good = False if course_code == '' else True
#     file_name_param_good = False if file_name == '' else True
#     token_param_good = False if token == '' else True
#     post_params_check = {
#         'course_code_param_good': course_code_param_good,
#         'file_name_param_good': file_name_param_good,
#         'token_param_good': token_param_good
#     }
#     log.debug( f'post_params_check, ``{pprint.pformat(post_params_check)}``' )
#     return post_params_check
