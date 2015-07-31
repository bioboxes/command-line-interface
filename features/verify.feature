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
      | image            |
      | bioboxes/velvet  |
      | bioboxes/megahit |

  Scenario: Verifying a invalid image
    When I run the command:
      """
      biobox short_read_assembler python:2.7 --verify
      """
    Then the stdout should be empty
    And the stderr should contain:
      """
      Verification failed - python:2.7 is not a valid biobox short read assembler.
      """
    And the exit code should be 1
