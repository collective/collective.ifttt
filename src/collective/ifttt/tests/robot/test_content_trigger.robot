
# ============================================================================
# CONTENT TRIGGER ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.ifttt -t test_content_trigger.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.ifttt.testing.COLLECTIVE_IFTTT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/ifttt/tests/robot/test_content_trigger.robot
#
#   for debug mode
# $ bin/robot-debug src/collective/ifttt/tests/robot/test_content_trigger.robot

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

Scenario: As a site administrator I cannot see Content Trigger actions form if secret key is not filled
    Given I'm logged in as a Site Administrator
    And I goto home page
    Then I check the 'Add IFTTT Content Trigger' action menu item

Scenario: As a site administrator I can see Content Trigger actions form
    Given I'm logged in as a Site Administrator
    And I fill secret key
    And I goto home page
    When I trigger the 'Add IFTTT Content Trigger' action menu item
    Then check 'including the description of content' on pagecontent

Scenario: As a site administrator I can configure Content Trigger action
    Given I'm logged in as a Site Administrator
    And I fill secret key
    And I goto home page
    And I trigger the 'Add IFTTT Content Trigger' action menu item
    When I fill Content Trigger form
    Then I see 'Successfully applied the IFTTT event test_event to Plone site' on success

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

# --- WHEN -------------------------------------------------------------------

I check the 'Add IFTTT Content Trigger' action menu item
    Element should not be visible  xpath=//li[@id='plone-contentmenu-ifttttriggers']/a

I trigger the '${action}' action menu item
    Element should be visible  xpath=//li[@id='plone-contentmenu-ifttttriggers']/a
    Click link  xpath=//li[@id='plone-contentmenu-ifttttriggers']/a
    Wait until element is visible  id=plone-contentmenu-ifttttriggers-${action}
    Click link  id=plone-contentmenu-ifttttriggers-${action}

I fill Content Trigger form
    input 'test_event' into 'form-widgets-ifttt_event_name' textinput

    # Wait that select2 widget has been initialized
    Wait until page contains element  css=#formfield-form-widgets-content_types .select2-choices

    # Activate the widget to open its list of available options
    Click element  css=#formfield-form-widgets-content_types .select2-choices

    # Wait that the widget options list is open and first item is auto-selected
    Wait until page contains element  css=.select2-input.select2-focused

    # Type value and enter to the box to get the value selected
    Input text  css=.select2-input.select2-focused  Collection\n
    Input text  css=.select2-input.select2-focused  Event\n
    Input text  css=.select2-input.select2-focused  File\n

    # Wait that select2 widget has been initialized
    Wait until page contains element  css=#formfield-form-widgets-workflow_transitions .select2-choices

    # Activate the widget to open its list of available options
    Click element  css=#formfield-form-widgets-workflow_transitions .select2-choices

    # Wait that the widget options list is open and first item is auto-selected
    Wait until page contains element  css=.select2-input.select2-focused

    # Type value and enter to the box to get the value selected
    Input text  css=.select2-input.select2-focused  Approve // Publish [publish]\n

    press 'form.buttons.add' clickbutton

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
