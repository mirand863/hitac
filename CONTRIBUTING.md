## General guidelines

To contribute, fork the repository and send a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible.

Where appropriate, please provide unit tests or integration tests. Unit tests should be pytest based tests and be added to <project>/tests.

Please make sure all tests pass before submitting a pull request. It is also good if you squash your commits and add the tags #major or #minor to the pull request title if need be, otherwise your pull request will be considered a patch bump. Please check [https://semver.org/](https://semver.org/) for more information about versioning.

## Testing the code locally

To test the code locally you need to install the dependencies for the library in the current environment. Additionally, you need to install the following dependencies for testing:

```shell
pip install coverage==5.5
pip install flake8==3.9.2
pip install iniconfig==1.1.1
pip install mccabe==0.6.1
pip install packaging==21.0
pip install pluggy==0.13.1
pip install py==1.10.0
pip install pycodestyle==2.7.0
pip install pydocstyle==6.1.1
pip install pyflakes==2.3.1
pip install pyparsing==2.4.7
pip install pytest==6.2.4
pip install pytest-cov==2.12.1
pip install pytest-flake8==1.0.7
pip install pytest-pydocstyle==2.2.0
pip install snowballstemmer==2.1.0
pip install toml==0.10.2
```

To run the tests simply execute:

```shell
pytest -v --flake8 --pydocstyle --cov=hitac --cov-fail-under=75 --cov-report html
```
