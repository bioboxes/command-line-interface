Feature: A CLI to verify images are biobox-compatible

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
      | short_read_assembler | bioboxes/megahit | --task=no-mercy |
      | assembler_benchmark  | bioboxes/quast   |                 |

  Scenario: Generating a verbose output of biobox image verification
    When I run the command:
      """
      biobox verify \
        short_read_assembler \
        bioboxes/velvet \
        --verbose \
        --t default
      """
    Then the stderr should be empty
    And the stdout should equal:
    """
    Return an error when the biobox.yaml is in an invalid format.            PASS
    Return an error when the biobox.yaml is missing a version number.        PASS
    Return an error when the biobox.yaml has an invalid version number.      PASS
    Return an error when the biobox.yaml is missing the "arguments" field.   PASS
    Return an error the biobox.yaml has an unknown additional field.         PASS
    Create a contigs file when given a valid biobox.yml and FASTQ data.      PASS
    Create a 'log.txt' file when a metadata directory is mounted.            PASS

    """
    And the exit code should be 0

  Scenario Outline: Verifying an invalid biobox image
    When I run the command:
      """
      biobox verify short_read_assembler test-verify --task <task>
      """
    Then the stdout should be empty
    And the stderr should equal:
      """
      Error "test-verify" is not a valid short_read_assembler biobox.
      Should return an error when the biobox.yaml is in an invalid format.

      """
    And the exit code should be 1

    Examples:
      | task     |
      | exit-0   |
      | exit-1   |
      | exit-128 |

  Scenario: Generating a verbose output of failing biobox image verification
    When I run the command:
      """
      biobox verify \
        short_read_assembler \
        test-verify \
        --verbose
      """
    Then the stderr should be empty
    And the stdout should equal:
    """
    Return an error when the biobox.yaml is in an invalid format.            FAIL
    Return an error when the biobox.yaml is missing a version number.        FAIL
    Return an error when the biobox.yaml has an invalid version number.      FAIL
    Return an error when the biobox.yaml is missing the "arguments" field.   FAIL
    Return an error the biobox.yaml has an unknown additional field.         FAIL
    Create a contigs file when given a valid biobox.yml and FASTQ data.      FAIL
    Create a 'log.txt' file when a metadata directory is mounted.            FAIL

    """
    And the exit code should be 0
