Configuring Your IFTTT Channel
=================================

Introduction to IFTTT
---------------------

`ifttt.com <https://ifttt.com/discover>`_ . If This Then That, also known as IFTTT (pronounced /ɪft/),
is a free web-based service to create chains of simple conditional statements,
called applets.
An applet consists of triggers and actions. They can be triggered by changes that occur within other
web services such as Gmail, Facebook, Telegram, Instagram, or Pinterest.

collective.ifttt is an addon which enables any Plone site
to play in the IFTTT ecosystem by allowing you to create IFTTT triggers,
and to do that you need to configure the site with your secret key.

Creating an IFTTT Key and Storing It In Plone Site
--------------------------------------------------

IFTTT supports push notification support.
Which can be leveraged the get instant notifications from Plone site.
Follow below steps to get your IFTTT secret key and saving it in Plone site.

Obtain IFTTT Secret Key
^^^^^^^^^^^^^^^^^^^^^^^

Follow step given below:

1. Go to `ifttt.com <https://ifttt.com/discover>`_, sign up for an account.
2. At the top click on ‘Search’ and find ‘Maker’ (Update: this is now named 'Webhook')

.. image:: _static/images/configure_ifttt_channel/secret_key/search_maker.png

3. Then click the ‘Connect’ button to create a Maker (Webhook) channel.

.. image:: _static/images/configure_ifttt_channel/secret_key/settings_maker.png

4. Click on the gears icon (Settings) on the top-right of the Maker (Webhook) channel to view your key.

.. image:: _static/images/configure_ifttt_channel/secret_key/obtain_key.png

Save Ifttt's Secret Key in Plone Site
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Go to Site Setup

.. image:: _static/images/Enable_Rss_Feed/Enable_RSS/Step1.png

2. Select ``Ifttt Settings`` under `Add-on Configuration Tab`

.. image:: _static/images/configure_ifttt_channel/secret_key/select_ifttt_settings.png

3. Copy this key to Plone’s IFTTT Settings.

.. image:: _static/images/configure_ifttt_channel/secret_key/store_key.png

