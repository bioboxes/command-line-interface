# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## v0.6.0 - 2016-02-13

### Added

  * Profiling verify command

## v0.5.2 - 2016-09-23

### Fixed

  * Image verification with `--verbose` returns non-zero exit code if
    verification fails.

## v0.5.1 - 2016-07-28

### Fixed

  * Containers are removed when the --no-rm flag is given as a command line
    argument. A unit-test not run on the CI server is added to ensure this
    works correctly.

  * Switched yaml library to ruamel.yaml which supports python3 and is actively
    maintained. The previous library PyYAML sometimes generated python import
    errors when running on python 3. The underlying bioboxes-py library has
    also made the same switch.

### Changed

  * Simplified the feature tests, removing some redundant scenarios and
    consolidating the existing scenarios so multiple flags can be tested in the
    same scenario.

## v0.5.0 - 2016-07-20

### Changed

  * Implemented support for the changed QUAST interface discussed in [Issue
    194][194].

  * Switched to use biobox.py python library. Many of the functions have been
    extracted to this library. This library also simplifies running biobox
    containers by taking care of where the host directories are mounted into
    the container, and correspondingly updating the mounted biobox.yaml.

[194]: https://github.com/bioboxes/rfc/issues/194

## v0.4.0 - 2016-06-02

### Added

  * Support for python 3. The command line interface is tested against python
    2.7 and 3.4.

  * Support for specifying resource consumption using Docker's cgroup flags.

## v0.3.0 - 2015-11-05

### Added

  * Support for assembler benchmark bioboxes was added to `biobox run` and
    `biobox verify` allowing the use of images such as bioboxes/quast.

  * The `biobox login` was allowing a user to log into a bash prompt in the
    specified image with test data volumes mounted. This feature was added to
    help interactive debugging when creating a biobox.

  * The `biobox verify` command now returns the reason for the failed
    verification. A flag `--verbose` can be used to list the PASS/FAIL status
    for all the verifications explicitly.

  * Containers are automatically removed by default after being run. This saves
    space on the users system by no longer keeping redundant containers around.
    An additional flag `--no-rm` was added to override this and keep
    the container after use.

  * Verify taxonomic binning benchmark container.

  * Verify read based assembly benchmark container.

### Fixed

  * Fixed bug where passing full paths as the input arguments would cause a
    crash. Full paths can now be given.

  * Fixed a bug where trying to validate a non-existent Docker image returned a
    verification failure message to the use instead of correctly informing the
    user the image does not exist.

## v0.2.2 - 2015-08-27

### Added

  * The documentation in `doc` is now much more detailed and contains examples
    on how to use the CLI.

  * A trigger `plumbing/rebuild-website` to rebuild the bioboxes.org website
    when a PR is merged into the master branch.

## v0.2.1 - 2015-08-14

### Fixed

  * A significant bug in the project layout and `setup.py` meant that
    biobox_cli sub modules, the `assets` directory and the `verification`
    directory were included in the `.tar.gz` released file, but not installed.
    This was fixed by moving all files under the `biobox_cli` directory, and
    specifying their inclusion using `find_packages()` and `package_data` in
    the `setup.py` configuration file.

## v0.2.0 - 2015-08-12

### Added

  * Flag specify a task `--task` when using a short read assembler biobox. This
    runs different combinations of parameters according to their specification
    in each biobox `Taskfile`.

  * Ability to specify a task to use when verifying a short read assembler
    biobox. This is passed using the `--task` flag to `biobox verify`.

  * Short read assembler verification now checks that the file `log.txt` is
    created when a directory that is mounted to `/bbx/metadata`.

### Changed

  * Updated README.md with more explicit instructions on how to submit pull
    requests.

### Fixed

  * Bug where bundled files could not be found if install in separate
    directories

## v0.1.0 - 2015-08-10

### Added

  * Added ability to verify a biobox. This is called via the `biobox verify`
    command. This tests the image with the cucumber files in the verification
    directory and returns a pass fail message.

### Changed

  * Now provides git-like syntax where commands are available as `biobox run`
    or `biobox verify`. This compares previously where the first command
    argument was the biobox type.

  * Error messages moved outside the python code and instead stored in a yaml
    file. This allows error messages to instead be called by name from the
    code.

### Fixed

  * More verbose error messages. The user now gets clearer error messages when
    the biobox is not available or the command is called incorrectly.
