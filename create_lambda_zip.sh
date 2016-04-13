#!/bin/sh

# clean up
rm -rf /tmp/paperless_registration
rm -f ~/paperless_registration.zip

# init
mkdir -p /tmp/paperless_registration

# copy data
cp -r * /tmp/paperless_registration

# install package dependencies
cd /tmp/paperless_registration
pip install -U -t . -r requirements/prod.txt

# compress
zip -qr ~/paperless_registration.zip *

# go back home
cd -
