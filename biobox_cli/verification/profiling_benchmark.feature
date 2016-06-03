Feature: Ensuring a the profiling benchmark matches the bioboxes specification

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
      ---
      arguments:
        prediction:
          path: /bbx/mnt/input/pred
          format: bioboxes.org:/profiling:0.9
        ground_truth:
          path: /bbx/mnt/input/truth
          format: bioboxes.org:/profiling:0.9
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
      version: "0.1"
      arguments:
        prediction:
          path: /bbx/mnt/input/pred
          format: bioboxes.org:/profiling:0.9
        ground_truth:
          path: /bbx/mnt/input/truth
          format: bioboxes.org:/profiling:0.9
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
      '0.1' does not match '^0.1.\\d+$'
      """

  Scenario: An biobox.yaml with a wrong version number.
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
    """
    version: "0.8.0"
    arguments:
      prediction:
        path: /bbx/mnt/input/pred
        format: bioboxes.org:/profiling:0.9
      ground_truth:
        path: /bbx/mnt/input/truth
        format: bioboxes.org:/profiling:0.9
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
      '0.8.0' does not match '^0.1.\\d+$'
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
      """
      'arguments' is a required property
      """

  Scenario Outline: An biobox.yaml with an additional unknown field
    Given I create the directory "input"
    And I create the directory "output"
    And I create the file "input/biobox.yaml" with the contents:
      """
      version: "0.1.0"
      arguments:
        prediction:
          path: /bbx/mnt/input/pred
          format: bioboxes.org:/profiling:0.9
        ground_truth:
          path: /bbx/mnt/input/truth
          format: bioboxes.org:/profiling:0.9
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


  Scenario: Run profiling benchmark with basic input
    Given I create the directory "input"
    And I create the directory "output"
    And I copy the example data files:
      | source                                     | dest        |
      | profiling_benchmark/ground_truth.profile   | input/truth |
      | profiling_benchmark/prediction.profile     | input/pred  |
    And I create the file "input/biobox.yaml" with the contents:
      """
      ---
      version: "0.1.0"
      arguments:
        prediction:
          path: /bbx/mnt/input/pred
          format: bioboxes.org:/profiling:0.9
        ground_truth:
          path: /bbx/mnt/input/truth
          format: bioboxes.org:/profiling:0.9
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
      | source                                     | dest        |
      | profiling_benchmark/ground_truth.profile   | input/truth |
      | profiling_benchmark/prediction.profile     | input/pred  |
    And I create the file "input/biobox.yaml" with the contents:
      """
      ---
      version: "0.1.0"
      arguments:
        prediction:
          path: /bbx/mnt/input/pred
          format: bioboxes.org:/profiling:0.9
        ground_truth:
          path: /bbx/mnt/input/truth
          format: bioboxes.org:/profiling:0.9
      """
    When I run the command:
      """
        docker run \
          --volume="$(pwd)/metadata:/bbx/metadata:rw" \
          --volume="$(pwd)/input:/bbx/mnt/input:ro" \
          --volume="$(pwd)/output:/bbx/mnt/output:rw" \
          ${IMAGE} ${TASK}
        """
    Then the exit code should be 0
    And the following files should exist and not be empty:
      | file               |
      | output/biobox.yaml |