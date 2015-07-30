Feature: Verification steps for short read assembler bioboxes

  Scenario: Running the biobox image successfully
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source                    | dest              |
      | genome_paired_reads.fq.gz | input/reads.fq.gz |
    And I create the file "input/biobox.yaml" with the contents:
      """
      ---
      version: 0.9.0
      arguments:
      - fastq:
        - value: /bbx/input/reads.fq.gz
          type: paired
          id: 0

      """
    When I run the command:
      """
      docker run \
        --volume="${TMPDIR}/input:/bbx/input:ro" \
        --volume="${TMPDIR}/output:/bbx/output:rw" \
        ${IMAGE} \
        default
      """
    Then the stderr should be empty
    And the exit code should be 0
    And the file "output/biobox.yaml" should not be empty
    And the file "output/contigs.fa" should not be empty
