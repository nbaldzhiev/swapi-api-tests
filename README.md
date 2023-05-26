# Star Wars API Tests

A repository containing API Tests, written in Python + pytest, for the [Star Wars API](https://swapi.dev/).

## Running tests

You can run the tests in two main ways: locally via Docker or via GitHub Actions.

### Locally via Docker

Simply clone the repository (and checkout to the correct branch) and run:

    $ ./test.sh

### GitHub Actions (CI)

-   [run-all-tests.yml](https://github.com/qredo-external/qa-nenko-baldzhiev/blob/nb/solution/.github/workflows/run-all-tests.yml) - Runs all tests upon manual trigger (`workflow_dispatch`);

An Allure HTML report is generated and uploaded as a workflow artifact. This HTML report can then be served to an HTML server; for instance, it can be sent to a AWS S3 bucket with enabled static website hosting.

> **_NOTE:_** You need to be a repository collaborator in order to run the workflow.

### Tests Location

Tests are located in the `tests/api/` package:

-   `test_miscellaneous.py` - contains miscellaneous tests for the SWAPI;
-   `test_people.py` - contains tests for the /people endpoint;
-   `test_planets.py` - contains tests for the /planets endpoint;
-   `test_starships.py` - contains tests for the /starships endpoint;
-   `test_vehicles.py` - contains tests for the /vehicles endpoint.
