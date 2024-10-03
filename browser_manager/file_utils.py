import os


class FileUtils:
    @staticmethod
    def find_files(directory, extension):
        path = os.path.abspath(directory)
        if not os.path.exists(path):
            os.makedirs(path)

        return [
            os.path.join(root, file)
            for root, _, files in os.walk(path)
            for file in files
            if file.endswith(extension)
        ]
