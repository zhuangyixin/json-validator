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

fail_file_names = list()
success_file_names = list()
for json_name, json_content in json_dict.items():
    try:
        output_json = validator.validate_str(json_content)
        file_manager.write_file(json_name, output_json)
        success_file_names.append(json_name)
        # logging.info("Verify success, output file:\n{}".format(os.path.join(output_path, json_name)))
    except JsonValidateError as e:
        fail_file_names.append(json_name)
        logging.error(
            "Verify fail, file name: {}, error message: {}".format(json_name, str(e)))

logging.info("*********** Result ***********")
logging.info("Success file here: {}".format(success_file_names))
logging.warning("Fail file here: {}".format(fail_file_names))
