Feature: Ensuring a the assembler benchmark matches the bioboxes specification

  Scenario: A garbled biobox.yaml file.
    Given I create the directory "input"
    And I create the directory "output"
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
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      arguments:
        - fasta:
          - id: "pe"
            value: "/reads.fasta"
            type: contigs
      """
    When I run the command:
    """
    docker run --volume="$(pwd)/input:/bbx/input" ${IMAGE} ${TASK}
    """
    Then the exit code should be 1
    And the stderr should contain:
      """
      'version' is a required property
      """

  Scenario: An biobox.yaml with a missing patch version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.9"
      arguments:
        - fasta:
          - id: "pe"
            value: "/reads.fasta"
            type: contigs
      """
    When I run the command:
    """
    docker run \
      --env="TASK=default" \
      --volume="$(pwd)/input:/bbx/input:ro" \
      ${IMAGE} \
      ${TASK}
    """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '0.9' does not match '^0.9.\\d+$'
      """

  Scenario: An biobox.yaml with a wrong version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
      version: "0.8.0"
      arguments:
        - fasta:
          - id: "pe"
            value: "/reads.fasta"
            type: contigs
     """
    When I run the command:
      """
      docker run \
        --env="TASK=default" \
        --volume="$(pwd)/input:/bbx/input:ro" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '0.8.0' does not match '^0.9.\\d+$'
      """

  Scenario: An biobox.yaml with a missing arguments field.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.9.0"
      """
    When I run the command:
      """
      docker run \
        --env="TASK=default" \
        --volume="$(pwd)/input:/bbx/input" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      'arguments' is a required property
      """

  Scenario Outline: An biobox.yaml with an additional unknown field
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.9.0"
      arguments:
        - fasta:
          - id: "pe"
            value: "/reads.fasta"
            type: contigs
      <field>: {}
      """
    When I run the command:
      """
      docker run \
        --env="TASK=default" \
        --volume="$(pwd)/input:/bbx/input:ro" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      Additional properties are not allowed ('<field>' was unexpected)
      """

    Examples:
      | field         |
      | unknown       |
      | invalid_fasta |


  Scenario: Run assembler benchmark with basic input
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source           | dest                 |
      | assembler_benchmark/assembly.fasta   | input/assembly.fasta |
    And I copy the example data directories:
      | source           | dest                 |
      | assembler_benchmark/references       | input/references     |
    And I create the file "input/biobox.yaml" with the contents:
      """
      ---
      version: 0.9.0
      arguments:
        - fasta:
          - id: "1"
            value: "/bbx/input/assembly.fasta"
            type: contigs
        - fasta_dir: "/bbx/input/references"
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input:ro" \
        --volume="$(pwd)/output:/bbx/output:rw" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |

  Scenario: Check if output log is produced.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the directory "metadata"
    And I copy the example data files:
      | source           | dest                 |
      | assembler_benchmark/assembly.fasta   | input/assembly.fasta |
    And I copy the example data directories:
      | source           | dest                 |
      | assembler_benchmark/references       | input/references     |
    And I create the file "input/biobox.yaml" with the contents:
      """
      ---
      version: 0.9.0
      arguments:
        - fasta:
          - id: "1"
            value: "/bbx/input/assembly.fasta"
            type: contigs
        - fasta_dir: "/bbx/input/references"
      """
    When I run the command:
      """
        docker run \
          --volume="$(pwd)/metadata:/bbx/metadata:rw" \
          --volume="$(pwd)/input:/bbx/input:ro" \
          --volume="$(pwd)/output:/bbx/output:rw" \
          ${IMAGE} ${TASK}
        """
    Then the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |
      | metadata/log.txt   |