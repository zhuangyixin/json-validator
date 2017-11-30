from lib.error.json_validate_error import ErrorMsg, JsonValidateError
from lib.utils.common_utils import top, append, build, is_number, is_empty


class JsonValidator(object):
    sign_map = {
        ":": "{",
        ",": [":", "["],
        "}": ":",
        "]": "["
    }

    def __init__(self):
        self.buffer = list()
        self.output = str()
        self.sign_stack = list()

    def validate(self, json: list):
        self.validate_not_empty(json)
        for i in range(0, len(json)):
            for j in range(0, len(json[i])):
                try:
                    ch = json[i][j]
                    self.insert(ch)
                except JsonValidateError as e:
                    self.clean()
                    raise JsonValidateError(ErrorMsg.error_format.format(str(e), i, j))
                except Exception as e:
                    self.clean()
                    raise JsonValidateError(ErrorMsg.unknown_error.format(str(e), i, j))
        if not is_empty(self.buffer) or not is_empty(self.sign_stack):
            self.clean()
            raise JsonValidateError(ErrorMsg.open_sign_error)
        result = self.output
        self.clean()
        return result

    def is_begin_mark(self, ch: str):
        if ch in ["{", "["] and is_empty(self.buffer):
            return True
        else:
            return False

    def process_sign(self, ch):
        if ch == ":":
            self.sign_stack.append(ch)
        elif ch in ",]" and top(self.sign_stack) in self.sign_map[ch][0]:
            self.sign_stack.pop()
        elif ch == "," and top(self.sign_stack) == "[":
            pass
        # elif ch == "]" and top(self.sign_stack) == "[":
        #     self.sign_stack.pop()
        elif ch == "}" and top(self.sign_stack) == ":":
            self.sign_stack.pop()
            if top(self.sign_stack) == "{":
                self.sign_stack.pop()
            else:
                raise JsonValidateError("{ need to be closed by }")
        else:
            raise JsonValidateError("Unknow Exception")

    def insert(self, ch: str):
        if self.is_begin_mark(ch):
            self.sign_stack.append(ch)
            self.output += ch
            return

        if ch in self.sign_map:
            if self.can_be_output(ch):
                self.output += build(self.buffer)
                self.output += ch
                self.buffer.clear()
                self.process_sign(ch)
                return
        if ch in "\"\\":
            self.buffer.append(ch)
            return
        if not is_empty(self.buffer):
            append(self.buffer, ch)
        elif is_number(ch):
            append(self.buffer, ch)
        else:
            self.output += ch

    @staticmethod
    def validate_not_empty(json: list):
        if len(json) is 0 or len(json[0]) is 0:
            raise JsonValidateError(ErrorMsg.empty_error)

    def can_be_output(self, ch):
        buffer_len = len(self.buffer)
        can_be_output = False
        # if empty
        if ch in ",]}" and buffer_len is 0:
            can_be_output = True
        # if buffer is a number
        if buffer_len is 1 and is_number(self.buffer[0].strip()):
            can_be_output = True
        # if buffer is a string
        if buffer_len > 1 and self.buffer[0][0] == "\"" and top(self.buffer).strip() == "\"":
            can_be_output = True
        if can_be_output and top(self.sign_stack) not in self.sign_map[ch]:
            raise JsonValidateError(ErrorMsg.no_match_error)
        return can_be_output

    def clean(self):
        self.output = str()
        self.sign_stack = list()
        self.buffer = list()
