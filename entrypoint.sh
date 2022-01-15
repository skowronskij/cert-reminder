#!/usr/bin/env bash

/usr/bin/env python /cert_reminder/main.py --settings /cert_reminder/settings.json -c
cron -f
