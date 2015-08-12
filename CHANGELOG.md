# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] - date

### Added

  * Ability to specify a task to use when verifying a short read assembler
    biobox. This is passed using the `--task` flag to `biobox verify`.

  * Short read assembler verification now checks that the file `log.txt` is
    created when a directory that is mounted to `/bbx/metadata`.

### Changed

  * Updated README.md with more explicit instructions on how to submit pull
    requests.

## [0.1.0] - 2015-02-17

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
