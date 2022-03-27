import re

def memo(input, dialog_status):
    if dialog_status == 'memo':
        dialog_status.memo.append(input)
        dialog_status.intent = 'end'

        return ('已经记好啦')