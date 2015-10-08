==============
Open-GridView
==============

An application insipired by PowerShell's `Out-GridView <https://technet.microsoft.com/en-us/library/hh849920.aspx>`_
.

Implemented on Gnome using GTK

Input is passed via STDIN or via filenames in argument. Every file is assigned a window and a thread in charge of reading that file and parsing it.

Also check out my post on it: http://blog.backslasher.net/open-gridview.html

Parsing
-------
These different types of input formatting are currently supported:

* ``autosplit`` (default), which uses ``re.split`` to create different columns from every row.
    Default separator is ``\s+`` which is good for space-separated items.

    Separator can contains capturing groups for `interesting results <https://docs.python.org/2/library/re.html#re.split>`_
* ``csv``, with configurable column separators
* ``line_json``, where every line is considered a single JSON object (Line delimited JSON)

Items are displayed immediately when parsed

Additional features
-------------------
* Clipboard support. Copies as CSV to allow easy pasting in spreadsheet software
* Simple text filtering


TODO
----
* act as pipeline middle (and not just terminator), meaning that you can select items and click "OK" to make it send the items to STDOUT
* Support advanced filtering (e.g. regex, specific columns)
* Support hiding and re-ordering columns
* show progress icon when stdin isn't EOF yet
