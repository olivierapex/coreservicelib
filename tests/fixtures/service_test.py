# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,no-member
# pylint: disable=unused-argument,too-many-arguments,protected-access
from pytest_bdd import scenarios, when

scenarios("core_service_lib/service.feature")


@when("Get health")
def service_runner_invoke(context):
    context["result"] = "FIXME"
