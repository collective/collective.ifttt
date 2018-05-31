.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.ifttt.svg?branch=master
    :target: https://travis-ci.org/collective/collective.ifttt
.. image:: https://coveralls.io/repos/github/collective/collective.ifttt/badge.svg
    :target: https://coveralls.io/github/collective/collective.ifttt
.. image:: https://readthedocs.org/projects/collectiveifttt/badge/?version=latest
    :target: https://collectiveifttt.readthedocs.io/en/latest/?badge=latest

================
collective.ifttt
================

collective.ifttt is an addon which enables any Plone site to play in the IFTTT (pronounced /ɪft/) ecosystem by allowing you to create IFTTT applets.

Examples
--------

Below are a few user stories of IFTTT with Plone site.

 - If published news on Plone Site, then tweet about it or post it on slack.
 - If published new event on Plone Site, then tweet about it
 - If new user signed up for an event, then add him to the slack channel.
 - If new applet gets published for Plone, then send me a notification about it.

Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://collectiveifttt.readthedocs.io/en/latest/


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install collective.ifttt by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.ifttt


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.ifttt/issues
- Source Code: https://github.com/collective/collective.ifttt
- Documentation: http://collectiveifttt.readthedocs.io/en/latest/


Support
-------

If you are having issues, please let us know in `issues`


License
-------

The project is licensed under the GPLv2.
