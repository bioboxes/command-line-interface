## Biobox command line interface

This repository contains the code for building the [bioboxes][] command line
interface. This allows a user to run bioboxes in the shell using Docker as the
backend. Documentation is provided in the `doc` folder.

### Development Scripts

The folder `script` provides a series of scripts to help developers and also
used by the continuous integration server. These scripts should be used in the
following order:

  * `script/bootstrap`: Install required python libraries using virtual env and
    pull Docker images necessary for testing.
  * `script/test`: Runs python unit tests. These can be found in the `test`
    directory.
  * `script/build`: Tests whether the project builds and installs as a python
    package. The package is installed in a Docker container as not to affect
    the user's system
  * `script/feature`: Tests the tool against several different user scenarios.
    These scenarios are described in `features`.

### Submitting pull requests

Contributing fixes or new features is welcome. For anything more than small bug
fixes please [open an issue on github][ghi] beforehand to discuss what you
intend to implement. This can help prevent time being wasted should the
situation occur that your pull request is not immediately accepted.

To contribute changes to this project, fork the repository and create a feature
branch. Once you have pushed your git commits to you forked repository, submit
a pull request. A pull request should include the following:

  * Add a new entry to the CHANGELOG.md and update `biobox_cli/version.py`.
    Please follow [semantic versioning][semver] when updating the version
    number.
  * Update the documentation in `doc` if the interface is changed.
  * Add new feature tests in `feature` if new functionality is added. This will
    prevent them being broken in future development.
  * Ensure the following scripts pass: `script/test`, `script/build` and
    `script/feature`

[ghi]: https://github.com/bioboxes/command-line-interface/issues
[semver]: http://semver.org
[bioboxes]: http://bioboxes.org
