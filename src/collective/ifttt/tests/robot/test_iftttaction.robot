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
    And I check 'Content types are: News Item' on pagecontent
    And I configure IFTTT trigger action
    Then I check 'test_ifttt_applet with context title,url' on pagecontent
    # Input IFTTT secret key
    And I fill secret key
    # Trigger action and post request to IFTTT
    When I add test__ifttt_content_rule for news item
    And I add a news item
    And I update news item
    Then I must see ifttt trigger in action

*** Keywords ***

# --- Given ------------------------------------------------------------------

I'm logged in as a Site Administrator
  Enable autologin as  Site Administrator

I'm at Content Rules
  Goto  ${PLONE_URL}/@@rules-controlpanel
  I check 'Content Rules' on pagecontent
  I check 'Use the form below' on pagecontent

I configure new content rule form
  Goto  ${PLONE_URL}/+rule/plone.ContentRule
  I check 'Add Rule' on pagecontent
  I check 'Once complete, you can manage the' on pagecontent
  I input 'test__ifttt_content_rule' into 'form.widgets.title' textinput
  I select 'Object modified' into 'form-widgets-event' selectbox
  I press 'Save' clickbutton
  I check 'Edit content rule' on pagecontent
  I check 'IFTTT Trigger Action' on pagecontent


# --- WHEN -------------------------------------------------------------------

I configure trigger condition
   I select 'plone.conditions.PortalType' into 'contentrules-add-condition' selectbox
   I press 'form.button.AddCondition' clickbutton
   I check 'portal type condition' on pagecontent
   I select 'News Item' into 'form-widgets-check_types' selectbox
   I press '#form-buttons-save' into 'css=.pattern-modal-buttons' clickoverlaybutton


I configure IFTTT trigger action
   I select 'plone.actions.Ifttt' into 'contentrules-add-action' selectbox
   I press 'form.button.AddAction' clickbutton
   I check 'An IFTTT trigger action' on pagecontent
   Then I input 'test_ifttt_applet' into 'form-widgets-ifttt_event_name' textinput
   And I select 'description' into 'form-widgets-payload_option' selectbox
   I press '#form-buttons-save' into 'css=.pattern-modal-buttons' clickoverlaybutton

I add test__ifttt_content_rule for news item
    Goto  ${Plone_URL}/@@manage-content-rules
    I check 'Content rules for' on pagecontent
    I select 'rule-1' into 'select-rules' selectbox
    I press 'Add' clickbutton
    I check 'Active content rules in this Plone Site' on pagecontent

I add a news item
  Goto  ${PLONE_URL}/++add++News%20Item
  I check 'Add News Item' on pagecontent
  I input 'This will not trigger IFTTT' into 'form-widgets-IDublinCore-title' textinput
  I input 'trigger summary' into 'form-widgets-IDublinCore-description' textinput
  I press 'form-buttons-save' clickbutton
  I check 'Item created' on pagecontent

I update news item
    Goto  ${PLONE_URL}/this-will-not-trigger-ifttt/edit
    I check 'Edit News Item' on pagecontent
    I input 'This will trigger IFTTT' into 'form-widgets-IDublinCore-title' textinput
    I input 'triggering ifttt applet' into 'form-widgets-IDublinCore-description' textinput
    I press 'form-buttons-save' clickbutton
#    I check 'Item created' on pagecontent

I select '${select}' into '${id}' selectbox
  Select from list by value  id=${id}  ${select}

I press '${value}' clickbutton
  Click button  ${value}

I input '${value}' into '${field}' textinput
  Input text  ${field}  ${value}

I press '${value}' into '${id}' clickoverlaybutton
  Click button  ${id} ${value}

I check '${text}' on pagecontent
  Wait until page contains  ${text}

I check element '${text}' on pagecsscontent
  Wait until page contains element  ${text}

I check '${text}' on instantpage
  Page should contain  ${text}

I check element '${text}' on instantpagecss
  Page should contain element  ${text}

I sleep for '${duration}'
  Sleep  time_=${duration}

# --- THEN -------------------------------------------------------------------

I fill secret key
  Goto  ${PLONE_URL}/@@collectiveifttt-controlpanel
  Page should contain  Ifttt Settings
  Input text  form.widgets.ifttt_secret_key  secret
  I press 'Save' clickbutton
  I check 'Changes saved' on pagecontent

I must see ifttt trigger in action
  I check 'Successfully triggered the IFTTT applet test_ifttt_applet' on pagecontent
#
I see confirmation on success
  Wait until page contains  Changes saved.

Test Setup
  Open test browser
#  Set Window Size  1280  720
