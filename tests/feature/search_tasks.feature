Feature: Search Tasks

Scenario: Search for tasks from title
    Given I have a task with Meow in the title
    And I have a task with hello in the title
    When I search for the string Meo
    Then There should be 1 tasks output

Scenario: Search for tasks from description
    Given I have a task with Meow in the description
    And I have a task with hello in the description
    When I search for the string Meo
    Then There should be 1 tasks output