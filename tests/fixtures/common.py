# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,no-member
# pylint: disable=unused-argument,too-many-arguments,protected-access
import logging
import re

import pytest
from pytest_bdd import parsers, then

# Common fixtures


@pytest.fixture
def context():
    return {}


@then("everything is fine")
def nothing_to_test(context):
    # Just to be safe, make sure context has no error
    assert "error" not in context


@then("something is wrong")
def something_wrong(context):
    assert "error" in context


@then(parsers.parse("there is no {key}"))
def check_no_key(context, key):
    assert key not in context


@then(parsers.parse("the {attribute} is <result>"))
def check_result_bool(context, attribute, result):
    result = result.lower() == "true"
    assert attribute in context and context[attribute] is result


@then(parsers.parse("the {attribute} is True"))
def check_result_true(context, attribute):
    assert attribute in context and context[attribute] is True


@then(parsers.parse("the {attribute} is False"))
def check_result_false(context, attribute):
    assert attribute in context and context[attribute] is False


# negative lookahead to distinguish with the store_map_key_explicit method
@then(parsers.re(r"^the (?P<attribute>\S+) map has attribute (?!.*to store as)(?P<key>.+)$"))
def store_map_key(context, attribute, key):
    assert attribute in context and key in context[attribute]
    context[key] = context[attribute][key]


@then(parsers.parse("the {attribute} map has attribute {key} to store as {store_key}"))
def store_map_key_explicit(context, attribute, key, store_key):
    assert attribute in context and key in context[attribute]
    context[store_key] = context[attribute][key]


@then(parsers.parse("the {attribute} is a list with entry {index:d} to store as {store_key}"))
def store_list_value(context, attribute, index, store_key):
    assert attribute in context and len(context[attribute]) >= index
    context[store_key] = context[attribute][index]


@then(parsers.parse("the {attribute} exit code is {exit_code:d}"))
def check_exit_code(exit_code, context, attribute):
    assert attribute in context and context[attribute].exit_code == exit_code


@then(parsers.parse("the {attribute} exit code is not {exit_code:d}"))
def check_not_exit_code(exit_code, context, attribute):
    assert attribute in context and context[attribute].exit_code != exit_code


@then(parsers.parse("the {attribute} output matches: {message}"))
def check_output(message, context, attribute):
    assert attribute in context and re.match(message, context[attribute])


@then(parsers.parse("the {attribute} is None"))
def assert_result_none(context, attribute):
    assert attribute in context and context[attribute] is None


@then(parsers.parse("the {attribute} is not None"))
def assert_result_not_none(context, attribute):
    assert attribute in context and context[attribute] is not None


@then(parsers.parse("the {attribute} is equal to integer {value:d}"))
def assert_result_int_value(context, attribute, value):
    assert attribute in context and context[attribute] == value


@then(parsers.parse("the {attribute} is equal to string {value}"))
def assert_result_string_value(context, attribute, value):
    assert attribute in context and context[attribute] == value


@then(parsers.parse("the {attribute} length is equal to {length:d}"))
def assert_result_attribute_length(context, attribute, length):
    assert attribute in context and len(context[attribute]) == length


@then(parsers.parse("the {attribute} list values are bytes"))
def assert_result_attribute_list_of_bytes(context, attribute):
    assert attribute in context
    the_list = context[attribute]
    assert len(list(filter(lambda x: isinstance(x, bytes), the_list))) == len(the_list)


@then(parsers.parse("the {attribute} is an empty list"))
def assert_result_empty_list(context, attribute):
    assert attribute in context and context[attribute] == []


@then(parsers.parse("the {attribute} is equal to attribute {other_attribute}"))
def assert_result_attributes_are_equals(context, attribute, other_attribute):
    assert attribute in context and context[attribute] == context[other_attribute]


@then(parsers.parse("the {attribute} type is ValueError"))
def check_result_type_value_error(context, attribute):
    assert attribute in context and isinstance(context.get(attribute, None), ValueError)


@then(parsers.parse("the {attribute} value string contains {value}"))
def check_result_contains_value_string(context, attribute, value):
    assert attribute in context and value in str(context[attribute])


@then(parsers.parse("the logger {logger_name} logged a {level} message: {message}"))
def check_logging_message(caplog, logger_name, level, message):
    assert (logger_name, logging._nameToLevel[level], message) in caplog.record_tuples


@then(parsers.parse("the logger {logger_name} logged nothing"))
def check_no_logging(caplog, logger_name):
    assert len(list(filter(lambda x: x[0] == logger_name, caplog.record_tuples))) == 0
