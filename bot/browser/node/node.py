from datetime import datetime
from typing import Union, Any, List

from ..browser import Browser
from ..js_scripts.get_element import get_element

from ...errors import ErrorType, BotError
from ...logger import log

class Node:
    name: str
    remote_object_id: Union[str, None]
    mouse_logs_mode: int
    mouse_path_shrink: float

    def __init__(self,
                 browser: Browser,
                 name: str,
                 selector: Union[str, None] = None,
                 timeout: int = 5000,
                 empty_text_allowed: bool = True,
                 remote_object_id: Union[str, None] = None,
                 required: bool = True,
                 not_found_error: Union[str, None] = None,
                 not_found_error_type: Union[ErrorType, None] = None) -> None:
        self.browser = browser
        self.name = name
        self.mouse_logs_mode = browser.mouse_logs_mode
        self.mouse_path_shrink = browser.mouse_path_shrink
        if remote_object_id:
            self.remote_object_id = remote_object_id
            return
        else:
            if not selector:
                raise Exception('Must provide remote_object_id or selector argument for Node constructor')
            try:
                start_time = datetime.now()
                log(f'Waiting for {name}... ', end_line=False)
                result = self.browser.run_js_function(get_element, [selector, timeout, empty_text_allowed], awaitPromise=True)
                if 'subtype' in result['result']['result'] and result['result']['result']['subtype'] == 'null':
                    object_id = None
                else:
                    object_id = result['result']['result']['objectId']
            except Exception as e:
                log(f'Error constructing node "{name}"')
                raise e

            end_time = datetime.now()
            diff = end_time - start_time
            if not object_id:
                log(f'Not found (took {diff.seconds}.{diff.microseconds // 1000:03}s)')
                if not required:
                    self.remote_object_id = None
                    return
                else:
                    raise BotError(f'Required node "{name}" not found' if not not_found_error else not_found_error, not_found_error_type if not_found_error_type else ErrorType.SOME_ELEMENT_NOT_FOUND)
            log(f'Found (took {diff.seconds}.{diff.microseconds // 1000:03}s)')
            self.remote_object_id = object_id
                
    
    def __bool__(self) -> bool:
        return self.remote_object_id != None
    
    def get_property(self, property_name: str) -> str:
        try:
            result: Any = self.browser.crdi.Runtime_getProperties(objectId=self.remote_object_id)
            properties = result['result']['result']
            property: Any = next(filter(lambda x: x['name'] == property_name, properties), None)
            # if property == None:
            #     log(f'Node "{self.name}" [{self.remote_object_id}] has no property {property_name}')
            #     return None
            return str(property['value']['value'])
        except Exception as e:
            log(f'Error getting property {property_name} of node "{self.name}" [{self.remote_object_id}]')
            print(type(e))
            raise e

    def get_class_list(self) -> Union[List[str], None]:
        try:
            result: Any = self.browser.crdi.Runtime_getProperties(objectId=self.remote_object_id)
            properties = result['result']['result']
            property: Any = next(filter(lambda x: x['name'] == 'classList', properties))
            class_list_object: Any = self.browser.crdi.Runtime_getProperties(objectId=property['value']['objectId'])
            class_list_object_properties = class_list_object['result']['result']
            class_list_property = next(filter(lambda x: x['name'] == 'value', class_list_object_properties), None)
            if not class_list_property:
                return None
            return str(class_list_property['value']['value']).strip().split()
        except Exception as e:
            log(f'Error getting class list of node "{self.name}" [{self.remote_object_id}]')
            raise e
    
    def get_box_model(self) -> Any:
        try:
            result: Any = self.browser.crdi.DOM_getBoxModel(objectId=self.remote_object_id)
            # getBoundingClientRect()
            # left-top, right-top, right-bottom, left-bottom
            return result['result']['model']
        except Exception as e:
            log(f'Error getting box model of node "{self.name}" [{self.remote_object_id}]')
            raise e
        
        
    def scroll_to(self, element_coordinate=None, container_css_selector=None, scrollable_section_css_selector=None, amount=None) -> Any:
        from ._scroll_to import scroll_to
        return scroll_to(self, element_coordinate=element_coordinate, container_css_selector=container_css_selector, scrollable_section_css_selector=scrollable_section_css_selector, amount=amount)
        

    def click(self, scroll=True, container_css_selector: Union[str, None] = None, scrollable_section_css_selector: Union[str, None] = None) -> None:
        from ._click import click
        return click(self, scroll=scroll, container_css_selector=container_css_selector, scrollable_section_css_selector=scrollable_section_css_selector)