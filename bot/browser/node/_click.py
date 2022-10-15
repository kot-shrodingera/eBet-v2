import random
import numpy as np

from python_ghost_cursor import path
from typing import Optional

from . import Node

def click(self: Node, scroll=False, container_css_selector: Optional[str] = None, scrollable_section_css_selector: Optional[str] = None) -> None:
    browser = self.browser.crdi
    
    content_coords = self.get_box_model()['content']
    top_coordinate = content_coords[1]
    right_coordinate = content_coords[2]
    bottom_coordinate = content_coords[5]
    left_coordinate = content_coords[0]

    # Scroll if specified
    if scroll or container_css_selector:
        scroll_amount = self.scroll_to(element_coordinate=bottom_coordinate, container_css_selector=container_css_selector, scrollable_section_css_selector=scrollable_section_css_selector)
    else:
        scroll_amount = 0

    x_coordinate = random.uniform(left_coordinate, right_coordinate)
    current_y_coordinate = random.uniform(top_coordinate, bottom_coordinate) - scroll_amount # Account for amount of pixels scrolled

    # Move mouse to element if it is not already at the coordinates
    if browser.x_coordinate != x_coordinate and browser.y_coordinate != current_y_coordinate:
        starting_point = {'x': browser.x_coordinate, 'y': browser.y_coordinate}
        ending_point = {'x': x_coordinate, 'y': current_y_coordinate}
        route = path(starting_point, ending_point)
        
        if self.mouse_path_shrink < 1 and self.mouse_path_shrink >= 0:
            steps_count = len(route)
            leave_count = round(steps_count * self.mouse_path_shrink)
            delete_count = steps_count - leave_count
            
            deleting_indecies = np.round(np.linspace(0, steps_count - 1, delete_count, endpoint=False)).astype(int)

            route = np.delete(route, deleting_indecies) # pyright: ignore [reportGeneralTypeIssues]

        for step in route:
            browser.Input_dispatchMouseEvent(type='mouseMoved', x=step['x'], y=step['y'])

    browser.Input_dispatchMouseEvent(type='mousePressed', x=x_coordinate, y=current_y_coordinate, button='left', clickCount=1)
    browser.Input_dispatchMouseEvent(type='mouseReleased', x=x_coordinate, y=current_y_coordinate, button='left', clickCount=1)

    browser.x_coordinate = x_coordinate
    browser.y_coordinate = current_y_coordinate