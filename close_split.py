import sublime
import sublime_plugin

class CloseSplitCommand(sublime_plugin.WindowCommand):
  def run(self) -> None:
    window = self.window
    groups = window.num_groups()

    if groups == 2:
      group_1_views = window.views_in_group(1)
      for v in group_1_views:
        v.close()

      window.run_command('set_layout', {
                                        "cols": [0.0, 1.0],
                                        "rows": [0.0, 1.0],
                                        "cells": [[0, 0, 1, 1]]
                                       }
      )
    else:
      sublime.message_dialog("OpenSplit: Need exactly two groups present. Aborting")
