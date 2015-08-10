Feature: A CLI to run biobox-compatible Docker containers

  Scenario Outline: Getting the version number
    When I run the command:
      """
      biobox <cmd>
      """
    Then the stderr should be empty
    And the exit code should be 0
    And the stdout should match /\d+\.\d+\.\d+/

    Examples:
      | cmd       |
      | --version |
      | -v        |

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

  Scenario Outline: Trying to run an unknown command
    When I run the command:
      """
      biobox <cmd> short_read_assembler biobox/velvet --help
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown command: "<cmd>".
      Run `biobox --help` for a list of available.

      """

      Examples:
      | cmd     |
      | dummy   |
      | unknown |

  Scenario Outline: Trying to run an unknown biobox type
    When I run the command:
      """
      biobox run <biobox> biobox/velvet --help
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown biobox type: "<biobox>".
      Run `biobox --help` for a list of available.

      """

      Examples:
      | command | biobox  |
      | run     | dummy   |
      | run     | unknown |
      | verify  | unknown |

  Scenario: Getting help documentation for a biobox type
    When I run the command:
      """
      biobox run short_read_assembler --help
      """
    Then the stderr should be empty
    And the stdout should contain
      """
      Usage:
          biobox run short_read_assembler <image>
      """
    And the exit code should be 0

  @internet
  Scenario Outline: Trying to run an unknown biobox image
    When I run the command:
      """
      biobox \
        run \
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
      | --input=reads.fq --output=contigs.fa |

  Scenario Outline: Running a biobox container
    Given I copy the example data files:
      | source                    | dest        |
      | genome_paired_reads.fq.gz | reads.fq.gz |
    When I run the command:
      """
      biobox \
        run \
        short_read_assembler \
        <assembler> \
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
