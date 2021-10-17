# Cloudflare Dynamic DNS Python

A simple Python script to dynamicially update a DNS record on Cloudflare.

I couldn't find a updated DDNS script for Cloudflare's DNS services that worked on my Window machine so I made one myself.

## Getting Started

### Dependencies

* Python 3+

### Executing script
1. Copy files, and then rename sample config to config.json
2. Fill in a Cloudflare API token with Zone read and DNS edit premissions in config
3. Use the get-ids&period;py to fill in the rest of config or do it manually
4. Use update-record&period;py (schedule it to run as a service or a shortcut in startup folder, etc..)



