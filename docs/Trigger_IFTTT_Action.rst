Content Rule Action "Trigger IFTTT"
===================================

`Plone Content Rules <https://docs.plone.org/working-with-content/managing-content/contentrules.html>`_
are a powerful mechanism to automate dealing with content using `conditions` and `actions`.
A content rule will automatically perform actions when certain Plone events (known as content rule “triggers”) 
take place and the defined conditions are met.

Collective.ifttt contains a new content rule action, `IFTTT Trigger`,
that posts an event to the IFTTT web service when a content rule is triggered and its 
conditions are satisfied. Content rules with this action are used to implement the folder-level
triggers that collective.ifttt provides (Content Trigger, Event Trigger, etc.) If
the functionality provided by these out-of-the-box triggers does not meet your needs, you
can create your own content rule with the `IFTTT Trigger` action and your own conditions.

Creating and Defining Content Rules
-----------------------------------

`Plone's documentation <https://docs.plone.org/working-with-content/managing-content/contentrules.html#creating-and-defining-content-rules>`_ provides instructions for creating content rules. Here is a simple example of
a content rule to send an IFTTT trigger when a news item is modified.
The resulting rule can be assigned to any folder on your site or to the site root.

- Triggering event: Object modified
- Condition: Content type equals News Item
- Action: Select “IFTTT Trigger” from the drop down menu and click on the “Add” button.

.. image:: _static/images/Trigger_IFTTT_Action/select_action.png

- Fill out the form:

  - For “IFTTT event name” enter the IFTTT event which you want to trigger.
    Note that the event name will be used in the URL sent to the IFTTT webservice,
    so it must be a URL-friendly name (no spaces or special characters)
  - Choose the 3rd payload from the options provided - description, username, or 
    event start time (which will only be used if the content triggering the action
    is an event).
    
- Click the “Save” button.

.. image:: _static/images/Trigger_IFTTT_Action/configure_action.png

Data Sent to IFTTT
------------------

The event sent to IFTTT will contain the following 3 payload data items 
from the content object that triggered the content rule:

- Title
- URL
- The 3rd payload chosen on the form
