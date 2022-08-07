import random
import math
import numpy as np

from datetime import datetime
from typing import Dict, Union, Any, List
from python_ghost_cursor import path # pyright: ignore [reportMissingTypeStubs, reportUnknownVariableType]

from ..browser import Browser
from ..js_scripts.get_element import get_element

from ...errors import BotError
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
                 not_found_error: Union[str, None] = None) -> None:
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
                    raise BotError(f'Required node "{name}" not found' if not not_found_error else not_found_error)
            log(f'Found (took {diff.seconds}.{diff.microseconds // 1000:03}s)')
            self.remote_object_id = object_id
                
    
    def __bool__(self) -> bool:
        return self.remote_object_id != None
    
    def get_property(self, property_name: str) -> str:
        try:
            result: Any = self.browser.crdi.Runtime_getProperties(objectId=self.remote_object_id) # pyright: reportUnknownMemberType=false
            properties = result['result']['result']
            property: Any = next(filter(lambda x: x['name'] == property_name, properties), None) # pyright: reportUnknownArgumentType=false
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

    def click(self, container_css_selector: Union[str, None] = None) -> None:
        start_time = datetime.now()
        try:
            log(f'Clicking {self.name}')
            content_coords = self.get_box_model()['content']
            top_coordinate = content_coords[1]
            right_coordinate = content_coords[2]
            bottom_coordinate = content_coords[5]
            left_coordinate = content_coords[0]
    
            step_1 = datetime.now()
            diff_1 = step_1 - start_time
            if self.mouse_logs_mode > 1:
                log(f'Got box model (took {diff_1.seconds}.{diff_1.microseconds // 1000:03}s)')
            
            element_x_coordinate = random.uniform(left_coordinate, right_coordinate)
            element_y_coordinate = random.uniform(bottom_coordinate, top_coordinate)
            
            step_2 = datetime.now()
            diff_2 = step_2 - step_1
            if self.mouse_logs_mode > 1:
                log(f'Got click coordinates (took {diff_2.seconds}.{diff_2.microseconds // 1000:03}s)')
            
            scroll_amount: int = self.browser.crdi.scroll_to(element_y_coordinate, container_css_selector=container_css_selector, recheck_viewport=True)
            
            step_3 = datetime.now()
            diff_3 = step_3 - step_2
            if self.mouse_logs_mode > 1:
                log(f'Scrolled (took {diff_3.seconds}.{diff_3.microseconds // 1000:03}s)')
            
            current_y_coordinate = element_y_coordinate - scroll_amount
            
            # self.browser.crdi.click_item_at_coords(element_x_coordinate, current_y_coordinate)
            
            full_length: float = 0
            min_step = 0
            max_step = 0
            steps_count = 0
            if self.browser.crdi.x_coordinate != element_x_coordinate and self.browser.crdi.y_coordinate != current_y_coordinate:
                starting_point: Dict[str, float] = {'x': self.browser.crdi.x_coordinate, 'y': self.browser.crdi.y_coordinate}
                ending_point = {'x': element_x_coordinate, 'y': current_y_coordinate}
                route = path(starting_point, ending_point) # pyright: ignore [reportUnknownVariableType]
                steps_count = len(route)
                
                step_4 = datetime.now()
                diff_4 = step_4 - step_3
                if self.mouse_logs_mode > 1:
                    log(f'Generated mouse path ({steps_count} steps) (took {diff_4.seconds}.{diff_4.microseconds // 1000:03}s)')
                
                if self.mouse_path_shrink < 1 and self.mouse_path_shrink >= 0:
                    leave_count = round(steps_count * self.mouse_path_shrink)
                    delete_count = steps_count - leave_count
                    
                    deleting_indecies = np.round(np.linspace(0, steps_count - 1, delete_count, endpoint=False)).astype(int)

                    route = np.delete(route, deleting_indecies) # pyright: ignore [reportUnknownVariableType, reportGeneralTypeIssues]
                    old_steps_count = steps_count
                    steps_count = len(route)
                    log(f'Shrinked mouse path ({100 * self.mouse_path_shrink}%: from {old_steps_count} to {steps_count} steps)')
                    

                step_number = 1
                prev_x: float = self.browser.crdi.x_coordinate
                prev_y: float = self.browser.crdi.y_coordinate
                for step in route: # pyright: ignore [reportUnknownVariableType]
                    step_start_time = datetime.now()
                    new_x: float = step['x']
                    new_y: float = step['y']
                    delta_x = new_x - prev_x
                    delta_y = new_y - prev_y
                    delta_length = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
                    full_length += delta_length
                    if self.mouse_logs_mode > 1:
                        log(f'Step {step_number:03}: [{delta_x:7.3f}, {delta_y:7.3f}], length: {delta_length:6.3f}... ', end_line=False)
                    
                    self.browser.crdi.Input_dispatchMouseEvent(type='mouseMoved', x=step['x'], y=step['y'])
                    
                    step_end_time = datetime.now() - step_start_time
                    seconds = step_end_time.seconds
                    microseconds = step_end_time.microseconds
                    miliseconds_float = seconds * 1000 + microseconds / 1000
                    seconds_float = seconds + (microseconds / 1000000)
                    if seconds_float != 0:
                        speed = (delta_length / seconds_float) / 1000
                    else:
                        speed = 0
                    if self.mouse_logs_mode > 1:
                        log(f'Done (took {miliseconds_float:7.3f}ms) ({speed:5.2f} kpx/s)')
                    
                    if min_step == 0 or min_step > miliseconds_float:
                        min_step = miliseconds_float
                    if max_step == 0 or max_step < miliseconds_float:
                        max_step = miliseconds_float
                    
                    step_number += 1
                    prev_x = new_x
                    prev_y = new_y
            else:
                step_4 = step_3
    
            step_5 = datetime.now()
            diff_5 = step_5 - step_4
            diff_5_seconds_float = diff_5.seconds + (diff_5.microseconds // 1000) / 1000
            if diff_5_seconds_float != 0:
                speed = (full_length / diff_5_seconds_float) / 1000
            else:
                speed = 0
            if self.mouse_logs_mode > 0:
                log(f'Mouse moved (took {diff_5_seconds_float:.3f}s) (length: {full_length:.2f}px. speed: {speed:5.2f} kpx/s)')
                log(f'Steps count: {steps_count}, min: {min_step}ms, avg: {0 if steps_count == 0 else 1000 * diff_5_seconds_float / steps_count:.3f}ms, max: {max_step}ms')

            self.browser.crdi.Input_dispatchMouseEvent(type='mousePressed', x=element_x_coordinate, y=current_y_coordinate, button='left', clickCount=1)
            self.browser.crdi.Input_dispatchMouseEvent(type='mouseReleased', x=element_x_coordinate, y=current_y_coordinate, button='left', clickCount=1)
    
            step_6 = datetime.now()
            diff_6 = step_6 - step_5
            if self.mouse_logs_mode > 1:
                log(f'Mouse clicked (took {diff_6.seconds}.{diff_6.microseconds // 1000:03}s)')
            
            self.browser.crdi.x_coordinate = element_x_coordinate
            self.browser.crdi.y_coordinate = current_y_coordinate
            
        except Exception as e:
            log(f'Error clicking node "{self.name}" [{self.remote_object_id}]')
            raise e
        finally:
            end_time = datetime.now()
            diff = end_time - start_time
            log(f'Click done (took {diff.seconds}.{diff.microseconds // 1000:03}s full)')