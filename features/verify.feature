Feature: A CLI to verify images are biobox-compatible

  @internet
  Scenario: Trying verify a non-existent image
    When I run the command:
      """
      biobox verify short_read_assembler unknown
      """
    Then the stdout should be empty
    And the stderr should contain:
      """
      No Docker image available with the name: unknown
      Did you include the namespace too? E.g. bioboxes/velvet.
      """ 
    And the exit code should be 1

  Scenario Outline: Verifying a valid biobox image
    When I run the command:
      """
      biobox verify <type> <image> <args>
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0

    Examples:
      | type                 | image            | args            |
      | short_read_assembler | bioboxes/velvet  |                 |
      | short_read_assembler | bioboxes/velvet  | -t default      |
      | short_read_assembler | bioboxes/megahit | --task=no-mercy |
      | assembler_benchmark  | bioboxes/quast   |                 |

  Scenario Outline: Verifying an invalid biobox image
    When I run the command:
      """
      biobox verify short_read_assembler test-verify --task <task>
      """
    Then the stdout should be empty
    And the stderr should contain:
      """
      Error "test-verify" is not a valid short_read_assembler biobox.
      Should return an error for a non-yaml formatted biobox.yaml file.

      """
    And the exit code should be 1

    Examples:
      | task     |
      | exit-0   |
      | exit-1   |
      | exit-128 |
