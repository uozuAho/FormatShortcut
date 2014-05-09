import sublime
import sublime_plugin
import re


PLUGIN_NAME = u"SublimeFormatShortcut"

DEBUG = True


def dbg(msg):
    if DEBUG:
        print("format shortcut: " + msg)


def load_settings():
    return sublime.load_settings(PLUGIN_NAME + '.sublime-settings')


def get_setting(key):
    return load_settings().get(key)


def get_format_command(syntax):
    return get_setting('syntax_formatter_mapping').get(syntax)


class SublimeFormatShortcutCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        syntax = self.get_view_syntax()
        dbg("current view syntax: " + syntax)
        format_command = get_format_command(syntax)
        if format_command is None:
            sublime.error_message(
                PLUGIN_NAME + ": no formatter set for syntax: " + syntax)
        else:
            dbg(syntax + " formatting command: " + format_command)
            self.view.run_command(format_command)

    def get_view_syntax(self):
        # shameless rip from CodeFormatter. Cheers akalongman!
        pattern = re.compile(r"Packages/(.+?)/.+?\.tmLanguage")
        m = pattern.search(self.view.settings().get('syntax'))
        found = ""
        if (m):
            for s in m.groups():
                found = s
                break
        return found.lower()
