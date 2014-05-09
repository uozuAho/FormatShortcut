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


def get_syntax(view_syntax_string):
    # shameless rip from CodeFormatter. Cheers akalongman!
    pattern = re.compile(r"Packages/(.+?)/.+?\.tmLanguage")
    m = pattern.search(view_syntax_string)
    found = ""
    if (m):
        for s in m.groups():
            found = s
            break
    return found.lower()


def test():
    sublime.Window.new_file()


class SublimeFormatShortcutCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        syntax = get_syntax(self.view.settings().get('syntax'))
        dbg("current view syntax: " + syntax)
        format_command = get_format_command(syntax)
        if format_command is None:
            sublime.error_message(
                PLUGIN_NAME + ": no formatter set for syntax: " + syntax)
        else:
            dbg(syntax + " formatting command: " + format_command)
            self.view.run_command(format_command)


class FormatShortcutSelectionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sel = self.view.sel()
        region1 = sel[0]
        selectionText = self.view.substr(region1)
        tmp = self.view.window().new_file()
        tmp.insert(edit, 0, selectionText)
        tmp.set_syntax_file(self.view.settings().get('syntax'))
        tmp.run_command('sublime_format_shortcut')
        newtxt = tmp.substr(sublime.Region(0, tmp.size()))
        self.view.replace(edit, region1, newtxt)
        tmp.set_scratch(True)
        self.view.window().focus_view(tmp)
        self.view.window().run_command("close_file")
