import base64
from datetime import datetime
from typing import Optional, Union, List, Any, Type
from ChromeController import Chrome as ChromeRemoteDebugInterface

from ..errors import ErrorType, BotError

from ..settings import Settings
from ..logger import log


class Browser:
    crdi: ChromeRemoteDebugInterface
    settings: Settings
    
    def __init__(self, crdi: ChromeRemoteDebugInterface, settings: Settings) -> None:
        self.crdi = crdi
        self.settings = settings
    
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

    def run_js_function(self, function: str, args: List[js_argument] = [], returnByValue: bool = False, awaitPromise: bool = False, globalContext: bool = False) -> Any:
        args_string = ', '.join(map(Browser._stringify_js_argument, args))
        expression = f'({function})({args_string})'
        # TODO: self.crdi.world_id check
        if globalContext:
            return self.crdi.Runtime_evaluate(expression=expression, returnByValue=returnByValue, awaitPromise=awaitPromise)
        else:
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
            if 'type' in result:
                if result['type'] == 'string' and 'value' in result:
                    # log('Result is string')
                    string: str = result['value']
                    return string
                if result['type'] == 'number' and 'value' in result:
                    # log('Result is number')
                    number: float = result['value']
                    return number
                if result['type'] == 'object':
                    if 'subtype' in result:
                        if result['subtype'] == 'node' and 'objectId' in result:
                            # log('Result is node objectId')
                            return self.node(node_name, remote_object_id=result['objectId'])
                        if result['subtype'] == 'error':
                            # log('Result is error')
                            if 'description' in result:
                                description = str(result['description']).replace('\\n', '\n')
                                raise BotError(f'Error in js function: {description}', ErrorType.JS_EXCEPTION)
                            else:
                                raise BotError(f'Error in js function: no description', ErrorType.JS_EXCEPTION)
                raise BotError('Unknown return type of js function', ErrorType.CANNOT_GET_JS_FUNCTION_RESULT, { 'return_type': result['type'], 'return_subtype': result['subtype'], 'result': result})
        log(result)
        raise BotError('Cannot get result from js function', ErrorType.CANNOT_GET_JS_FUNCTION_RESULT, {'result': result})
    
    def take_screenshot(self, path: str, fullPage = False) -> None:
        if fullPage:
            metrics = self.crdi.Page_getLayoutMetrics()
            width, height = metrics['result']['contentSize']['width'], metrics['result']['contentSize']['height']
            self.crdi.Emulation_setVisibleSize(width=width, height=height)
            log(f'Seting width/height to {width}/{height}')
        resp = self.crdi.Page_captureScreenshot()
        log('Got metrics')
        assert 'result' in resp
        assert 'data' in resp['result']
        imgdat = base64.b64decode(resp['result']['data'])
        log('Decoded base64')
        with open(path, 'wb') as file:
            file.write(imgdat)
        log('File written')

    def show_click_target(self,
                          x_coordinate: float,
                          y_coordinate: float,
                          left_boundary_coordinate: float,
                          right_boundary_coordinate: float,
                          top_boundary_coordinate: float,
                          bottom_boundary_coordinate: float) -> None:
        function = '''
(x, y) => {
    const radius = 20;
    const color = 'red';
    timeout = 10000;
    delay = 100;

    const targetWrapperElement = document.createElement('div');
    targetWrapperElement.style.position = 'fixed';
    targetWrapperElement.style.left = `${x - radius / 2}px`;
    targetWrapperElement.style.top = `${y - radius / 2}px`;
    targetWrapperElement.style.zIndex = 100000;
    targetWrapperElement.style.width = `${radius + 1}px`;
    targetWrapperElement.style.height = `${radius + 1}px`;
    targetWrapperElement.style.display = 'flex';
    targetWrapperElement.style.justifyContent = 'center';
    targetWrapperElement.style.alignItems = 'center';
    targetWrapperElement.style.border = `2px solid ${color}`;
    targetWrapperElement.style.borderRadius = `${Math.floor(radius / 2) + 1}px`;
    targetWrapperElement.style.pointerEvents = 'none';
    targetWrapperElement.style.transition = `border-color ${timeout - delay}ms`;

    const targetElement = document.createElement('div');
    targetElement.style.width = '1px';
    targetElement.style.height = '1px';
    targetElement.style.backgroundColor = color;

    targetWrapperElement.appendChild(targetElement);
    document.body.appendChild(targetWrapperElement);
    setTimeout(() => {
        targetWrapperElement.style.borderColor = 'transparent';
    }, delay);
    setTimeout(() => {
        targetWrapperElement.remove();
    }, timeout);
}
'''
        self.run_js_function(function, [x_coordinate, y_coordinate])
        function = '''
(left, right, top, bottom) => {
    const color = 'red';
    timeout = 10000;
    delay = 100;

    const boundaryElement = document.createElement('div');
    boundaryElement.style.position = 'fixed';
    boundaryElement.style.left = `${left}px`;
    boundaryElement.style.width = `${right - left}px`;
    boundaryElement.style.top = `${top}px`;
    boundaryElement.style.height = `${bottom - top}px`;
    boundaryElement.style.zIndex = 100000;
    boundaryElement.style.border = `1px solid ${color}`;
    boundaryElement.style.pointerEvents = 'none';
    boundaryElement.style.transition = `border-color ${timeout - delay}ms`;

    document.body.appendChild(boundaryElement);
    setTimeout(() => {
        boundaryElement.style.borderColor = 'transparent';
    }, delay);
    setTimeout(() => {
        boundaryElement.remove();
    }, timeout);
}
'''
        self.run_js_function(function, [left_boundary_coordinate, right_boundary_coordinate, top_boundary_coordinate, bottom_boundary_coordinate])