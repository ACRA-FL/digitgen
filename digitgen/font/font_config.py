import os
from os.path import dirname, abspath

from ..utils.helper import download_font_from_gdrive


class FontConfig:
    def __init__(self, font_type="terminal-grotesque-regular"):
        font_dir = dirname(abspath(__file__))
        self.font_dir = os.path.join(font_dir, "fonts")
        os.makedirs(self.font_dir, exist_ok=True)
        self.font_type = font_type
        self.download_font_file()

    @staticmethod
    def get_available_fonts():
        return ["terminal-grotesque-regular"]

    def get_font_file_location(self):
        if self.font_type == "terminal-grotesque-regular":
            return os.path.join(self.font_dir, "terminal-grotesque-regular.ttf")

    def download_font_file(self):
        if self.font_type == "terminal-grotesque-regular":
            path_to_download = os.path.join(self.font_dir, "terminal-grotesque-regular.ttf")
            file_id = "1N68bQ4s2bFkH-y9ZWbzs7XoXddhUDY1V"

            if not os.path.exists(path_to_download):
                if download_font_from_gdrive(file_id, path_to_download):
                    print(f"Downloaded font type {self.font_type}")
                else:
                    print(f"Download Failed")

