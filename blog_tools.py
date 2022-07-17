import sublime
import sublime_plugin
from typing import Callable, Optional
# from OpenSplit.target_file import TargetFile
from datetime import date

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
    else:
      sublime.message_dialog("No active window found")

  def post_name_given(self, input: str) -> None:
    window = self.window

    if window:
      today = date.today()
      formatted_date = today.strftime("%Y-%m-%d")

      file_name_title: str = input.lower().replace(" ", "-")
      file_name_with_date: str = f"{formatted_date}-{file_name_title}.md"
      blog_title: str = input.title()

      print(f"Blog title: {blog_title}")
      print(f"file_name: {file_name_with_date}")

      if folder := self.get_folder_name():
        file_name: str = f"{folder}/posts/{file_name_with_date}"
        try:
          with open(file_name, 'x') as f: #create only if it does not exist
            f.write("")
        except Exception as e:
          sublime.message_dialog(f"could not create {file_name}: {e}")

        view = self.window.open_file(file_name)
        self.async_check_for_view(view, lambda v: self.insert_snippet(blog_title, v))


      else:
        sublime.message_dialog("Could find current directory")
    else:
      sublime.message_dialog("Could not find Window")

  def async_check_for_view(self, view: sublime.View, callback: Callable[[sublime.View], None], retries: int = 8) -> None:
    if view.is_loading():
      if retries >= 0:
        new_retries = retries - 1
        print(f"waiting for view, retries left: {new_retries}")
        sublime.set_timeout_async(lambda: self.async_check_for_view(view, callback, new_retries), 250)
      else:
        sublime.message_dialog("View is taking too long to load. Giving up.")
    else:
      callback(view)

  def get_folder_name(self) -> Optional[str]:
    window = self.window
    if window:
      variables = window.extract_variables()
      if variables:
        return variables.get('folder') # could be None
      else:
        return None
    else:
      return None

  def insert_snippet(self, title: str, view: sublime.View) -> None:
    window = self.window

    description = title.lower()
    if window and view:
      # There doesn't seem to be a nice way to load snippet content with variables pre-supplied
      # hardcoding this here for now.
      snippet_file = \
f"""---
title: {title}
author: sanjiv sahayam
description: {description}
tags:
comments: true
---

$1
"""
      print(f"view: {view}")

      if view.is_loading():
        print("view is still loading, giving up")
      else:
        print("view had loaded")
        view.run_command("insert_snippet", { "contents":  snippet_file})
    else:
      sublime.message_dialog("Could not find Window or View")
