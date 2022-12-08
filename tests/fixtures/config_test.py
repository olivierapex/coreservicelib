# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,no-member
# pylint: disable=unused-argument,too-many-arguments,protected-access, W0703
from pytest_bdd import scenarios, when

from core_service_lib.config import Conf

scenarios("core_service_lib/config.feature")
GOOD_CONFIG_FILE = "./tests/config.yaml.good"
BAD_CONFIG_FILE = "./tests/config.yaml.bad"


@when("I set good config")
def create_with_good_file(context):
    try:
        Conf(GOOD_CONFIG_FILE)
        context["result"] = "OK"
    except Exception as error:
        context["error"] = error


@when("I set bad config")
def create_with_bad_file(context):
    try:
        Conf("./doesnt-exist-file")
        context["result"] = "NOK"
    except Exception as error:
        context["error"] = error


@when("I get log with good config file")
def get_log_with_good_file(context):
    try:
        conf = Conf(GOOD_CONFIG_FILE)
        log = conf.log_info
        if log:
            context["result"] = "OK"
        else:
            context["error"] = "log doesn't exist"
    except Exception as error:
        context["error"] = error


@when("I get log with bad config file")
def get_log_with_bad_file(context):
    try:
        conf = Conf(BAD_CONFIG_FILE)
        log = conf.log_info
        if not log:
            context["result"] = "OK"
        else:
            context["error"] = "log doesn't exist"
    except Exception as error:
        context["error"] = error


@when("I get host_ip with good config file")
def get_host_ip_with_good_file(context):
    try:
        conf = Conf(GOOD_CONFIG_FILE)
        host_ip = conf.host_ip
        if host_ip:
            context["result"] = "OK"
        else:
            context["error"] = "host_ip doesn't exist"
    except Exception as error:
        context["error"] = error


@when("I get host_ip with bad config file")
def get_host_ip_with_bad_file(context):
    try:
        conf = Conf(BAD_CONFIG_FILE)
        host_ip = conf.host_ip
        if not host_ip:
            context["result"] = "OK"
        else:
            context["error"] = "host_ip doesn't exist"
    except Exception as error:
        context["error"] = error
