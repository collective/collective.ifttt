.. _user_trigger:

User Trigger
============

This document will explain how to add an IFTTT "User Trigger" to a Plone folder.
The User Trigger will send a triggering event to IFTTT when content in or below
the folder is edited, including information about who changed it.
This allows creation of IFTTT applets to, for example,
log the edit information to Slack or a Google spreadsheet.

**Note**: For the trigger to work, an IFTTT secret key must be configured
for the site as described at :ref:`configure_ifttt_secret_key`.

Add User Trigger
----------------

Follow the steps given below to add a User Trigger to any folder.

1. Traverse to the desired folder.

2. From the IFTTT menu select ``Add IFTTT User Trigger``.

.. image:: _static/images/add_ifttt_content_trigger/select_actions.png

3. Fill out the form with the required values and click ``Add``.
   Note that the event name will be used in the URL that will trigger IFTTT,
   so it must be a URL-friendly name (no spaces or special characters).

.. image:: _static/images/add_ifttt_user_trigger/fill_form.png

Behind the Scenes
-----------------

Collective.ifttt uses
`Plone content rules <https://docs.plone.org/working-with-content/managing-content/contentrules.html>`_
to implement IFTTT triggers.
For those who are interested, this section explains what happens behind the scenes.

After the Add form gets filled in, a new content rule is dynamically created and
applied to the folder. See the Rules menu on the left bar to see all the folder's content rules.

.. image:: _static/images/add_ifttt_user_trigger/rule_tab.png

The new content rule will be triggered by a Plone ``Object Modified`` event.
It will have one condition defined for each content type selected,
and one action, IFTTT Trigger. This action will trigger IFTTT with an event
named according to what was filled out on the Add form.

Data Sent to IFTTT
------------------

The event sent to IFTTT by the User Trigger will contain the following 3 payload
data items for the content object that was edited:

- Title
- URL
- Username of the person who modified the content

