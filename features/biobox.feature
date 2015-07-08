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
