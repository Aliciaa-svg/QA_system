import re

def memo(input, dialog_status):
    if dialog_status.memo_process == 'start':
        dialog_status.memo_process = 'record'
        return ('要记下什么呢')
    elif dialog_status.memo_process == 'record':
        dialog_status.memo.append(input)
        dialog_status.intent = 'end'
        return ('记好啦')

def memo_check(input, dialog_status):
    if dialog_status.memo_process == 'start':
        dialog_status.intent = 'end'
        if dialog_status.memo == []:
            return ('备忘录是空的耶')
        return dialog_status.memo

def memo_delete(input, dialog_status):
    if dialog_status.memo_process == 'start':
        dialog_status.memo = []
        dialog_status.intent = 'end'
        return ('备忘录清空啦')
    