Feature: New Task ID Generation

Scenario: Id Incrementation
    Given I have a task with id 5
    When I create a new task
    Then The newly created task will have id 6

Scenario: Multiple Tasks
    Given I have a task with id 5
    When I create a new task
    And I create a new task
    And I create a new task
    And I create a new task
    Then The newly created task will have id 9

Scenario: Multiple Tasks with seperated IDs
    Given I have a task with id 4
    And I have a task with id 9
    When I create a new task
    Then The newly created task will have id 10
