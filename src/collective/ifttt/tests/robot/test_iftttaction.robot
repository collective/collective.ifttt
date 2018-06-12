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
   And I'm at Content Rules
   And I configure new content rule form
  When I configure trigger condition
  And I sleep for '3s'
  And I configure IFTTT trigger action
  Then I press '#form-buttons-save' into 'css=.pattern-modal-buttons' clickoverlaybutton
  And I sleep for '3s'
  And I check 'test_ifttt_applet with context title,url' on pagecontent

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

I configure new content rule form
  Goto  ${PLONE_URL}/+rule/plone.ContentRule
  I check 'Add Rule' on pagecontent
  I check 'Once complete, you can manage the' on pagecontent
  I input 'test__content_rule' into 'form.widgets.title' textinput
  I select 'Object modified' into 'form-widgets-event' selectbox
  I press 'Save' clickbutton
  I check 'Edit content rule' on pagecontent
  I check 'IFTTT Trigger Action' on pagecontent

# --- WHEN -------------------------------------------------------------------

I configure trigger condition
   I select 'plone.conditions.PortalType' into 'contentrules-add-condition' selectbox
   I press 'form.button.AddCondition' clickbutton
   I sleep for '3s'
   I check 'portal type condition' on pagecontent
   I select 'News Item' into 'form-widgets-check_types' selectbox
   I press '#form-buttons-save' into 'css=.pattern-modal-buttons' clickoverlaybutton

I configure IFTTT trigger action
   I select 'plone.actions.Ifttt' into 'contentrules-add-action' selectbox
   And I sleep for '1s'
   I press 'form.button.AddAction' clickbutton
   And I sleep for '2s'
   I check 'An IFTTT trigger action' on pagecontent
   Then I input 'test_ifttt_applet' into 'form-widgets-ifttt_event_name' textinput
   And I select 'description' into 'form-widgets-payload_option' selectbox

I select '${select}' into '${id}' selectbox
  Select from list by value  id=${id}  ${select}

I press '${value}' clickbutton
  Click button  ${value}

I input '${value}' into '${field}' textinput
  Input text  ${field}  ${value}

I press '${value}' into '${id}' clickoverlaybutton
  Click button  ${id} ${value}

I check '${text}' on pagecontent
  Page should contain  ${text}
  Wait until page contains  ${text}

I check element '${text}' on pagecsscontent
  Page should contain element  ${text}
  Wait until page contains element  ${text}

I sleep for '${duration}'
  Sleep  time_=${duration}

# --- THEN -------------------------------------------------------------------

I see confirmation on success
  Wait until page contains  Changes saved.

Test Setup
  Open test browser
#  Set Window Size  1280  720
