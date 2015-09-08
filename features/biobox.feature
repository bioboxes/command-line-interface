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

  Scenario Outline: Running a biobox short read assembler container
    Given I copy the example data files:
      | source                    | dest        |
      | genome_paired_reads.fq.gz | reads.fq.gz |
    When I run the command:
      """
      biobox \
        run \
        short_read_assembler \
        <assembler> \
        --no-rm \
        --input=<input> \
        --output=<output> \
        <args>
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0
    And the file "contigs.fa" should exist
    And the file "contigs.fa" should not be empty

    Examples:
      | assembler        | args            | input                   | output                   |
      | bioboxes/velvet  |                 | reads.fq.gz             | contigs.fa               |
      | bioboxes/velvet  |                 | $(realpath reads.fq.gz) | contigs.fa               |
      | bioboxes/velvet  |                 | reads.fq.gz             | $(realpath .)/contigs.fa |
      | bioboxes/megahit | --task=no-mercy | reads.fq.gz             | contigs.fa               |

  Scenario Outline: Running a biobox assembler benchmark container
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source         | dest                 |
      | assembly.fasta | input/assembly.fasta |
    And I copy the example data directories:
      | source     | dest             |
      | references | input/references |
    When I run the command:
      """
      biobox \
        run \
        assembler_benchmark \
        <benchmark> \
        --no-rm \
        --input-fasta=<input-fasta> \
        --input-ref=<input-ref> \
        --output=<output> \
        <args>
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0
    And the file "output/biobox.yaml" should exist
    And the file "output/biobox.yaml" should not be empty
    Examples:
      | benchmark      | args | input-fasta                      | input-ref                    | output             |
      | bioboxes/quast |      | $(realpath input/assembly.fasta) | $(realpath input/references) | $(realpath output) |
      | bioboxes/quast |      | input/assembly.fasta             | input/references             | output             |