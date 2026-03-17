import os

class TempFilesManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.configured = False
        return cls._instance

    def configure(self, temp_files_path: str) -> bool:
        if not self.configured:
            self.files_path = temp_files_path
            self.temp_files = []
            self.configured = True
            return True
        return False

    def create(self, text: str, temp_file_name_template: str, **kwargs) -> str | None:
        if not self.configured:
            return None

        if not os.path.exists(self.files_path):
            os.mkdir(self.files_path)

        path = self.files_path + temp_file_name_template

        for key, value in kwargs.items():
            path = path.replace("{"+str(key)+"}", str(value))

        with open(path, "w") as file:
            file.write(text)

        self.temp_files.append(path)
        return path
    
    def delete(self, path: str) -> bool:
        if path in self.temp_files:
            try:
                os.remove(path)
                self.temp_files.remove(path)
                return True
            except Exception:
                self.temp_files.remove(path)
                return True
        return False