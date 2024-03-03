from sw2.task.print import sw2_parser_task_print, sw2_task_print
from sw2.task.test import sw2_parser_task_test, sw2_task_test
from sw2.task.update import sw2_parser_task_update, sw2_task_update

task_function_map = {
    'print': { 'function': sw2_task_print, 'parser': sw2_parser_task_print },
    'test': { 'function': sw2_task_test, 'parser': sw2_parser_task_test},
    'update': { 'function': sw2_task_update, 'parser': sw2_parser_task_update },
}