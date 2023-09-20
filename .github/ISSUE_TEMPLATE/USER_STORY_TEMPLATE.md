name: User story [Only Quivr Team]
description: Use this form for user stories.
title: "[Epic]: User story"
labels: ["user story"]
body:

- type: markdown
    attributes:
      value: |
        **Epic**

        Include the issue that represents the epic.

- type: input
    id: epic-link
    attributes:
      label: Link to the Epic
      placeholder: Paste the link to the related epic here...
    validations:
      required: true

- type: markdown
    attributes:
      value: |
        **Functional**

        Detail the functionality and provide context and motivation.

- type: textarea
    id: functionality-detail
    attributes:
      label: Explain the Functionality
      placeholder: Detail the user story functionality here...
    validations:
      required: true

- type: markdown
    attributes:
      value: |
        **Schema**

- type: markdown
    attributes:
      value: |
        ### Tech

- type: checkboxes
    id: tech-todo
    attributes:
      label: Tech To-dos
      options:
        - label: To-do Item 1
        - label: To-do Item 2
        # Add more to-dos as needed

- type: markdown
    attributes:
      value: |
        ### Tests

- type: checkboxes
    id: tests
    attributes:
      label: Test Cases
      options:
        - label: it should ...
        - label: it can ...
        # Add more test cases as needed
  
- type: markdown
    attributes:
      value: |
        ### Validation Checks

- type: checkboxes
    id: validation-checks
    attributes:
      label: Validation Checks
      options:
        - label: it should validate ...
        - label: it shouldn't allow ...
        # Add more validation checks as needed
