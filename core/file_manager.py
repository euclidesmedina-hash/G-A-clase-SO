import os

class FileManager:
    def __init__(self):
        self.current_path = os.path.expanduser("~")
        self.history = [self.current_path]
        self.history_index = 0

    def list_dir(self, path=None):
        if path is None:
            path = self.current_path
        
        try:
            items = os.listdir(path)
            return sorted(items, key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        except PermissionError:
            return["acceso denegado"]
        except FileNotFoundError:
            return ["ruta no econtrada"]
        
    def navigate_to(self, folder_name):
        new_path = os.path.join(self.current_path, folder_name)
        if os.path.isdir(new_path):
            self.current_path = new_path
            self.update_history(new_path)
            return True
        return False
    
    def go_back(self):
        """Retrocede en historial"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            return True
        return False

    def go_forward(self):
        """Avanza en historial"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            return True
        return False

    def update_history(self, new_path):
        """Actualiza historial de navegación"""
        self.history = self.history[:self.history_index + 1]
        self.history.append(new_path)
        self.history_index += 1


file = FileManager()

print("ruta actual: ",file.current_path)
print(file.history)