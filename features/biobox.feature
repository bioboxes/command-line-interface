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
    And the stdout should contain
      """
      biobox short_read_assembler <image> [options]
      """
    And the exit code should be 0

  Scenario Outline: Trying to run an unknown container type
    When I run the command:
      """
      biobox <container> --help
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown biobox container type: "<container>".
      Run `biobox --help` for a list of available biobox types.

      """

      Examples:
      | container |
      | dummy     |
      | unknown   |

  Scenario Outline: Trying to run an unknown biobox container
    When I run the command:
      """
      biobox \
        short_read_assembler \
        biobox/unknown \
        <args>
      """
    Then the stdout should be empty
    And the stderr should equal:
      """
      No Docker image available with the name: biobox/unknown
      Did you include the namespace too? E.g. bioboxes/velvet.
      """
    And the exit code should be 1

    Examples:
      | args                                 |
      |                                      |
      | --input=reads.fq --output=contigs.fa |

  Scenario Outline: Running a biobox container
    Given I have the example genome paired fastq file "reads.fq.gz"
    When I run the command:
      """
      biobox \
        short_read_assembler \
        <assembler>
        --input=reads.fq.gz \
        --output=contigs.fa
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0
    And the file "contigs.fa" should exist
    And the file "contigs.fa" should not be empty

    Examples:
      | assembler        |
      | bioboxes/velvet  |
      | bioboxes/megahit |
