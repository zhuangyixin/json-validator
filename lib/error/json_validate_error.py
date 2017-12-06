class JsonValidateError(Exception):
    pass


class ErrorMsg:
    empty_error = "Json cannot be empty."
    syntax_error = "Json element should be string or number."
    list_error = "List cannot contains key-value pair."
    dict_error = "Dictionary need a key."
    map_error = "{} need to close."
    error_format = "{} located in row {}, column {}."
    unknown_error = "{} unknown error in row{}, column {}."
    open_sign_error = "Element need to be close."
    no_match_error = "Sign not match."
