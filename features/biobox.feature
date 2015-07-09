Feature: A CLI to run biobox-compatible Docker containers

  Scenario Outline: Getting help documentation
    When I run the command:
      """
      biobox <cmd>
      """
    Then the stderr should be empty
    And the exit code should be 0
    And the stdout should contain
      """
      Usage
      """

    Examples:
      | cmd    |
      | --help |
      | -h     |

  Scenario: Getting help documentation for a biobox type
    When I run the command:
      """
      biobox short_read_assembler --help
      """
    Then the stderr should be empty
    And the exit code should be 0
    And the stdout should contain
      """
      biobox short_read_assembler <container> [options]
      """

  Scenario: Trying to run an unknown container type
    When I run the command:
      """
      biobox unknown_container --help
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown biobox container type: "unknown_container".
      Run `biobox --help` for a list of available biobox types.

      """
