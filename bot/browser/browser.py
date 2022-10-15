from datetime import datetime
from typing import Optional, Union, List, Any
from ChromeController import Chrome as ChromeRemoteDebugInterface

from ..errors import ErrorType, BotError

from ..logger import log


class Browser:
    crdi: ChromeRemoteDebugInterface
    mouse_logs_mode: int
    mouse_path_shrink: float
    
    def __init__(self, crdi: ChromeRemoteDebugInterface, mouse_logs_mode: int, mouse_path_shrink: float = 1) -> None:
        self.crdi = crdi
        self.mouse_logs_mode = mouse_logs_mode
        self.mouse_path_shrink = mouse_path_shrink
    
    js_argument = Union[bool, str, int, float, None]
    
    @staticmethod
    def _stringify_js_argument(arg: js_argument) -> str:
        if type(arg) is bool:
            return 'true' if arg == True else 'false'
        if type(arg) is int or type(arg) is float:
            return str(arg)
        if type(arg) is str:
            return f'"{arg}"'
        return 'undefined'

    def create_isolated_world(self) -> None:
        start_time = datetime.now()
        log('Creating Isolated World... ', end_line=False)
        self.crdi.create_isolated_world()
        end_time = datetime.now()
        diff = end_time - start_time
        log(f'Created (took {diff.seconds}.{diff.microseconds // 1000:03}s)')

    def run_js_function(self, function: str, args: List[js_argument] = [], returnByValue: bool = False, awaitPromise: bool = False) -> Any:
        args_string = ', '.join(map(Browser._stringify_js_argument, args))
        expression = f'({function})({args_string})'
        # TODO: self.crdi.world_id check
        return self.crdi.Runtime_evaluate(expression=expression, contextId=self.crdi.world_id, returnByValue=returnByValue, awaitPromise=awaitPromise)

    def go_to_url(self, url: str) -> None:
        # self.crdi.Runtime_evaluate(expression=f'if (window.location.href !== "{url}") window.location.href = "{url}"')
        if self.crdi.get_current_url() != url:
            self.crdi.get(url)

    def node(self,
             name: str,
             selector: Optional[str] = None,
             timeout: int = 5000,
             empty_text_allowed: bool = True,
             remote_object_id: Optional[str] = None,
             required: bool = True,
             not_found_error: Optional[str] = None,
             not_found_error_type: Optional[ErrorType] = None):
        from .node import Node
        return Node(browser=self,
                    name=name,
                    selector=selector,
                    timeout=timeout,
                    empty_text_allowed=empty_text_allowed,
                    remote_object_id=remote_object_id,
                    required=required,
                    not_found_error=not_found_error,
                    not_found_error_type=not_found_error_type)
    
    # Get result object or string error
    def process_js_return(self, result: Any, node_name: str):
        if 'type' in result and result['type'] == 'undefined':
            # TODO: Error handling
            pass
        elif 'result' in result and 'result' in result['result']:
            result = result['result']['result']
            if 'objectId' in result and 'subtype' in result and result['subtype'] == 'node':
                # log('Result is node objectId')
                return self.node(node_name, remote_object_id=result['objectId'])
            if 'type' in result and result['type'] == 'string' and 'value' in result:
                # log('Result is string')
                string: str = result['value']
                return string
            if 'subtype' in result and result['subtype'] == 'error':
                # log('Result is error')
                if 'description' in result:
                    description = str(result['description']).replace('\\n', '\n')
                    raise BotError(f'Error in js function: {description}', ErrorType.JS_EXCEPTION)
                else:
                    raise BotError(f'Error in js function: no description', ErrorType.JS_EXCEPTION)
        log(result)
        raise BotError('Cannot get result from js function', ErrorType.CANNOT_GET_JS_FUNCTION_RESULT)
