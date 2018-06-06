# ============================================================================
# ROBOT SCREENSHOTS
# ============================================================================
#
# Update screenshots from the project root directory by running
#
#  $ ./bin/pybot -v SCREENSHOTS:true docs/_screenshots
#
# Add and commit the updated screenshots into git repository and use them
# in the package Sphinx documentation as any other image files.
#
# Add new screenshots by writing new acceptance tests / test suites into
# ./src/collective/ifttt/tests/robot, follow the existing examples and
# symlink the .robot files into this directory to include their screenshots.
#
# ============================================================================

*** Settings ***

Library         plone.app.robotframework.Zope2Server

Suite Setup     Suite Setup
Suite Teardown  Suite Teardown

Test Setup      Test Setup
Test Teardown   Test Teardown

*** Variables ***

${FIXTURE}  collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING

*** Keywords ***

Suite Setup
    Start Zope server  ${FIXTURE}

Suite Teardown
    Stop Zope server
