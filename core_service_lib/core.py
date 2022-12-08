#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" Core Module """

import sys
from functools import partial, update_wrapper

from flask import Flask, Response, abort, jsonify, request

from core_service_lib import config, logger


class CustomResponse(Response):
    # pylint: disable=too-many-ancestors
    """ Response class to make our flask respond follow a standard. """
    charset = "utf-8"
    default_status = 200
    default_mimetype = "application/json"

    def __init__(  # pylint: disable=E0101, R0913, R1725
        self, response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False
    ):
        return super(CustomResponse, self).__init__(response)

    @classmethod
    def force_type(cls, rv, environ=None):
        # pylint: disable=W0221
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(CustomResponse, cls).force_type(rv, environ)


class Core(Flask):
    """ Core Class that will interact directly with Flask Framework. """

    def __init__(self, app_name, config_file_path):
        """ To initiate Core, we need to give him config file path. """
        Flask.__init__(self, app_name)
        Flask.response_class = CustomResponse
        self.__set_error_handler()
        self.set_conf = config.Conf(config_file_path)
        self.set_logger = logger.setup_logger("logger", self.conf.log_info["path"], self.conf.log_info["level"])

    def __set_error_handler(self):
        """ Error handling with details and logger. """

        @self.errorhandler(404)
        def not_found(error):
            # pylint: disable=W0612
            self.logger.warning(
                "HTTP 404, The IP : %s  is trying to access : %s but doesnt exist.",
                self.connection_ip,
                self.full_url_path,
            )
            return jsonify({"ERROR": 404, "Message": str(error)}), 404

        @self.errorhandler(400)
        def bad(error):
            # pylint: disable=W0612
            self.logger.warning(
                "HTTP 400, The IP : %s is trying to access : %s . ARGS : %s  HEADERS : %s",
                self.connection_ip,
                self.full_url_path,
                self.request_args,
                self.request_headers,
            )
            return jsonify({"ERROR": 400, "Message": str(error)}), 400

        @self.errorhandler(405)
        def method_not_allowed(error):
            # pylint: disable=W0612
            self.logger.warning(
                "HTTP 405, The IP : %s  is trying to access : %s  Using HTTP Method : %s",
                self.connection_ip,
                self.full_url_path,
                self.request_method,
            )
            return (
                jsonify({"ERROR": 405, "Message": str(error) + "Please use the proper HTTP Method for the function."}),
                405,
            )

        @self.errorhandler(500)
        def internal(error):
            # pylint: disable=W0612
            self.logger.error(str(error))  # to be implemented with maybe try except.
            return jsonify({"ERROR": 500, "Message": str(error)}), 500

        @self.errorhandler(503)
        def service_unvalaible(error):
            # pylint: disable=W0612
            self.logger.error(str(error))  # to be implemented with maybe try except.
            return (
                jsonify(
                    {
                        "ERROR": 503,
                        "Message": str(error)
                        + "A dependancy of this API is unvailable, please contact your administrator.",
                    }
                ),
                503,
            )

    def __decode_data(self, data):
        """ Return decoded UTF8 data from anything, I guess. """
        try:
            return data.decode("utf8")
        except (TypeError, AttributeError):
            return None
        except Exception as error:
            self.logger.exception("Impossible to Decode data to utf8 : %s", str(error))
            return None

    @staticmethod
    def compose(deco, apply_obj):
        """ Static method to create custom decorator for flask routes. """
        return lambda *args, **kwargs: deco(apply_obj(*args, **kwargs))

    @property
    def conf(self):
        """ Property return configuration properties from the conf file. """
        return self.set_conf

    @property
    def logger(self):
        # pylint: disable=W0236
        """ Property return logger wrapper object class. """
        return self.set_logger

    @property
    def request_data(self):
        """ Property return HTTP request Data. """
        return self.__decode_data(request.data)

    @property
    def request_args(self):
        """ Property return HTTP url arg variables. EG: ...?ma_var=bob . """
        return request.args.to_dict()

    @property
    def request_headers(
        self,
    ):  # We are not parsing it as a dict, because it's using a special class named EnvironHeaders.
        # You can make a .get() on it.
        """ Property return Request Headers. """
        return request.headers

    @property
    def request_method(self):
        """ Property return HTTP Method. EG: POST, GET . """
        return request.method

    @property
    def connection_ip(self):
        """ Property return requester IP. """
        return request.remote_addr

    @property
    def full_url_path(self):
        """ Property returning full url request path. """
        return request.url_root + request.full_path

    @property
    def abort(self):
        """ Property returning flask abort function. """
        return abort

    def route(self, rule, **options):
        # pylint disable=E731
        """ Simple lambda to build and standard/custom Flask route. """
        apply_self = lambda f: update_wrapper(partial(f, self=None), f)
        decorator = Flask.route(self, rule, **options)
        return self.compose(decorator, apply_self)


def run(config_file_path):
    """ Returning Core object with app data. """
    api = Core(app_name=__name__, config_file_path=config_file_path)
    api.run(host=api.conf.host_ip)
    return api


if __name__ == "__main__":
    wsgi_app = run(sys.argv[1])
