
import math
import random
import numpy as np

from datetime import datetime
from python_ghost_cursor import path
from typing import Optional, Dict

from . import Node

from ... import logger

def click(self: Node, container_css_selector: Optional[str] = None) -> None:
    start_time = datetime.now()
    try:
        logger.log(f'Clicking {self.name}')
        content_coords = self.get_box_model()['content']
        top_coordinate = content_coords[1]
        right_coordinate = content_coords[2]
        bottom_coordinate = content_coords[5]
        left_coordinate = content_coords[0]

        step_1 = datetime.now()
        diff_1 = step_1 - start_time
        if self.mouse_logs_mode > 1:
            logger.log(f'Got box model (took {diff_1.seconds}.{diff_1.microseconds // 1000:03}s)')
        
        element_x_coordinate = random.uniform(left_coordinate, right_coordinate)
        element_y_coordinate = random.uniform(bottom_coordinate, top_coordinate)
        
        step_2 = datetime.now()
        diff_2 = step_2 - step_1
        if self.mouse_logs_mode > 1:
            logger.log(f'Got click coordinates (took {diff_2.seconds}.{diff_2.microseconds // 1000:03}s)')
        
        scroll_amount: int = self.browser.crdi.scroll_to(element_y_coordinate, container_css_selector=container_css_selector)
        
        step_3 = datetime.now()
        diff_3 = step_3 - step_2
        if self.mouse_logs_mode > 1:
            logger.log(f'Scrolled (took {diff_3.seconds}.{diff_3.microseconds // 1000:03}s)')
        
        current_y_coordinate = element_y_coordinate - scroll_amount
        
        # self.browser.crdi.click_item_at_coords(element_x_coordinate, current_y_coordinate)

        script = '''
(top, right, bottom, left) => {
console.log('Box');
console.log(left, right, top, bottom);

box = document.createElement('div');
box.style.position = 'absolute';
box.style.left = `${left}px`;
box.style.top = `${top}px`;
box.style.width = `${right - left}px`;
box.style.height = `${bottom - top}px`;
box.style.border = '2px solid blue';
box.style.pointerEvents = 'none';
console.log(box);
document.body.appendChild(box);
console.log(box);
setTimeout(() => {
    box.remove();
}, 5000);
}
'''
        self.browser.run_js_function(script, [top_coordinate - scroll_amount, right_coordinate, bottom_coordinate - scroll_amount, left_coordinate])

        full_length: float = 0
        min_step = 0
        max_step = 0
        steps_count = 0
        if self.browser.crdi.x_coordinate != element_x_coordinate and self.browser.crdi.y_coordinate != current_y_coordinate:
            starting_point: Dict[str, float] = {'x': self.browser.crdi.x_coordinate, 'y': self.browser.crdi.y_coordinate}
            ending_point = {'x': element_x_coordinate, 'y': current_y_coordinate}
            route = path(starting_point, ending_point)
            steps_count = len(route)
            
            step_4 = datetime.now()
            diff_4 = step_4 - step_3
            if self.mouse_logs_mode > 1:
                logger.log(f'Generated mouse path ({steps_count} steps) (took {diff_4.seconds}.{diff_4.microseconds // 1000:03}s)')
            
            if self.mouse_path_shrink < 1 and self.mouse_path_shrink >= 0:
                leave_count = round(steps_count * self.mouse_path_shrink)
                delete_count = steps_count - leave_count
                
                deleting_indecies = np.round(np.linspace(0, steps_count - 1, delete_count, endpoint=False)).astype(int)

                route = np.delete(route, deleting_indecies) # pyright: ignore [reportGeneralTypeIssues]
                old_steps_count = steps_count
                steps_count = len(route)
                logger.log(f'Shrinked mouse path ({100 * self.mouse_path_shrink}%: from {old_steps_count} to {steps_count} steps)')
                

            step_number = 1
            prev_x: float = self.browser.crdi.x_coordinate
            prev_y: float = self.browser.crdi.y_coordinate
            for step in route:
                step_start_time = datetime.now()
                new_x: float = step['x']
                new_y: float = step['y']
                delta_x = new_x - prev_x
                delta_y = new_y - prev_y
                delta_length = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
                full_length += delta_length
                if self.mouse_logs_mode > 1:
                    logger.log(f'Step {step_number:03}: [{delta_x:7.3f}, {delta_y:7.3f}], length: {delta_length:6.3f}... ', end_line=False)
                
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
                    logger.log(f'Done (took {miliseconds_float:7.3f}ms) ({speed:5.2f} kpx/s)')
                
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
            logger.log(f'Mouse moved (took {diff_5_seconds_float:.3f}s) (length: {full_length:.2f}px. speed: {speed:5.2f} kpx/s)')
            logger.log(f'Steps count: {steps_count}, min: {min_step}ms, avg: {0 if steps_count == 0 else 1000 * diff_5_seconds_float / steps_count:.3f}ms, max: {max_step}ms')

        script = '''
(x, y) => {
console.log('Target');
const roundX = Math.floor(x);
const roundY = Math.floor(y);
console.log(x, y, roundX, roundY);
const width = 5;
target = document.createElement('div');
target.style.position = 'absolute';
target.style.left = `${roundX}px`;
target.style.top = `${roundY}px`;
target.style.width = `${1 + 2*width}px`;
target.style.height = `${1 + 2*width}px`;
target.style.marginLeft = `${-width}px`;
target.style.marginRight = `${-width}px`;
target.style.border = '2px solid red';
box.style.pointerEvents = 'none';
console.log(target);
document.body.appendChild(target);
console.log(target);
setTimeout(() => {
    target.remove();
}, 5000);
}
'''

        self.browser.crdi.Input_dispatchMouseEvent(type='mousePressed', x=element_x_coordinate, y=current_y_coordinate, button='left', clickCount=1)
        self.browser.crdi.Input_dispatchMouseEvent(type='mouseReleased', x=element_x_coordinate, y=current_y_coordinate, button='left', clickCount=1)
        
        self.browser.run_js_function(script, [element_x_coordinate, current_y_coordinate])

        step_6 = datetime.now()
        diff_6 = step_6 - step_5
        if self.mouse_logs_mode > 1:
            logger.log(f'Mouse clicked (took {diff_6.seconds}.{diff_6.microseconds // 1000:03}s)')
        
        self.browser.crdi.x_coordinate = element_x_coordinate
        self.browser.crdi.y_coordinate = current_y_coordinate
        
    except Exception as e:
        logger.log(f'Error clicking node "{self.name}" [{self.remote_object_id}]')
        raise e
    finally:
        end_time = datetime.now()
        diff = end_time - start_time
        logger.log(f'Click done (took {diff.seconds}.{diff.microseconds // 1000:03}s full)')