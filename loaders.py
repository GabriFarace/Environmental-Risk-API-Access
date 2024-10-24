import shutil
from abc import ABC, abstractmethod
import gdown
import os
import zipfile
import tempfile

class FilePathLoader(ABC):

    @abstractmethod
    def load_path(self, file_data):
        pass


class FilePathLoaderFromGdrive(FilePathLoader):
    ''' Class used to create a temporary directory and loading there the zip files from google drive'''
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def load_path(self, file_data):
        ''' Return the file path of the public file described by file_data from google drive'''
        file_id = file_data['id']
        file_name = file_data['name']
        file_type = file_data['type']

        # Download the zip file containing the file (zip name is equal to file name)
        zip_path = os.path.join(self.temp_dir, file_name + ".zip")
        gdown.download(f'https://drive.google.com/uc?id={file_id}', zip_path, quiet=False)

        # Extract the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

        # Find the  file in the extracted files
        file_path = None
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file == file_name + file_type:
                    file_path = os.path.join(root, file)
                    break

        if file_path is None:
            raise FileNotFoundError("File not found in the downloaded zip file.")

        # Return the file path
        return file_path

    def __del__(self):
        '''Remove the temporary directory and all its contents'''
        if self.temp_dir:
            print(f"Cleaning up temporary directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)
