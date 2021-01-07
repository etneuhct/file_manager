import os
import shutil
import zipfile
from typing import List
from PyPDF2 import PdfFileReader
from file_types import get_file_types


class SystemItem:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def is_folder(self):
        return os.path.isdir(self.file_path)

    def is_file(self):
        return os.path.isfile(self.file_path)

    def exist(self):
        return os.path.exists(self.file_path)

    def delete(self, force_delete=False):
        if self.is_file():
            os.remove(self.file_path)
        elif self.is_folder():
            if force_delete:
                shutil.rmtree(self.file_path)
            else:
                try:
                    os.rmdir(self.file_path)
                except OSError:
                    print(f"Le répertoire {os.path.basename(self.file_path)} n'est pas vide. Suppression impossible")

    def dir_name(self):
        return os.path.dirname(self.file_path)

    def rename(self, new_name):
        new_name = os.path.join(self.dir_name(), new_name)
        os.rename(self.file_path, new_name)

    def get_size(self):
        return os.path.getsize(self.file_path)

    def move(self, new_path, copy_name=""):
        os.makedirs(new_path, exist_ok=True)
        try:
            os.rename(self.file_path, os.path.join(new_path, f"{copy_name}{self.name()}"))
        except FileExistsError:
            self.move(new_path, copy_name="(copy) ")

    def name(self):
        return os.path.basename(self.file_path)


class SystemFile(SystemItem):

    def get_extension(self):
        return self.file_path.split(".")[-1].lower()

    def get_type(self):
        file_types = get_file_types()
        for file_type in file_types:
            if self.get_extension() in file_types[file_type]:
                return file_type

    def get_name_without_extension(self):
        return ".".join(os.path.basename(self.file_path).split(".")[:-1])


class SystemFolder(SystemItem):

    def list_files(self) -> List[SystemItem]:
        return [SystemItem(os.path.join(self.file_path, item)) for item in os.listdir(self.file_path)]

    def add_folder(self, folder_name):
        folder_path = os.path.join(self.file_path, folder_name)
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            pass
        return folder_path

    def create(self):
        os.mkdir(self.file_path)

    def get_all_sub_folders(self):
        result = []
        for path, sub_dirs, files in os.walk(self.file_path):
            for name in sub_dirs:
                result.append(SystemFolder(os.path.join(path, name)))
        return result


class SystemArchive(SystemFile):

    def extract(self, destination_directory):
        destination = os.path.join(destination_directory, self.get_name_without_extension())
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)


class SystemApplication(SystemItem):
    pass


class SystemFilePdf(SystemFile):

    def get_metadata(self):
        pdf = PdfFileReader(open(self.file_path, "rb"))
        print(pdf.getDocumentInfo())
        """for k in pdf.getDocumentInfo().keys():
            if "ARTICLEDOI".lower() in k.lower() or "/doi" in k.lower():
                print(k, pdf.getDocumentInfo()[k])"""


class SystemFileImage(SystemFile):
    pass

