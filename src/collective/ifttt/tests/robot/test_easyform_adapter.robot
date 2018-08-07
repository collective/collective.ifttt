
# ============================================================================
# CONTENT TRIGGER ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.ifttt -t test_easyform_adapter.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/ifttt/tests/robot/test_easyform_adapter.robot
#
#   for debug mode
# $ bin/robot-debug src/collective/ifttt/tests/robot/test_easyform_adapter.robot

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

Scenario: As a site administrator I can add an easyform and see IFTTTTrigger as action type
    Given I'm logged in as a Site Administrator
    And I goto home page
    And I trigger the easyform action menu item
    And I fill easyform
    When I trigger the Define form Actions menu item
    And I add new actions
    Then select 'IFTTTTrigger' into 'form-widgets-factory' selectbox

Scenario: As a site administrator I can configure IFTTTTrigger action
    Given I'm logged in as a Site Administrator
    And I goto home page
    And I trigger the easyform action menu item
    And I fill easyform
    And I trigger the Define form Actions menu item
    When I add new actions
    And I add IFTTTTrigger action
    Then I can configure IFTTTTrigger action

*** Keywords ***

# --- Given ------------------------------------------------------------------

I'm logged in as a Site Administrator
  Enable autologin as  Site Administrator

I goto home page
   GOTO  ${PLONE_URL}/

I trigger the easyform action menu item
    Element should be visible  xpath=//li[@id='plone-contentmenu-factories']/a
    Click link  xpath=//li[@id='plone-contentmenu-factories']/a
    Wait until element is visible  id=easyform
    Click link  id=easyform

I fill easyform
   input 'test_form' into 'form-widgets-IDublinCore-title' textinput
   press 'form-buttons-save' clickbutton


# --- WHEN -------------------------------------------------------------------

I add IFTTTTrigger action
   input 'test action' into 'form-widgets-title' textinput
   input 'test_action' into 'form-widgets-__name__' textinput
   select 'IFTTTTrigger' into 'form-widgets-factory' selectbox
   press 'form.buttons.add' clickbutton

I trigger the Define form Actions menu item
    Element should be visible  xpath=//li[@id='plone-contentmenu-actions']/a
    Click link  xpath=//li[@id='plone-contentmenu-actions']/a
    Wait until element is visible  id=plone-contentmenu-actions-Actions
    Click link  id=plone-contentmenu-actions-Actions

I add new actions
    Goto  ${PLONE_URL}/test_form/actions/@@add-action

# --- THEN -------------------------------------------------------------------

I can configure IFTTTTrigger action
    Goto  ${PLONE_URL}/test_form/actions/test_action
    input 'test ifttt' into 'form-widgets-ifttt_event_name' textinput
    select 'topic' into 'form-widgets-payload_fields-from' selectbox
    press 'from2toButton' clickbutton
    press 'form-buttons-save' clickbutton

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
