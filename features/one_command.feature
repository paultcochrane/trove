Feature: run one command from command line
    As a trove user
    When I run trove with single commands
    I should see the output I expect

    Scenario: "--onecmd" without arguments
        Given I run trove with the --onecmd option and no argument
        Then I should see the missing argument in onecmd error message

    Scenario: "--onecmd" with "exit"
        Given a default password file exists
        When I run trove with "--onecmd exit"
        And the master passphrase is entered
        Then trove should exit cleanly

# vim: expandtab shiftwidth=4 softtabstop=4
