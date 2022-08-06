class Control:
    filename = './control'
    current_action: str
    
    def __init__(self) -> None:
        pass
    
    def get_current_action(self) -> str:
        with open(self.filename) as file:
            self.current_action = file.read()
            return self.current_action
    
    def set_current_action(self, action: str) -> None:
        with open(self.filename, 'w') as file:
            file.write(action)
            self.current_action = action
