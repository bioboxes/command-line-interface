Feature: Ensuring a unsupervised binning benchmark container matches the bioboxes specification

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
      ---
      arguments:
        - fasta:
          value: /path/to/file
          type: contig
        - labels:
          value: /path/to/file
          type: binning
        - predictions:
          value: /path/to/file
          type: binning
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
      version: "0.11"
      arguments:
        - fasta:
          value: /path/to/file
          type: contig
        - labels:
          value: /path/to/file
          type: binning
        - predictions:
          value: /path/to/file
          type: binning
      """
    When I run the command:
    """
    docker run \
      --volume="$(pwd)/input:/bbx/input:ro" \
      ${IMAGE} \
      ${TASK}
    """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '0.11' does not match '^0.11.\\d+$'
      """

  Scenario: An biobox.yaml with a wrong version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
    version: "42.11.0"
    arguments:
      - fasta:
          value: /path/to/file
          type: contig
      - labels:
          value: /path/to/file
          type: binning
      - predictions:
          value: /path/to/file
          type: binning
     """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/input:ro" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '42.11.0' does not match '^0.11.\\d+$'
      """

  Scenario: An biobox.yaml with a missing arguments field.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.11.0"
      """
    When I run the command:
      """
      docker run \
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
      version: "0.11.0"
      arguments:
        - fasta:
            value: /path/to/file
            type: contig
        - labels:
            value: /path/to/file
            type: binning
        - predictions:
            value: /path/to/file
            type: binning

      <field>: {}
      """
    When I run the command:
      """
      docker run \
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

  Scenario: Run unsupervised binning benchmark with basic input
    Given I create the directory "input"
    And I create the directory "output"
    And I download the file "https://s3-eu-west-1.amazonaws.com/cami-data-eu/CAMI_low/CAMI_low_RL_S001__insert_270_GoldStandardAssembly.fasta.gz" to "input/gold_standard.fasta.gz"
    And I copy the example data files:
      | source                                                 | dest        |
      | unsupervised_binning_benchmark/query.binning           | input/query.binning |
      | unsupervised_binning_benchmark/gsa_mapping.binning     | input/gsa_mapping.binning  |
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.11.0"
      arguments:
        - fasta:
            value: /bbx/input/gold_standard.fasta.gz
            type: contig
        - labels:
            value: /bbx/input/gsa_mapping.binning
            type: binning
        - predictions:
            value: /bbx/input/query.binning
            type: binning
      """
    When I run the command:
      """
      docker run --volume="$(pwd)/input:/bbx/input:ro" --volume="$(pwd)/output:/bbx/output:rw" ${IMAGE} ${TASK}
      """
    Then the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |