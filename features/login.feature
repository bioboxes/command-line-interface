Feature: Allow a user to ssh into an image to test internally

  Scenario: Logging into an image and listing file locations
    When I run the interactive command:
      """
      biobox login short_read_assembler bioboxes/crash-test-biobox
      """
    And I type:
      """
      find /bbx/*
      """
    And I exit the shell
    Then the stdout should contain:
      """
      /bbx/output
      """
    And the stdout should contain:
      """
      /bbx/input/biobox.yaml
      """
    And the stdout should contain:
      """
      /bbx/input/reads.fq.gz
      """
