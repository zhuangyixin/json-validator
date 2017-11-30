import logging
import os


from lib.error.json_validate_error import JsonValidateError
from lib.json_validator import JsonValidator
from lib.utils.file_manager import FileManager



base_path = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(base_path, "source")
output_path = os.path.join(base_path, "output")


file_manager = FileManager(source_path, output_path)
source_file_names = file_manager.list_input_file(".json")
json_dict = file_manager.read_files(source_file_names)

validator = JsonValidator()
for json_name, json_content in json_dict.items():
    try:
        output_json = validator.validate(json_content)
        file_manager.write_file(json_name, output_json)
        logging.info("Verify success, output file:\n{}".format(os.path.join(output_path, json_name)))
    except JsonValidateError as e:
        logging.error("Verify error, output file:\n{}\nerror message: {}".format(os.path.join(output_path,json_name),str(e)))
