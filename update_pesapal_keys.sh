#!/bin/bash
# This safely updates your .env file with new Pesapal Live keys

# Remove old keys if they exist
sed -i '/^PESAPAL_CONSUMER_KEY=/d' .env
sed -i '/^PESAPAL_CONSUMER_SECRET=/d' .env

# Add new Live keys
echo "PESAPAL_CONSUMER_KEY=5ttQz4Th4ro/4zkyWiQvsSPqIot+6R1L" >> .env
echo "PESAPAL_CONSUMER_SECRET=Dk2jK6SfNcSk1DQl7+wgs+czslg=" >> .env

echo "✅ Pesapal Live keys updated in .env file!"
