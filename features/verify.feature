Feature: A CLI to verify images are biobox-compatible

  Scenario Outline: Verifying a valid biobox image
    When I run the command:
      """
      biobox verify short_read_assembler <image> <args>
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0

    Examples:
      | image            | args            |
      | bioboxes/velvet  |                 |
      | bioboxes/velvet  | -t default      |
      | bioboxes/megahit | --task=no-mercy |

  Scenario: Verifying a invalid image
    When I run the command:
      """
      biobox verify short_read_assembler python:2.7
      """
    Then the stdout should be empty
    And the stderr should contain:
      """
      Error "python:2.7" is not a valid short_read_assembler biobox.
      Should return an error for a non-yaml formatted biobox.yaml file.

      """
    And the exit code should be 1
