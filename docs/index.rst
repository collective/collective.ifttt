Welcome to collective.ifttt!
============================================

collective.ifttt is a Plone addon which enables any
Plone site to play in the IFTTT (pronounced /ɪft/) ecosystem
by allowing you to create IFTTT applets at `ifttt.com <http://ifttt.com>`_.

Below are a few examples of using IFTTT with Plone sites.

 - If a news item is published, then tweet about it or post it on Facebook.
 - If an event is published, then add it to my calendar.
 - If new users sign up for an event, then add them to a Slack channel.
 - If content changes, then record who edited it in a Google spreadsheet.

Contents
--------

This documentation will teach you how to use collective.ifttt to create IFTTT applets for Plone sites.
We'll start with setting up a Plone RSS feed, which can be used on IFTTT without doing anything special.
In the sections after that you will learn how to set up your IFTTT secret key and create IFTTT triggers 
for content and forms, so you can create more customized applets. Finally, we explain how this add-on
uses Plone content rules under the hood. For those who are familiar with them, we show how to get even 
more flexibility by creating a content rule with an IFTTT action.


.. toctree::
   :maxdepth: 3

   What_is_IFTTT
   Introduction_to_IFTTT_Applets
   Enable_RSS_feed_on_Plone
   Using_Plone_RSS_Feeds_in_IFTTT_Applets
   Configuring_Your_IFTTT_Secret_Key
   content_trigger
   user_trigger
   event_trigger
   manage_trigger
   IFTTT_Easyform_Action
   IFTTT_Trigger_and_Applet
   Trigger_IFTTT_Action

