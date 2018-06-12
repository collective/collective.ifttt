# ============================================================================
# IFTTTACTION ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.ifttt -t test_iftttaction.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/ifttt/tests/robot/test_iftttaction.robot
#
#   for debug mode
# $ bin/robot-debug src/collective/ifttt/tests/robot/test_iftttaction.robot


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
Library  Selenium2Screenshots

Test Setup  Test Setup
Test Teardown  Close all browsers



*** Variables ***

${SELENIUM2LIBRARY_RUN_ON_FAILURE}  Capture page screenshot
${SCREENSHOTS}  false


*** Test Cases ***

Scenario: As a site administrator I can configure IFTTT Trigger Action on modified news item
  Given I'm logged in as a Site Administrator
   And I'm at Site Setup
   And I'm at Content Rules
   And I click add content rule
   And I fill new rule form
   And I select 'Object modified' into 'form-widgets-event' selectbox
   And I press 'Save' clickbutton
  When I can see Edit content rule
   And I select 'plone.conditions.PortalType' into 'contentrules-add-condition' selectbox
   And I press 'form.button.AddCondition' clickbutton
   And I check 'Add Content Type Condition' on pagecontent
   And I select 'News Item' into 'form-widgets-check_types' selectbox
   And I press 'form-buttons-save' clickbutton
   And I select 'plone.actions.Ifttt' into 'contentrules-add-action' selectbox
    And I press 'form.button.AddAction' clickbutton
    And I check 'An ifttt trigger action' on pagecontent
   Then I fill the Ifttt Trigger Action form
    And I press 'Save' clickbutton

*** Keywords ***

# --- Given ------------------------------------------------------------------

I'm logged in as a Site Administrator
  Enable autologin as  Site Administrator

I'm at Site Setup
  Goto  ${PLONE_URL}/@@overview-controlpanel
  Page should contain  Site Setup
  Page should contain  Configuration area for Plone

I'm at Content Rules
  Goto  ${PLONE_URL}/@@rules-controlpanel
  Page should contain  Content Rules
  Page should contain  Use the form below

I click add content rule
  Goto  ${PLONE_URL}/+rule/plone.ContentRule
  Page should contain  Add Rule
  Page should contain  Once complete, you can manage the rule's actions and conditions separately.

I fill new rule form
    Input text  form.widgets.title  test__content_rule

I select '${select}' into '${id}' selectbox
  Select from list by value  id=${id}  ${select}

I press '${value}' clickbutton
  Click button  ${value}

# --- WHEN -------------------------------------------------------------------

I can see Edit content rule
  Page should contain  Edit content rule
  Page should contain  Add action
  Page should contain  Ifttt Trigger Action

I check '${text}' on pagecontent
  Page should contain  ${text}

# --- THEN -------------------------------------------------------------------

I fill the Ifttt Trigger Action form
    Input text  form-widgets-ifttt_event_name  test__event_name
    Select from list by value  id=form-widgets-payload_option  description

I see confirmation on success
  Wait until page contains  Changes saved.

Test Setup
  Open test browser
  Set Window Size  1280  720
