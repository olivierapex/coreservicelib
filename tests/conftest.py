# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,no-member
# pylint: disable=unused-argument,too-many-arguments,protected-access

pytest_plugins = ["tests.fixtures.common"]

# pytest callbacks
def pytest_collection_modifyitems(items, config):
    # If running a single test, or collecting tests don't interfere
    if len(items) == 1 or "--collect-only" in config.invocation_params.args:
        return

    for item in items:
        if "integration" not in [mark.name for mark in item.iter_markers()]:
            item.add_marker("unit")

    # Ensure the 'unit' marker is always selected unless 'integration' is
    markexpr = config.getoption("markexpr", "False")
    if len(markexpr) == 0:
        config.option.markexpr = "unit"
    elif "integration" not in markexpr:
        config.option.markexpr = "unit and (%s)" % markexpr


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    # option_value = vars(metafunc.config.option).get("password", None)
    # if "password" in metafunc.fixturenames and option_value is not None:
    #     option_value = base64.b64decode(option_value).decode()
    #     metafunc.parametrize("password", [option_value])
    pass
