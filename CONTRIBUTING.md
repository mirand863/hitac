## General guidelines

To contribute, fork the repository and send a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible.

Where appropriate, please provide unit tests or integration tests. Unit tests should be pytest based tests and be added to <project>/tests.

Please make sure all tests pass before submitting a pull request. It is also good if you squash your commits and add the tags #major or #minor to the pull request title if need be, otherwise your pull request will be considered a patch bump. Please check [https://semver.org/](https://semver.org/) for more information about versioning.

## Testing the code locally

To test the code locally you need an environment with QIIME2 installed. Please, look into [QIIME2 documentation](https://docs.qiime2.org/2022.8/install/) to install the latest version for your operating system. After installing QIIME2, you can install the dependencies to test HiTaC with:

```shell
pip install -e ".[dev]"
```

To run the tests simply execute:

```shell
flake8 hitac tests
pydocstyle hitac
pytest -v --cov=hitac --cov-fail-under=70 --cov-report html
```

Lastly, you can set up the git hooks scripts to fix formatting errors locally during commits:

```shell
pre-commit install
```

If black is not executed locally and there are formatting errors, the CI/CD pipeline will fail.
