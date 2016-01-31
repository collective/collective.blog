# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.blog -t test_blogentry.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.blog.testing.COLLECTIVE_BLOG_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_blogentry.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a BlogEntry
  Given a logged-in site administrator
    and an add blogentry form
   When I type 'My BlogEntry' into the title field
    and I submit the form
   Then a blogentry with the title 'My BlogEntry' has been created

Scenario: As a site administrator I can view a BlogEntry
  Given a logged-in site administrator
    and a blogentry 'My BlogEntry'
   When I go to the blogentry view
   Then I can see the blogentry title 'My BlogEntry'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add blogentry form
  Go To  ${PLONE_URL}/++add++BlogEntry

a blogentry 'My BlogEntry'
  Create content  type=BlogEntry  id=my-blogentry  title=My BlogEntry


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the blogentry view
  Go To  ${PLONE_URL}/my-blogentry
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a blogentry with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the blogentry title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
