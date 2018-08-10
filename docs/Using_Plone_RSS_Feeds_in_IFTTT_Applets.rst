Using Plone RSS Feeds in IFTTT Applets
======================================

To learn how to create an IFTTT applet using an
RSS feed, follow the example below.
This applet will add a new row to a 
Google Spreadsheet each time an item is published on an RSS feed.
You can change this configuration to suit your own requirements.

-------------------

- Signup for a `free IFTTT account <https://ifttt.com/join>`_.

- Navigate to your username in the upper right corner.

- Select **New Applet** from the dropdown menu.

- Click the blue 'this' text.

- Search for ``rss`` and select ``RSS Feed``.

.. image:: _static/images/plone_rss_applet/search_rss.png

- Choose `New feed item` as the trigger.

- Fill in the RSS feed URL in the given space. Click `Create Trigger`.

.. image:: _static/images/plone_rss_applet/fill_rss_url.png

- Click the blue 'that' text.

- Search for ``google`` and choose `Google Sheets` as the Action Service.

.. image:: _static/images/plone_rss_applet/choose_google_sheets.png

-  Choose `Add row to spreadsheet` as the action.

- Configure the form as you wish and click `Create Action`.

.. image:: _static/images/plone_rss_applet/configure_action.png

- Click `Finish`.

.. image:: _static/images/plone_rss_applet/finish.png

This creates a new IFTTT Applet.

.. image:: _static/images/plone_rss_applet/successfull_creation.png

Now every time an item is published on the RSS feed, it will automatically be added as a new row
to the Google Spreadsheet.

.. image:: _static/images/plone_rss_applet/google_spreadsheet.png





