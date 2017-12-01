import logging
import os


class FileManager:
    def __init__(self, input_dir: str, output_dir: str, encoding="utf-8"):
        self.encoding = encoding
        self.input_dir = input_dir
        self.output_dir = output_dir

    def read_files_in_line(self, file_names: list) -> dict:
        result = dict()
        for file_name in file_names:
            with open(file=os.path.join(self.input_dir, file_name), encoding=self.encoding) as file:
                result[file_name] = file.readlines()
        return result

    def read_files(self, file_names: list) -> dict:
        result = dict()
        for file_name in file_names:
            file_content = self.read_file(file_name)
            result[file_name] = file_content
        return result

    def read_file(self, file_name: str) -> list:
        with open(file=os.path.join(self.input_dir, file_name), encoding=self.encoding) as file:
            result = file.read()
        return result

    def write_file(self, json_name: str, json_content):
        with open(file=os.path.join(self.output_dir, json_name), mode="w", encoding=self.encoding) as file:
            file.write(json_content)

    def list_input_file(self, suffix="") -> list:
        file_names = os.listdir(self.input_dir)
        file_names = [file_name for file_name in file_names if file_name.endswith(suffix)]
        info_message = "Source directory: {}\nFile list: {}\n"
        logging.info(info_message.format(self.input_dir, file_names))
        return file_names
