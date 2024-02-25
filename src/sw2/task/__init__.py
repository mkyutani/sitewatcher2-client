from sw2.task.list import sw2_parser_task_list, sw2_task_list
from sw2.task.print import sw2_parser_task_print, sw2_task_print

task_function_map = {
    'list': { 'function': sw2_task_list, 'parser': sw2_parser_task_list },
    'print': { 'function': sw2_task_print, 'parser': sw2_parser_task_print }
}