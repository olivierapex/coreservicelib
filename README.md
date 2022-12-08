# core-service-lib

Flask Wrapper with error management and dynamic routes.
This can be imported in all other microservices using Flask as Framework.

## Development

Please make sure to [install pre-commit](https://pre-commit.com/#quick-start) prior any modification to this module.

The project is configured for development with vscode with remote containers.
Install the latest version of vscode and the extensions `Remote-Containers`
Then open the project folder using the Remote-Containers extension, it will build the docker container and launch it.

### poetry

Start the container in vscode.
TO DO

### dependencies and virtualenv

To install the project dependencies run `poetry install --remove-untracked`
To start a shell run `poetry shell`
To update the dependencies to the latest version (as allowed in `pyproject.toml`) run `poetry update` and commit the file `poetry.lock`

### tests

#### During development

1. Watch all tests on save
Open a terminal window and run `make watcha`
1. Watch all tests in a file on save
*Note*: Add `@current` at the top of the test feature file(s) you are currently working on (but do not commit it).
On every save it will execute all the `@current` tests, if they are successful it will then execute all the unit tests, run flake and pylint.

#### Integration tests

By default integration tests are visible in vscode but they are ignored when `Run All Tests` is executed.
Integration tests can be run one at a time in vscode (one test, not one class).

To run all the integration tests from the console: `pytest -s -m integration`
To run (and debug in vscode) all integration tests, select the launch configuration `Python: Run all integration tests`
To run (and debug in vscode) a single integration test class, open in and select the launch configuration `Python: Test current file`
