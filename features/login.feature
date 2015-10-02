Feature: Allow a user to ssh into an image to test internally

  Scenario: Logging into an image and listing file locations
    When I run the interactive command:
      """
      biobox login short_read_assembler bioboxes/velvet
      """
    And I type:
      """
      ls /bbx/*
      """
    Then the stdout should contain:
      """
      output:
      """
    And the stdout should contain:
      """
      input:
      biobox.yaml reads.fq.gz
      """
    And the directory ".biobox_tmp" should not exist
