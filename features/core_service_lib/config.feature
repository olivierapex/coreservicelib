Feature: config
    Conf class

Scenario: Set config file exist
    When I set good config
    Then everything is fine

# Scenario: Set config file doesn't exist
#     When I set bad config
#     Then everything is fine

Scenario: Get log with good config file
    When I get log with good config file
    Then everything is fine

Scenario: Get log with bad config file
    When I get log with bad config file
    Then something is wrong

Scenario: Get host_ip with good config file
    When I get host_ip with good config file
    Then everything is fine

Scenario: Get host_ip with bad config file
    When I get host_ip with bad config file
    Then something is wrong