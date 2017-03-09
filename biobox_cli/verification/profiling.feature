Feature: Ensuring a the profiling matches the bioboxes specification

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
        - fastq:
          - type: fastq
            value: /path/to/fastq
        - database:
            type: bioboxes.org:/taxonomy_ncbi_dumps
            value: /tmp/taxonomy
        - cache:
            type: directory
            value: /tmp/cache
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
      version: "0.1"
      arguments:
        - fastq:
          - type: fastq
            value: /path/to/fastq
        - database:
            type: bioboxes.org:/taxonomy_ncbi_dumps
            value: /tmp/taxonomy
        - cache:
            type: directory
            value: /tmp/cache
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
    """0.1' does not match '^0.1.\\d+$
    """

  Scenario: An biobox.yaml with a wrong version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
    version: "0.8.0"
    arguments:
      - fastq:
        - type: fastq
          value: /path/to/fastq
      - database:
          type: bioboxes.org:/taxonomy_ncbi_dumps
          value: /tmp/taxonomy
      - cache:
          type: directory
          value: /tmp/cache
     """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/mnt/input:ro" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """'0.8.0' does not match '^0.1.\\d+$'
      """
  Scenario: An biobox.yaml with a missing arguments field.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.1.0"
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/mnt/input" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """'arguments' is a required property
      """

  Scenario Outline: An biobox.yaml with an additional unknown field
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.1.0"
      arguments:
        - fastq:
          - type: fastq
            value: /path/to/fastq
        - database:
            type: bioboxes.org:/taxonomy_ncbi_dumps
            value: /tmp/taxonomy
        - cache:
            type: directory
            value: /tmp/cache
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

  Scenario: Run profiling benchmark with basic input
    Given I create the directory "input"
    And I download and extract the file "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz" to "input"
    And I create the directory "output"
    And I copy the example data files:
      | source                                     | dest        |
      | short_read_assembler/genome_paired_reads.fq.gz   | input/reads.fq.gz |
    And I create the file "input/biobox.yaml" with the contents:
      """
      ---
      version: "1.0.0"
      arguments:
        - fastq:
          - type: fastq
            value: /bbx/input/reads.fq.gz
        - database:
            type: bioboxes.org:/taxonomy_ncbi_dumps
            value: /bbx/input
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