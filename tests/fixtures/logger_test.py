# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,no-member
# pylint: disable=unused-argument,too-many-arguments,protected-access, W0703
from pytest_bdd import scenarios, when

from core_service_lib import logger

scenarios("core_service_lib/logger.feature")

@when("I setup a logger")
def setup_logger(context):
    try:
        logger.setup_logger("ALogger", "logger_output_file.log")
        # The second call allow to reach the existing logger case.
        logger.setup_logger("ALogger", "logger_output_file.log")
        context["result"] = "OK"
    except Exception as error:
        context["error"] = error