## General guidelines

To contribute, fork the repository and send a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible.

Where appropriate, please provide unit tests or integration tests. Unit tests should be pytest based tests and be added to <project>/tests.

Please make sure all tests pass before submitting a pull request. It is also good if you squash your commits and add the tags #major or #minor to the pull request title if need be, otherwise your pull request will be considered a patch bump. Please check [https://semver.org/](https://semver.org/) for more information about versioning.

## Testing the code locally

To test the code locally you need an environment with QIIME2 installed. Please, look into [QIIME2 documentation](https://docs.qiime2.org/2022.8/install/) to install the latest version for your operating system. After installing QIIME2, you can install the dependencies to test HiTaC with:

```shell
pip install flake8==3.9.2
pip install pytest==6.2.4
pip install pytest-flake8==1.0.7
pip install pydocstyle==6.1.1
pip install pytest-pydocstyle==2.2.0
pip install pytest-cov==2.12.1
pip install pre-commit==2.20.0
pip install -e .
```

To run the tests simply execute:

```shell
pytest -v --flake8 --pydocstyle --cov=hitac --cov-fail-under=75 --cov-report html
```

Lastly, you can set up the git hooks scripts to fix formatting errors locally during commits:

```shell
pre-commit install
```

If black is not executed locally and there are formatting errors, the CI/CD pipeline will fail.
