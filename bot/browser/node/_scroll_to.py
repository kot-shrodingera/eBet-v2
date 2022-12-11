import math
import random
from timeout import random_timeout

from . import Node

scroll_function = '''
(scrollAmount, scrollElementSelector) => {
    const element = document.querySelector(scrollElementSelector);
    element.scrollTop += scrollAmount;
}
'''

def scroll_to(self: Node, element_coordinate=None, container_css_selector=None, scrollable_section_css_selector=None, amount=None) -> int:
    if container_css_selector:
        visible_section_top_coordinate, visible_section_bottom_coordinate = self.browser.crdi.move_mouse_to_container(container_css_selector)
    else:
        visible_section_top_coordinate = 0
        response = self.browser.crdi.execute_javascript_statement('window.innerHeight')
        visible_section_bottom_coordinate = response['value'] # pyright: ignore [reportGeneralTypeIssues]

    if element_coordinate: # Default option
        # print('Passed coordinate:', coordinate)
        # print('Bottom of viewport:', visible_section_bottom_coordinate)

        if element_coordinate > visible_section_bottom_coordinate: # Scroll down, element is below viewport
            if scrollable_section_css_selector:
                scrollable_section = self.browser.crdi.find(scrollable_section_css_selector)
                if scrollable_section:
                    scrollable_section_top_coordinate, scrollable_section_right_coordinate, scrollable_section_bottom_coordinate, scrollable_section_left_coordinate = scrollable_section['coordinates']
                else:
                    scrollable_section_bottom_coordinate = 10000
                    
            coordinate_to_scroll_to = element_coordinate - visible_section_bottom_coordinate
            # print('coordinate_to_scroll_to:', coordinate_to_scroll_to)
            # print()
            
            if self.browser.settings.js_scroll:
                scroll_amount = 100 * (math.ceil(coordinate_to_scroll_to / 100) + 1)
                self.browser.run_js_function(scroll_function, [scroll_amount, container_css_selector or 'body'])
                return scroll_amount
            
            steps = math.ceil(coordinate_to_scroll_to / 100)
            if not scrollable_section_css_selector: # If there isn't a chance to overscroll, add randomisation
                steps_randomiser = random.randint(0, 1)
                steps += steps_randomiser
            for step in range(steps):
                self.browser.crdi.Input_dispatchMouseEvent(type='mouseWheel', x=self.browser.crdi.x_coordinate, y=self.browser.crdi.y_coordinate, deltaX=-1, deltaY=100, pointerType='mouse')
                random_timeout(0.01, 0.08)
            random_timeout(0.2, 0.3)
            scroll_amount = steps * 100
            
            coordinate_scrolled_to = visible_section_bottom_coordinate + scroll_amount
            if scrollable_section_css_selector and coordinate_scrolled_to > scrollable_section_bottom_coordinate: # pyright: ignore [reportUnboundVariable] If we have overscrolled, calculate the amount of pixels the last scroll amount was # 872 + 200 = 1072 (> 1054)
                coordinate_before_overscrolling = coordinate_scrolled_to - 100 # 872 + 200 - 100 = 972
                last_scroll_amount = scrollable_section_bottom_coordinate - coordinate_before_overscrolling # pyright: ignore [reportUnboundVariable] 1054 - 972 = 82
                scroll_amount = scroll_amount - 100 + last_scroll_amount # 200 - 100 + 82 = 182
                # updated_element_coordinates = 987 - 182 = 805
            return scroll_amount
        elif element_coordinate < visible_section_top_coordinate: # Scroll up
            coordinate_to_scroll_to = (element_coordinate - visible_section_top_coordinate) * -1
            
            if self.browser.settings.js_scroll:
                scroll_amount = -100 * (math.ceil(coordinate_to_scroll_to / 100) + 1)
                self.browser.run_js_function(scroll_function, [scroll_amount, container_css_selector or 'body'])
                return scroll_amount
            
            steps = math.ceil(coordinate_to_scroll_to / 100) # We may need to scroll to the top, so using a randomiser could cause us to overscroll despite having reached the top meaning the coordinate would be wrong
            for step in range(steps):
                self.browser.crdi.Input_dispatchMouseEvent(type='mouseWheel', x=self.browser.crdi.x_coordinate, y=self.browser.crdi.y_coordinate, deltaX=-1, deltaY=-100, pointerType='mouse')
                random_timeout(0.01, 0.08)
            random_timeout(0.2, 0.3)
            scroll_amount = steps * -100
            return scroll_amount

    elif amount:
        for step in range(amount):
            self.browser.crdi.Input_dispatchMouseEvent(type='mouseWheel', x=self.browser.crdi.x_coordinate, y=self.browser.crdi.y_coordinate, deltaX=-1, deltaY=100, pointerType='mouse')
            
    return 0