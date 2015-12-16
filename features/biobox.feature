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

  Scenario Outline: Running a biobox short read assembler container
    Given I copy the example data files:
      | source                    | dest        |
      | short_read_assembler/genome_paired_reads.fq.gz | reads.fq.gz |
    When I run the command:
      """
      biobox \
        run \
        short_read_assembler \
        <assembler> \
        <ressources> \
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
      | assembler        | ressources                                       |    args                        | input                   | output                   |
      | bioboxes/velvet  |                                                  |                                | reads.fq.gz             | contigs.fa               |
      | bioboxes/velvet  |                                                  |                                | $(realpath reads.fq.gz) | contigs.fa               |
      | bioboxes/velvet  |                                                  |                                | reads.fq.gz             | $(realpath .)/contigs.fa |
      | bioboxes/velvet  | --memory=1g --cpu-shares=512                     |                                | reads.fq.gz             | $(realpath .)/contigs.fa |
      | bioboxes/velvet  | -m 1g -c 512                                     |                                | $(realpath reads.fq.gz) | contigs.fa               |

  Scenario Outline: Running a biobox assembler benchmark container
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source         | dest                 |
      | assembler_benchmark/assembly.fasta | input/assembly.fasta |
    And I copy the example data directories:
      | source     | dest             |
      | assembler_benchmark/references | input/references |
    When I run the command:
      """
      biobox \
        run \
        assembler_benchmark \
        <benchmark> \
        <ressources> \
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
      | benchmark      | args | ressources                                              | input-fasta                      | input-ref                    | output             |
      | bioboxes/quast |      |                                                         | $(realpath input/assembly.fasta) | $(realpath input/references) | $(realpath output) |
      | bioboxes/quast |      |                                                         | input/assembly.fasta             | input/references             | output             |
      | bioboxes/quast |      | --memory=1g --cpu-shares=512                            | $(realpath input/assembly.fasta) | $(realpath input/references) | $(realpath output) |
      | bioboxes/quast |      | -m 1g -c 512                                            | input/assembly.fasta             | input/references             | output             |