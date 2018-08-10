Easyform Trigger
================

This document will exhplain how to add an IFTTT Trigger to an
Easyform by using the Easyform action that is provided in this package.

What are Easyforms?
-------------------
Easyforms provide a Plone through-the-web form builder using 
fields, widgets, actions and validators. To learn more about
Easyforms, see the
`Easyform documentation <https://collectiveeasyform.readthedocs.io/en/latest/>`_.

About IFTTTTrigger
------------------
Collective.ifttt provides a new Easyform action called IFTTTTrigger. It can be added 
to a form at any time but it will not be functional until it has
at least 1 IFTTT payload defined. On successful form submission, IFTTTTrigger
will send a triggering event to IFTTT that contains selected form field data as
payloads.

Add IFTTT Action
----------------

Follow the steps given below to add an IFTTTTrigger action to any Easyform.

1. Create the Easyform as described `here <https://collectiveeasyform.readthedocs.io/en/latest/adding.html>`_.

2. Add an action to the form.

.. image:: _static/images/easyform/add_action.png

3. Click on ``Add new action``, fill in the required details
and select ``IFTTTTrigger`` as `Action type`.

.. image:: _static/images/easyform/add_new_action.png

4. Click ``Settings`` on the created action to configure it.

.. image:: _static/images/easyform/settings_action.png

5. Configure the action and click `Save`:

   - Provide the `IFTTT event name` you want to use - note that this will be used in the
     URL sent to trigger IFTTT, so it must be a URL-friendly name (no spaces or
     special characters)
   - Select up to 3 `form fields` to use as the `payloads`

.. image:: _static/images/easyform/configure_action.png


Now upon every successful submission of the
form, the data in the selected form fields
will be sent to IFTTT as the event payloads.
