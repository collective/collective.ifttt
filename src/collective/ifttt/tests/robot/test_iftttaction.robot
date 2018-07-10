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

Scenario: As a site administrator I can configure IFTTT Trigger on modified news item
    Given I'm logged in as a Site Administrator
    And I'm at Content Rules
    And I configure new content rule form
    And I configure trigger condition
    When I configure IFTTT trigger action
    Then I see 'test_ifttt_applet with context title,url' on success


# Already checked on test_controlpanel
Scenario: As a site administrator I can configure IFTTT Secret Key
    Given I'm logged in as a Site Administrator
    When I fill secret key
    Then I see 'Changes saved' on success

# Check request call to IFTTT on object modified
# this depends on successful passing of previous 2 scenerios
Scenerio: As a site administrator I can modify news item and see Ifttt triggering action
    Given I'm logged in as a Site Administrator
    And I'm at Content Rules
    And I configure new content rule form
    And I configure trigger condition
    And I configure IFTTT trigger action
    And I fill secret key
    When I add test__ifttt_content_rule for news item
    And I add a news item
    And I update news item
    Then I see 'Successfully triggered the IFTTT applet test_ifttt_applet' on success

*** Keywords ***

# --- Given ------------------------------------------------------------------

I'm logged in as a Site Administrator
  Enable autologin as  Site Administrator

I'm at Content Rules
  Goto  ${PLONE_URL}/@@rules-controlpanel
  check 'Content Rules' on pagecontent
  check 'Use the form below' on pagecontent

I configure new content rule form
  Goto  ${PLONE_URL}/+rule/plone.ContentRule
  check 'Add Rule' on pagecontent
  check 'Once complete, you can manage the' on pagecontent
  input 'test__ifttt_content_rule' into 'form.widgets.title' textinput
  select 'Object modified' into 'form-widgets-event' selectbox
  press 'Save' clickbutton
  check 'Edit content rule' on pagecontent
  check 'IFTTT Trigger' on pagecontent

I configure trigger condition
   select 'plone.conditions.PortalType' into 'contentrules-add-condition' selectbox
   press 'form.button.AddCondition' clickbutton
   check 'portal type condition' on pagecontent
   select 'News Item' into 'form-widgets-check_types' selectbox
   press '#form-buttons-save' into 'css=.pattern-modal-buttons' clickoverlaybutton
   check 'Content types are: News Item' on pagecontent

# --- WHEN -------------------------------------------------------------------


I configure IFTTT trigger action
   select 'plone.actions.Ifttt' into 'contentrules-add-action' selectbox
   press 'form.button.AddAction' clickbutton
   check 'An IFTTT trigger action' on pagecontent
   input 'test_ifttt_applet' into 'form-widgets-ifttt_event_name' textinput
   select 'description' into 'form-widgets-payload_option' selectbox
   press '#form-buttons-save' into 'css=.pattern-modal-buttons' clickoverlaybutton
   check 'context title,url' on pagecontent

I fill secret key
  Goto  ${PLONE_URL}/@@collectiveifttt-controlpanel
  check 'IFTTT Settings' on pagecontent
  input 'secret' into 'form.widgets.ifttt_secret_key' textinput
  press 'Save' clickbutton
  check 'Changes' on pagecontent

I add test__ifttt_content_rule for news item
    Goto  ${Plone_URL}/@@manage-content-rules
    check 'Content rules for' on pagecontent
    select 'rule-1' into 'select-rules' selectbox
    press 'Add' clickbutton
    check 'Active content rules in this Plone Site' on pagecontent

I add a news item
  Goto  ${PLONE_URL}/++add++News%20Item
  check 'Add News Item' on pagecontent
  input 'This will not trigger IFTTT' into 'form-widgets-IDublinCore-title' textinput
  input 'trigger summary' into 'form-widgets-IDublinCore-description' textinput
  press 'form-buttons-save' clickbutton
  check 'Item created' on pagecontent

I update news item
    Goto  ${PLONE_URL}/this-will-not-trigger-ifttt/edit
    check 'Edit News Item' on pagecontent
    input 'This will trigger IFTTT' into 'form-widgets-IDublinCore-title' textinput
    input 'triggering ifttt applet' into 'form-widgets-IDublinCore-description' textinput
    press 'form-buttons-save' clickbutton

# --- THEN -------------------------------------------------------------------

I see '${sucess_message}' on success
  Page should contain   ${sucess_message}

Test Setup
  Open test browser
#  Set Window Size  1280  720


# --- selenium library keywords -------------------------------------------------------------------

select '${select}' into '${id}' selectbox
  Select from list by value  id=${id}  ${select}

press '${value}' clickbutton
  Click button  ${value}

input '${value}' into '${field}' textinput
  Input text  ${field}  ${value}

press '${value}' into '${id}' clickoverlaybutton
  Click button  ${id} ${value}

check '${text}' on pagecontent
  Wait until page contains  ${text}

check element '${text}' on pagecsscontent
  Wait until page contains element  ${text}

check '${text}' on instantpage
  Page should contain  ${text}

check element '${text}' on instantpagecss
  Page should contain element  ${text}

sleep for '${duration}'
  Sleep  time_=${duration}

