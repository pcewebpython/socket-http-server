#!/usr/bin/env python

"""
make_time.py

simple script that returns and HTML page with the current time
"""

import datetime

time_str = datetime.datetime.now().isoformat()

html = """<!DOCTYPE html>
<html>
<body>
<h2> The time is: </h2>
<p> %s </p>
</body>
</html>""" % time_str

print(html)
