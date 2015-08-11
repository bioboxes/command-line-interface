Feature: Verification steps for short read assembler bioboxes

  Scenario: A garbled biobox.yaml file.
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

  Scenario: An biobox.yaml missing the version number.
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

  Scenario: An biobox.yaml with a missing patch version number.
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

  Scenario: An biobox.yaml with a missing arguments field.
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

  Scenario Outline: An biobox.yaml with an additional unknown field
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
        ${TASK}
      """
    Then the stderr should be empty
    And the exit code should be 0
    And the file "output/biobox.yaml" should not be empty
    And the file "output/contigs.fa" should not be empty
