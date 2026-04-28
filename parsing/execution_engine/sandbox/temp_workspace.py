import os
import shutil
import tempfile


class TempWorkspace:

    def __init__(self):
        self.base_dir = tempfile.mkdtemp(prefix="exec_")

    def get_path(self):
        return self.base_dir

    def create_file(self, filename: str, content: str) -> str:
        file_path = os.path.join(self.base_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return file_path

    def cleanup(self):
        try:
            shutil.rmtree(self.base_dir)
        except Exception:
            pass