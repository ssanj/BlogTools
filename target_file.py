from typing import NamedTuple

class TargetFile(NamedTuple):
  file_name: str
  row: int
  col: int

  def encoded_str(self) -> str:
    return f"{self.file_name}:{self.row}:{self.col}"
