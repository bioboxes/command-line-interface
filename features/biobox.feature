Feature: A CLI to run biobox-compatible Docker containers

  Scenario Outline: Getting help documentation
    When I run the command:
      """
      biobox <cmd>
      """
    Then the stderr should be empty
    And the exit code should be 0
    And the stdout should contain:
      """
      Usage
      """

    Examples:
      | cmd    |
      | --help |
      | -h     |
