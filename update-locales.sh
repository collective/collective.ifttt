#!/usr/bin/env bash
# i18ndude should be available in current $PATH (eg by running
# ``export PATH=$PATH:$BUILDOUT_DIR/bin`` when i18ndude is located in your buildout's bin directory)
#
# For every language you want to translate into you need a
# ./src/collective/ifttt/locales/[language]/LC_MESSAGES/collective.ifttt.po
# (e.g. ./src/collective/ifttt/locales/de/LC_MESSAGES/collective.ifttt.po)

domain=collective.ifttt

./bin/i18ndude rebuild-pot \
    --pot ./src/collective/ifttt/locales/$domain.pot \
    --create $domain ./src/collective/ifttt
./bin/i18ndude sync \
    --pot ./src/collective/ifttt/locales/$domain.pot \
    ./src/collective/ifttt/locales/*/LC_MESSAGES/$domain.po
