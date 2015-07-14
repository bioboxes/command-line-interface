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

### Development Workflow

To contribute changes to this project, fork the repository and create a feature
branch. Once you have pushed your git commits to you forked repository, submit
a pull request. The above scripts should all pass and return a non-zero exit
before a PR will be merged.

[bioboxes]: http://bioboxes.org
