Feature: Providing useful errors to a user when they run the tool incorrectly

  Scenario Outline: Trying to run an unknown command
    When I run the command:
      """
      biobox <cmd> short_read_assembler bioboxes/crash-test-biobox --help
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


  Scenario Outline: Trying to run a biobox when the required input files do not exist
    When I run the command:
      """
      biobox \
        run \
        <type> \
        bioboxes/crash-test-biobox \
        --task=<task> \
        --no-rm \
        --<arg>=missing-file \
        --output=output
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should contain:
      """
      Given input file does not exist:
      """

    Examples:
      | type                 | task                 | arg         |
      | short_read_assembler | short-read-assembler | input       |
      | assembler_benchmark  | quast                | input-fasta |


  Scenario Outline: Trying to use an unknown biobox type
    When I run the command:
      """
      biobox <command> unknown bioboxes/crash-test-biobox
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown biobox type: "unknown".
      Run `biobox --help` for a list of available.

      """

    Examples:
      | command |
      | login   |
      | run     |
      | verify  |


  @internet
  Scenario Outline: Trying to use an unknown biobox image
    Given I copy the example data files:
      | source                                         | dest        |
      | short_read_assembler/genome_paired_reads.fq.gz | reads.fq.gz |
    When I run the command:
      """
      biobox <command> <type> bioboxes/unknown <args>
      """
    Then the stdout should be empty
    And the stderr should equal:
      """
      No Docker image available with the name: bioboxes/unknown
      Did you include the namespace too? E.g. bioboxes/velvet.

      """
    And the exit code should be 1

    Examples:
      | command | type                 | args                                    |
      | run     | short_read_assembler | --input=reads.fq.gz --output=contigs.fa |
      | login   | short_read_assembler |                                         |
      | verify  | short_read_assembler |                                         |
