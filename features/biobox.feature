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


  Scenario: Using absolute paths when passing command line arguments
    Given I copy the example data files:
      | source                                         | dest        |
      | short_read_assembler/genome_paired_reads.fq.gz | reads.fq.gz |
    When I run the command:
      """
      biobox \
        run \
        short_read_assembler \
        bioboxes/crash-test-biobox \
        --task=short-read-assembler \
        --no-rm \
        --input=$(realpath reads.fq.gz) \
        --output=$(realpath .)/contigs.fa
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0
    And the file "contigs.fa" should exist
    And the file "contigs.fa" should not be empty


  Scenario Outline: Running a biobox short read assembler container
    Given I copy the example data files:
      | source                                         | dest        |
      | short_read_assembler/genome_paired_reads.fq.gz | reads.fq.gz |
    When I run the command:
      """
      biobox \
        run \
        short_read_assembler \
        bioboxes/crash-test-biobox \
        --task=short-read-assembler \
        <resources> \
        --no-rm \
        --input=reads.fq.gz \
        --output=contigs.fa
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0
    And the file "contigs.fa" should exist
    And the file "contigs.fa" should not be empty

    Examples:
      | resources        |
      | --memory=1g      |
      | --cpu-shares=512 |


  Scenario Outline: Running a biobox assembler benchmark container
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source                             | dest                 |
      | assembler_benchmark/assembly.fasta | input/assembly.fasta |
    And I copy the example data directories:
      | source                         | dest             |
      | assembler_benchmark/references | input/references |
    When I run the command:
      """
      biobox \
        run \
        assembler_benchmark \
        bioboxes/crash-test-biobox \
        <resources> \
        --no-rm \
        --task=quast \
        --input-fasta=input/assembly.fasta \
        --output=output
      """
    Then the stdout should be empty
    And the stderr should be empty
    And the exit code should be 0
    And the file "output/report.tsv" should exist
    And the file "output/report.tsv" should not be empty

    Examples:
      | resources        | input-ref                    |
      | --cpu-shares=512 |                              |
      | --memory=1g      | --input-ref=input/references |
