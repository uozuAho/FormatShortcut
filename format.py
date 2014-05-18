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
    spl = view_syntax_string.split('/')
    if len(spl) > 1:
        return spl[1]


def get_syntax_file(syntax_name):
    if len(syntax_name) > 0:
        return 'Packages/' + syntax_name + '/' + syntax_name + '.tmLanguage'


# Return the indentation of a region as whitespace characters
def get_region_indentation(view, region):
    # Return the leading whitespace of the first line of the region:
    first_line = view.substr(view.line(region.begin()))
    return get_leading_whitespace(first_line)


def get_leading_whitespace(string):
    return string[:-len(string.lstrip())]


def format_view(view, syntax):
    format_command = get_format_command(syntax)
    if format_command is None:
        sublime.error_message(
            PLUGIN_NAME + ": no formatter set for syntax: " + syntax)
    else:
        dbg("running formatter: " + format_command)
        # in case the formatter doesn't run when the view's
        # syntax doesn't match its supported syntaxes, temporarily
        # change the view's syntax while formatting
        tmp = view.settings().get('syntax')
        view.set_syntax_file(get_syntax_file(syntax))
        view.run_command(format_command)
        view.set_syntax_file(tmp)


class FormatShortcutCommand(sublime_plugin.TextCommand):

    def run(self, edit, syntax=None):
        if syntax is None:
            syntax = get_syntax_name(self.view.settings().get('syntax'))
        dbg("syntax: " + syntax)
        dbg("syntax file: " + get_syntax_file(syntax))
        if not self.is_text_selected():
            format_view(self.view, syntax)
        else:
            dbg("Formatting selected text, syntax: " + syntax)
            for region in self.view.sel():
                self.format_selection(edit, region, syntax)

    def is_text_selected(self):
        if len(self.view.sel()) == 1:
            if self.view.sel()[0].empty():
                return False
        return True

    def format_selection(self, edit, region, syntax):
        selected_text = self.view.substr(region)
        temp_view = self.view.window().new_file()
        temp_view.insert(edit, 0, selected_text)
        format_view(temp_view, syntax)
        newtxt = temp_view.substr(sublime.Region(0, temp_view.size()))
        self.view.replace(edit, region, newtxt)
        temp_view.set_scratch(True)
        self.view.window().focus_view(temp_view)
        self.view.window().run_command("close_file")
