import sublime
import sublime_plugin


PLUGIN_NAME = u"SublimeFormatShortcut"


def load_settings():
    return sublime.load_settings(PLUGIN_NAME + '.sublime-settings')


def get_setting(key):
    return load_settings().get(key)


class FormatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print("format shortcut: not implemented...")
        self.view.run_command('pep8_autoformat')
