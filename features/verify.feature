Feature: A CLI to verify images are biobox-compatible

  Scenario Outline: Verifying a valid biobox image
    When I run the command:
      """
      biobox short_read_assembler <image> --verify
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0

    Examples:
      | image           |
      | bioboxes/velvet |
