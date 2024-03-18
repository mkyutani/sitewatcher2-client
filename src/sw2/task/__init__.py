from sw2.task.command_print import sw2_parser_task_print, sw2_task_print
from sw2.task.command_update import sw2_parser_task_update, sw2_task_update

task_function_map = {
    'print': { 'function': sw2_task_print, 'parser': sw2_parser_task_print },
    'update': { 'function': sw2_task_update, 'parser': sw2_parser_task_update },
}