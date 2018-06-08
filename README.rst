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

collective.ifttt is a Plone addon which enables any Plone site to play in the IFTTT (pronounced /ɪft/) ecosystem by allowing you to create IFTTT applets at `ifttt.com <http://ifttt.com>`_.

Examples
--------

Below are a few examples of using IFTTT with Plone sites.

 - If a news item is published, then tweet about it or post it on Facebook.
 - If an event is published, then add it to my calendar.
 - If new users sign up for an event, then add them to a Slack channel.
 - If content changes, then record who edited it in a Google spreadsheet.

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
