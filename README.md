# who's there?

this is where i play with dns-sd using avahi.

## pipe.py

this takes input from avahi-browse and generates output from whatever is
resolved. it currently doesn't know about removals, so keep this in mind.

the script either creates coloured text output or html output.

text:
```
name @ hostname.local / 127.0.0.1
service: _service._tcp
property: value
----------
```

html:
```
# i recommend -k/--no-db-lookup if you don't want human-friendly names for
# services
avahi-browse -artpk ./pipe.py html > test.html
```

i plan to show the html output to my friends and have fun spotting people
on wifi.
