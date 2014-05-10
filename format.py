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


def get_syntax_name(view_syntax_string):
    # shameless rip from CodeFormatter. Cheers akalongman!
    pattern = re.compile(r"Packages/(.+?)/.+?\.tmLanguage")
    m = pattern.search(view_syntax_string)
    found = ""
    if (m):
        for s in m.groups():
            found = s
            break
    return found.lower()


def get_syntax_file(syntax_name):
    if len(syntax_name) > 0:
        # ensure correct case
        syntax_name = syntax_name.lower()
        syntax_name = syntax_name[0].upper() + syntax_name[1:]
        return 'Packages/' + syntax_name + '/' + syntax_name + '.tmLanguage'


def run_format(view, syntax=None):
    if syntax is None:
        syntax = get_syntax_name(view.settings().get('syntax'))
    format_command = get_format_command(syntax)
    if format_command is None:
        sublime.error_message(
            PLUGIN_NAME + ": no formatter set for syntax: " + syntax)
    else:
        dbg("syntax: " + syntax)
        dbg("syntax file: " + get_syntax_file(syntax))
        dbg("running formatter: " + format_command)
        # in case the formatter doesn't run when the view's
        # syntax doesn't match its supported syntaxes, temporarily
        # change the view's syntax while formatting
        tmp = view.settings().get('syntax')
        view.set_syntax_file(get_syntax_file(syntax))
        view.run_command(format_command)
        view.set_syntax_file(tmp)


class SublimeFormatShortcutCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        run_format(self.view)


class FormatShortcutSelectionCommand(sublime_plugin.TextCommand):

    def run(self, edit, syntax=None):
        for region in self.view.sel():
            selectionText = self.view.substr(region)
            tmp = self.view.window().new_file()
            tmp.insert(edit, 0, selectionText)
            if syntax is None:
                syntax = get_syntax_name(self.view.settings().get('syntax'))
            dbg("Running format on selected text, syntax: " + syntax)
            run_format(tmp, syntax)
            newtxt = tmp.substr(sublime.Region(0, tmp.size()))
            self.view.replace(edit, region, newtxt)
            tmp.set_scratch(True)
            self.view.window().focus_view(tmp)
            self.view.window().run_command("close_file")
