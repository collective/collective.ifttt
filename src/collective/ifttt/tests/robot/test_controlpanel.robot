# ============================================================================
# CONTROLPANEL ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.ifttt -t test_controlpanel.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/ifttt/tests/robot/test_controlpanel.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  Selenium2Screenshots/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Variables ***

${SELENIUM2LIBRARY_RUN_ON_FAILURE}  Capture page screenshot
${SCREENSHOTS}  false


*** Test Cases ***

Scenario: As a site administrator I can see IFTTT Settings configlet
  Given I'm logged in as a Site Administrator
   When I open Site Setup
   Then I can see IFTTT Settings configlet

Scenario: As a site administrator I can open IFTTT Settings form
  Given I'm logged in as a Site Administrator
    And I'm at Site Setup
   When I click IFTTT Settings configlet
   Then I can see IFTTT Settings form

Scenario: As a site administrator I can set IFTTT secret
  Given I'm logged in as a Site Administrator
    And I'm at IFTTT Settings form
   When I enter IFTTT secret
    And I press Save
   Then I see confirmation on success


*** Keywords ***

# --- Given ------------------------------------------------------------------

I'm logged in as a Site Administrator
  Enable autologin as  Site Administrator

I'm at Site Setup
  Goto  ${PLONE_URL}/@@overview-controlpanel
  Page should contain  Site Setup
  Page should contain  Configuration area for Plone

I'm at IFTTT Settings form
  Goto  ${PLONE_URL}/@@collectiveifttt-controlpanel
  Page should contain  IFTTT Settings


# --- WHEN -------------------------------------------------------------------

I open Site Setup
  Goto  ${PLONE_URL}/@@overview-controlpanel
  Page should contain  Site Setup
  Page should contain  Configuration area for Plone

I click IFTTT Settings configlet
  Page should contain  Add-on Configuration
  Page should contain  IFTTT Settings
  Page should contain link  css=a[href$="@@collectiveifttt-controlpanel"]
  Click link  css=a[href$="@@collectiveifttt-controlpanel"]

I enter IFTTT secret
  Input text  form.widgets.ifttt_secret_key  secret

  # Capture screenshots for docs
  Run keyword if  '${SCREENSHOTS}' == 'true'
  ...  Highlight  css=#formfield-form-widgets-ifttt_secret_key
  Run keyword if  '${SCREENSHOTS}' == 'true'
  ...  Capture page screenshot
  ...  ${CURDIR}/ifttt-setting-secret-full.png
  Run keyword if  '${SCREENSHOTS}' == 'true'
  ...  Capture and crop page screenshot
  ...  ${CURDIR}/ifttt-setting-secret-cropped.png  css=#content

I press Save
  Click button  Save


# --- THEN -------------------------------------------------------------------

I can see IFTTT Settings configlet
  Page should contain  Add-on Configuration
  Page should contain  IFTTT Settings
  Page should contain link  css=a[href$="@@collectiveifttt-controlpanel"]

I can see IFTTT Settings form
  Page should contain element
  ...  css=body.template-collectiveifttt-controlpanel #content #form
  Element should be visible
  ...  css=body.template-collectiveifttt-controlpanel #content #form

  # Capture screenshots for docs
  Run keyword if  '${SCREENSHOTS}' == 'true'
  ...  Capture page screenshot
  ...  ${CURDIR}/ifttt-controlpanel-full.png
  Run keyword if  '${SCREENSHOTS}' == 'true'
  ...  Capture and crop page screenshot
  ...  ${CURDIR}/ifttt-controlpanel-cropped.png  css=#content

I see confirmation on success
  Wait until page contains  Changes saved.
