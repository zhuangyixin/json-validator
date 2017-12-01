import logging
import re

from lib.error.json_validate_error import JsonValidateError, ErrorMsg


def top(buffer: list):
    top_index = len(buffer) - 1
    if top_index == -1:
        raise JsonValidateError("Cannot top a empty list.")
    return buffer[top_index]


def append(buffer: list, ch: str):
    if len(buffer) is 0:
        buffer.append(ch)
    else:
        item = buffer.pop() + ch
        buffer.append(item)


def build(buffer: list):
    if is_empty(buffer):
        return ""
    output = top(buffer)
    buffer_len = len(buffer)
    if buffer_len is 1 and is_number(output.strip()):
        pass
    elif buffer_len > 1 and is_str(buffer):
        output = buffer[0]
        if buffer_len > 2:
            for i in range(1, buffer_len - 1):
                if i < buffer_len - 2 and buffer[i] == "\\":
                    if buffer[i + 1][0] in "\"":
                        continue
                    elif buffer[i + 1][0] in "\\":
                        output += buffer[i]
                        continue
                output += "\\"
                output += buffer[i]
            logging.warning("change {} to {}".format("".join(buffer), output + top(buffer)))
        output += top(buffer)
    else:
        raise JsonValidateError(ErrorMsg.syntax_error)
    return output


def is_number(number_str: str):
    regex_for_number = re.compile(r'^[-]?[0-9]?\.?[0-9]+$')
    if regex_for_number.match(number_str):
        return True
    return False


def is_str(buffer: list):
    if top(buffer).strip() == "\"" and buffer[0][0] == "\"":
        return True
    return False


def is_empty(buffer: list):
    return True if len(buffer) is 0 else False
