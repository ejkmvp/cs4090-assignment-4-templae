Feature: Filter by Task Priority

Scenario: Filter for High Priority
    Given I have a task with High Priority
    And I have a task with Medium Priority
    And I have a task with Low Priority
    When I filter for High Priority
    Then I only receive tasks with High Priority

Scenario: Filter for Medium Priority
    Given I have a task with High Priority
    And I have a task with Medium Priority
    And I have a task with Low Priority
    When I filter for Medium Priority
    Then I only receive tasks with Medium Priority
    
Scenario: Filter for Low Priority
    Given I have a task with High Priority
    And I have a task with Medium Priority
    And I have a task with Low Priority
    When I filter for Low Priority
    Then I only receive tasks with Low Priority