class Field:
    START = 'start'
    END = 'end'

    TUID = 'tuid'
    SRC = 'src'
    TARGET = 'target'
    SRC_LANG = "src_lang"
    TARGET_LANG = "target_lang"

class Tag:
    TU = 'tu'
    TUV = 'tuv'
    TUID = 'tuid'
    SEG = 'seg'

class Parameters:
    QUEUE_SIZE = 0
    MAX_WORKERS = 4
    TOPIC = 'rawdata'

class ErrorMessage:
    FILE_NOT_FOUND = 'file_not_found in given path'
    QUEUE_FULL = 'Increase the queue size in config.py'

