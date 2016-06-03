Feature: Verification steps for short read assembler bioboxes

  Scenario: Should return an error when the biobox.yaml is in an invalid format.
    Given I create the directory "input"
    And I create the file "input/biobox.yaml" with the contents:
      """
      'nonsense"/4*
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input" \
        ${IMAGE} \
        ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      Error parsing the YAML file: /bbx/input/biobox.yaml
      """

  Scenario: Should return an error when the biobox.yaml is missing a version number.
    Given I create the directory "input"
    Given I create the file "input/biobox.yaml" with the contents:
      """
      arguments:
        - fastq:
          - id: "pe"
            value: "/reads.fastq.gz"
            type: paired
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input" \
        ${IMAGE} \
        ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      'version' is a required property
      """

  Scenario: Should return an error when the biobox.yaml has an invalid version number.
    Given I create the directory "input"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.9"
      arguments:
        - fastq:
          - id: "pe"
            value: "/reads.fastq.gz"
            type: paired
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input" \
        ${IMAGE} \
        ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '0.9' does not match '^0.9.\\d+$'
      """

  Scenario: Should return an error when the biobox.yaml is missing the "arguments" field.
    Given I create the directory "input"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.9.0"
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input" \
        ${IMAGE} \
        ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      'arguments' is a required property
      """

  Scenario Outline: Should return an error the biobox.yaml has an unknown additional field.
    Given I create the directory "input"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.9.0"
      arguments:
        - fastq:
          - id: "pe"
            value: "/reads.fastq.gz"
            type: paired
      <field>: {}
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input" \
        ${IMAGE} \
        ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      Additional properties are not allowed ('<field>' was unexpected)
      """

    Examples:
      | field         |
      | unknown       |
      | invalid_fastq |

  Scenario: Should create a contigs file when given a valid biobox.yml and FASTQ data.
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source                    | dest              |
      | short_read_assembler/genome_paired_reads.fq.gz | input/reads.fq.gz |
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
        ${TASK}
      """
    Then excluding warnings the stderr should be empty
    And the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |
      | output/contigs.fa  |

  Scenario: Should create a 'log.txt' file when a metadata directory is mounted.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the directory "metadata"
    And I copy the example data files:
      | source                    | dest              |
      | short_read_assembler/genome_paired_reads.fq.gz | input/reads.fq.gz |
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
        --volume="${TMPDIR}/metadata:/bbx/metadata:rw" \
        --volume="${TMPDIR}/input:/bbx/input:ro"       \
        --volume="${TMPDIR}/output:/bbx/output:rw"     \
        ${IMAGE} \
        ${TASK}
      """
    Then excluding warnings the stderr should be empty
    And the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |
      | output/contigs.fa  |
      | metadata/log.txt   |
