Feature: Ensuring a short read assembler matches the bioboxes specification

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
      --volume="$(pwd)/input:/bbx/mnt/input" \
      ${IMAGE} \
      ${TASK}
    """
    Then the exit code should be 1
    And the stderr should contain:
      """
      Error parsing the YAML file: /bbx/mnt/input/biobox.yaml
      """

  Scenario: An biobox.yaml missing the version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      arguments:
        assemblies:
          - path: /bbx/mnt/input/assembly.fasta
            id: ray
            type: contig
            format: bioboxes.org:/fasta
        reads:
          - path: /bbx/mnt/input/reads.fq.gz
            id: lib1
            type: paired
            format: bioboxes.org:/fastq
      """
    When I run the command:
    """
    docker run --volume="$(pwd)/input:/bbx/mnt/input" ${IMAGE} ${TASK}
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
      version: "0.2"
      arguments:
        assemblies:
          - path: /bbx/mnt/input/assembly.fasta
            id: ray
            type: contig
            format: bioboxes.org:/fasta
        reads:
          - path: /bbx/mnt/input/reads.fq.gz
            id: lib1
            type: paired
            format: bioboxes.org:/fastq
      """
    When I run the command:
    """
    docker run \
      --env="TASK=default" \
      --volume="$(pwd)/input:/bbx/mnt/input:ro" \
      ${IMAGE} \
      ${TASK}
    """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '0.2' does not match '^0.2.\\d+$'
      """

  Scenario: An biobox.yaml with a wrong version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
      version: "0.8.0"
      arguments:
        assemblies:
          - path: /bbx/mnt/input/assembly.fasta
            id: ray
            type: contig
            format: bioboxes.org:/fasta
        reads:
          - path: /bbx/mnt/input/reads.fq.gz
            id: lib1
            type: paired
            format: bioboxes.org:/fastq
     """
    When I run the command:
      """
      docker run \
        --env="TASK=default" \
        --volume="$(pwd)/input:/bbx/mnt/input:ro" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      '0.8.0' does not match '^0.2.\\d+$'
      """

  Scenario: An biobox.yaml with a missing arguments field.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.2.0"
      """
    When I run the command:
      """
      docker run \
        --env="TASK=default" \
        --volume="$(pwd)/input:/bbx/mnt/input" \
        ${IMAGE} ${TASK}
      """
    Then the exit code should be 1
    And the stderr should contain:
      """
      'arguments' is a required property
      """

  Scenario Outline: A biobox.yaml with an additional unknown field
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.2.0"
      arguments:
        assemblies:
          - path: /bbx/mnt/input/assembly.fasta
            id: ray
            type: contig
            format: bioboxes.org:/fasta
        reads:
          - path: /bbx/mnt/input/reads.fq.gz
            id: lib1
            type: paired
            format: bioboxes.org:/fastq
      <field>: {}
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/mnt/input:ro" \
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

  Scenario: Run read based assembler benchmark container with basic input
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source                      | dest                 |
      | assembler_read_based_benchmark/genome_paired_reads.fq.gz   | input/reads.fq.gz               |
      | assembler_read_based_benchmark/assembly.fasta   | input/assembly.fasta  |
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.2.0"
      arguments:
        assemblies:
          - path: /bbx/mnt/input/assembly.fasta
            id: ray
            type: contig
            format: bioboxes.org:/fasta
        reads:
          - path: /bbx/mnt/input/reads.fq.gz
            id: lib1
            type: paired
            format: bioboxes.org:/fastq
      """
    When I run the command:
      """
      docker run \
        --volume="$(pwd)/input:/bbx/mnt/input:ro" \
        --volume="$(pwd)/output:/bbx/mnt/output:rw" \
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
      | source                      | dest                 |
      | assembler_read_based_benchmark/genome_paired_reads.fq.gz   | input/reads.fq.gz               |
      | assembler_read_based_benchmark/assembly.fasta   | input/assembly.fasta  |
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.2.0"
      arguments:
        assemblies:
          - path: /bbx/mnt/input/assembly.fasta
            id: ray
            type: contig
            format: bioboxes.org:/fasta
        reads:
          - path: /bbx/mnt/input/reads.fq.gz
            id: lib1
            type: paired
            format: bioboxes.org:/fastq
      """
    When I run the command:
      """
        docker run \
          --volume="$(pwd)/metadata:/bbx/mnt/metadata:rw" \
          --volume="$(pwd)/input:/bbx/mnt/input:ro" \
          --volume="$(pwd)/output:/bbx/mnt/output:rw" \
          ${IMAGE} ${TASK}
        """
    Then the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |
      | metadata/log.txt   |