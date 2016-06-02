# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## [v0.3.0] - 2015-11-05

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

## [v0.2.2] - 2015-08-27

### Added

  * The documentation in `doc` is now much more detailed and contains examples
    on how to use the CLI.

  * A trigger `plumbing/rebuild-website` to rebuild the bioboxes.org website
    when a PR is merged into the master branch.

## [v0.2.1] - 2015-08-14

### Fixed

  * A significant bug in the project layout and `setup.py` meant that
    biobox_cli sub modules, the `assets` directory and the `verification`
    directory were included in the `.tar.gz` released file, but not installed.
    This was fixed by moving all files under the `biobox_cli` directory, and
    specifying their inclusion using `find_packages()` and `package_data` in
    the `setup.py` configuration file.

## [v0.2.0] - 2015-08-12

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

## [v0.1.0] - 2015-08-10

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

[v0.3.0]: https://github.com/bioboxes/command-line-interface/releases/tag/v0.3.0
[v0.2.2]: https://github.com/bioboxes/command-line-interface/releases/tag/v0.2.2
[v0.2.1]: https://github.com/bioboxes/command-line-interface/releases/tag/v0.2.1
[v0.2.0]: https://github.com/bioboxes/command-line-interface/releases/tag/v0.2.0
[v0.1.0]: https://github.com/bioboxes/command-line-interface/releases/tag/v0.1.0
