import sublime
import sublime_plugin
# from typing import Optional
# from OpenSplit.target_file import TargetFile

class BlogToolsCommand(sublime_plugin.WindowCommand):
  def run(self):
    window = self.window

    if window:
      print("found active window")
      #show_input_panel(caption: str, initial_text: str, on_done: Optional[Callable[[str], None]], on_change: Optional[Callable[[str], None]], on_cancel: Optional[Callable[[], None]])
      window.show_input_panel(
        caption = "Blog title",
        initial_text = "<your blog title>",
        on_done = self.post_name_given,
        on_cancel = None,
        on_change = None
      )
      # if (text := self.has_selected_word(view.sel())) is not None:
      #   print(f"found symbol: {text}")
      #   symbol = window.symbol_locations(text, type=sublime.SYMBOL_TYPE_DEFINITION)

      #   if len(symbol) > 0:
      #     target_file = self.get_target_file(symbol[0])
      #     # if the target file open in group 0?
      #      # find file in group 0
      #      # close file in group 0

      #     # open file in group 1
      #     self.create_or_focus_group1(window)
      #     if target_file:
      #       window.open_file(target_file.encoded_str(), sublime.ENCODED_POSITION, group=1)
      #     else:
      #       print("no valid target file")
      #   else:
      #     print("symbol is empty")
      # else:
      #   print("Invalid word selected")
    else:
      print("No active window found")

  def post_name_given(self, input: str) -> None:
    print(f"you said: {input}")

  # def get_target_file(self, first_match: sublime.SymbolLocation) -> TargetFile:
  #   file_name = first_match.path
  #   line = first_match.row
  #   column = first_match.col
  #   target_file = TargetFile(file_name, line, column)
  #   print(f"target_file: {target_file}")
  #   return target_file

  # def create_or_focus_group1(self, window: sublime.Window) -> None:
  #   groups = window.num_groups()
  #   active_group = window.active_group()
  #   if groups > 1:
  #     if active_group == 1:
  #       print("nothing to do. Split 1 is already selected")
  #     else:
  #       window.focus_group(1)
  #   else:
  #     window.run_command('set_layout', { "cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]] })
  #     window.focus_group(1)


  # def has_selected_word(self, selection: sublime.Selection) -> Optional[str]:
  #   if len(selection) > 0:
  #     view = self.view
  #     possible_word = view.substr(view.word(selection[0]))
  #     if possible_word and possible_word.lstrip():
  #       word = possible_word.lstrip()
  #     else:
  #       word = None
  #   else:
  #     word = None

  #   return word
