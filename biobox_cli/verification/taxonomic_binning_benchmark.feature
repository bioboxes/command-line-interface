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
        sequences:
          path: STRING
          id: STRING
          type: contig
          format: bioboxes.org:/fasta
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
      version: "0.10"
      arguments:
        sequences:
          path: STRING
          id: STRING
          type: contig
          format: bioboxes.org:/fasta
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
      '0.10' does not match '^0.10.\\d+$'
      """

  Scenario: An biobox.yaml with a wrong version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
      version: "0.8.0"
      arguments:
         sequences:
          path: STRING
          id: STRING
          type: contig
          format: bioboxes.org:/fasta
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
      '0.8.0' does not match '^0.10.\\d+$'
      """

  Scenario: An biobox.yaml with a missing arguments field.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
    version: "0.10.0"
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

  Scenario Outline: An biobox.yaml with an additional unknown field
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
     """
     version: "0.10.0"
     arguments:
       sequences:
         path: STRING
         id: STRING
         type: contig
         format: bioboxes.org:/fasta
       labels:
         path: STRING
         id: STRING
         type: binning
         format: bioboxes.org:/binning/binning:0.9/taxbinning
       predictions:
         path: STRING
         id: STRING
         type: binning
         format: bioboxes.org:/binning/binning:0.9/taxbinning
       databases:
         taxonomy:
           path: STRING
           id: STRING
           type: ncbi
           format: bioboxes.org:/taxonomy_ncbi_dumps
     <field>: {}
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
     Additional properties are not allowed ('<field>' was unexpected)
     """

    Examples:
      | field         |
      | unknown       |
      | invalid_fasta |

  Scenario: Run taxonomic binning with basic input
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data directories:
      | source            | dest                 |
      | taxonomic_binning | input/taxonomic_binning     |
    And I create the file "input/biobox.yaml" with the contents:
     """
     ---
     version: 0.10.0
     arguments:
       sequences:
         path: /bbx/mnt/input/taxonomic_binning/contigs.fna
         id: contigs
         type: contig
         format: bioboxes.org:/fasta
       labels:
         path: /bbx/mnt/input/taxonomic_binning/labels.binning
         id: binning
         type: binning
         format: bioboxes.org:/binning/binning:0.9/taxbinning
       predictions:
         path: /bbx/mnt/input/taxonomic_binning/prediction.binning
         id: prediction
         type: binning
         format: bioboxes.org:/binning/binning:0.9/taxbinning
       databases:
         taxonomy:
           path: /bbx/mnt/input/taxonomic_binning/taxonomy
           id: tax
           type: ncbi
           format: bioboxes.org:/taxonomy_ncbi_dumps
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
    And I copy the example data directories:
      | source            | dest                 |
      | taxonomic_binning | input/taxonomic_binning     |
    And I create the file "input/biobox.yaml" with the contents:
     """
     ---
     version: 0.10.0
     arguments:
       sequences:
         path: /bbx/mnt/input/taxonomic_binning/contigs.fna
         id: contigs
         type: contig
         format: bioboxes.org:/fasta
       labels:
         path: /bbx/mnt/input/taxonomic_binning/labels.binning
         id: binning
         type: binning
         format: bioboxes.org:/binning/binning:0.9/taxbinning
       predictions:
         path: /bbx/mnt/input/taxonomic_binning/prediction.binning
         id: prediction
         type: binning
         format: bioboxes.org:/binning/binning:0.9/taxbinning
       databases:
         taxonomy:
           path: /bbx/mnt/input/taxonomic_binning/taxonomy
           id: tax
           type: ncbi
           format: bioboxes.org:/taxonomy_ncbi_dumps
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