#!/bin/bash

# Define the crontab entries
entry1="0 3 * * * ubuntu /opt/emol/.venv/bin/python /opt/emol/emol/manage.py send_reminders"
entry2="0 4 * * * ubuntu /opt/emol/.venv/bin/python /opt/emol/emol/manage.py clean_expired"

# Function to check if a crontab entry exists
cron_entry_exists() {
    crontab -l 2>/dev/null | grep -q "$1"
}

# Add the crontab entries idempotently
if ! cron_entry_exists "$entry1"; then
    (crontab -l 2>/dev/null; echo "$entry1") | crontab -
    echo "Added crontab entry: $entry1"
else
    echo "Crontab entry already exists: $entry1"
fi

if ! cron_entry_exists "$entry2"; then
    (crontab -l 2>/dev/null; echo "$entry2") | crontab -
    echo "Added crontab entry: $entry2"
else
    echo "Crontab entry already exists: $entry2"
fi