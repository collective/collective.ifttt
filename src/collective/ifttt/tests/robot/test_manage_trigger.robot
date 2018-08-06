
# ============================================================================
# CONTENT TRIGGER ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.ifttt -t test_manage_trigger.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/ifttt/tests/robot/test_manage_trigger.robot
#
#   for debug mode
# $ bin/robot-debug src/collective/ifttt/tests/robot/test_manage_trigger.robot

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

Scenario: As a site administrator I cannot see Manage Trigger actions form if secret key is not filled
    Given I'm logged in as a Site Administrator
    And I goto home page
    Then I check the 'Manage IFTTT Triggers' action menu item

Scenario: As a site administrator I can see Manage Trigger actions form
    Given I'm logged in as a Site Administrator
    And I fill secret key
    And I goto home page
    When I trigger the 'Manage IFTTT Triggers' action menu item
    Then check 'Select certain IFTTT Triggers to delete' on pagecontent

Scenario: As a site administrator I can delete an IFTTT Trigger
    Given I'm logged in as a Site Administrator
    And I fill secret key
    And I goto home page
    And I trigger the 'Add IFTTT Content Trigger' action menu item
    And I fill Content Trigger form
    And I see 'Successfully applied the IFTTT event test_event to Plone site' on success
    And I trigger the 'Manage IFTTT Triggers' action menu item
    When I select Test Trigger to delete
    Then I see 'Successfully applied changes' on success

*** Keywords ***

# --- Given ------------------------------------------------------------------

I'm logged in as a Site Administrator
  Enable autologin as  Site Administrator

I fill secret key
  Goto  ${PLONE_URL}/@@collectiveifttt-controlpanel
  check 'IFTTT Settings' on pagecontent
  input 'secret' into 'form.widgets.ifttt_secret_key' textinput
  press 'Save' clickbutton
  check 'Changes' on pagecontent

I goto home page
   GOTO  ${PLONE_URL}/

I fill Content Trigger form
   input 'test_event' into 'form-widgets-ifttt_event_name' textinput
   select 'Collection' into 'form-widgets-content_types-from' selectbox
   press 'from2toButton' clickbutton
   select 'Event' into 'form-widgets-content_types-from' selectbox
   press 'from2toButton' clickbutton
   select 'File' into 'form-widgets-content_types-from' selectbox
   press 'from2toButton' clickbutton
   press 'form.buttons.add' clickbutton

# --- WHEN -------------------------------------------------------------------

I check the 'Manage IFTTT Triggers' action menu item
    Element should not be visible  xpath=//li[@id='plone-contentmenu-ifttttriggers']/a

I trigger the '${action}' action menu item
    Element should be visible  xpath=//li[@id='plone-contentmenu-ifttttriggers']/a
    Click link  xpath=//li[@id='plone-contentmenu-ifttttriggers']/a
    Wait until element is visible  id=plone-contentmenu-ifttttriggers-${action}
    Click link  id=plone-contentmenu-ifttttriggers-${action}

I select Test Trigger to delete
   select checkbox 'form-widgets-ifttt_triggers-0'
   press 'form.buttons.delete' clickbutton


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

select checkbox '${value-id}'
  Select Checkbox  css=#${value-id}

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
