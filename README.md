SublimeFormatShortcut
=====================

One command/shortcut to format any syntax in Sublime Text.
Chooses a formatter based on current syntax highlighting setting.

Note: doesn't include formatters, these must be installed separately.


Configuration
-------------
Syntaxes are mapped to formatters in the settings file, under the
setting "syntax_formatter_mapping". Change this mapping as you please -
formatters not included (install separately).


TODO
----
- Format selection: keep indentation
- Auto-install necessary formatter plugins?
- Support standalone formatters (not sublime plugins)