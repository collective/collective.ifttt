*** Settings ***

Library  SeleniumLibrary  timeout=30  implicit_wait=0

*** Variables ***

${FIXTURE}    collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING
${BROWSER}    firefox

*** Keywords ***

# ============================================================================
# Test Setup and Test Teardown are only called when robot tests are run for
# the whole directory with ./bin/pybot -v SCREENSHOTS:true ./docs/_screenshots
# ============================================================================

Test Setup
    Import library  plone.app.robotframework.Zope2Server
    Set Zope layer  ${FIXTURE}
    ZODB Setup
    Open default browser
    Set window size  1200  900

Test Teardown
    Import library  plone.app.robotframework.Zope2Server
    Set Zope layer  ${FIXTURE}
    ZODB TearDown
    Close all browsers
