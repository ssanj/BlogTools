import sublime
import sublime_plugin
from typing import Callable, Optional
from datetime import date
from xml.dom.minidom import parseString

class BlogToolsCommand(sublime_plugin.WindowCommand):
  def run(self):
    window = self.window

    if window:
      print("found active window1")
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

      snippet_file_path_op = self.get_snippet_file_name("meta_md")

      if snippet_file_path_op is not None:
        snippet_file_path = snippet_file_path_op
        print(f"snippet file path: {snippet_file_path}")
        try:

          with open(snippet_file_path, 'r') as snippet_file:
            xml_content = snippet_file.read()

          template_content_op = self.get_snippet_content(xml_content)
          if template_content_op is not None:
            template_content = template_content_op.lstrip().rstrip()
            print(f"template_content: {template_content}")
            expanded_snippet = sublime.expand_variables(template_content, {"1": blog_title, "2": blog_title.lower(), "3": "", "4": "inspiration awaits..."})
            print(f"expanded snippet: {expanded_snippet}")
            if folder := self.get_folder_name():
              file_name: str = f"{folder}/data/posts/{file_name_with_date}"
              try:
                with open(file_name, 'x') as f: #create only if it does not exist
                  f.write(expanded_snippet)
              except Exception as e:
                sublime.message_dialog(f"could not create {file_name}: {e}")

              lines = len(template_content.split('\n'))
              print(f"lines: {lines}")
              view = self.window.open_file(f"{file_name}:{lines}:0", sublime.ENCODED_POSITION)
              # self.async_check_for_view(view, lambda v: self.insert_snippet(blog_title, v))
            else:
              sublime.message_dialog("Could find current directory")
          else:
            sublime.message_dialog("Template content is None")

        except Exception as e:
          sublime.message_dialog(f"Could find load snippet file: {e}")
      else:
        print(f"snippet file path is None")
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

  def get_snippet_file_name(self, snippet_name: str) -> Optional[str]:
    window = self.window

    if window:
      return sublime.expand_variables(f"$packages/User/snippets/{snippet_name}.sublime-snippet", window.extract_variables())
    else:
      sublime.message_dialog("Could not find Window")
      return None

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

  def get_snippet_content(self, snippet_template_content: str) -> Optional[str]:
    try:
        result: str = \
          parseString(snippet_template_content) \
          .getElementsByTagName('content')[0] \
          .firstChild \
          .wholeText
        return result
    except Exception as e:
      print(f"Could not parse XML: {snippet_template_content} because of: {e}")
      return None
