import os
import zipfile

from file_types import FileTypes
from system_file import SystemFolder, SystemFile, SystemArchive, SystemApplication, SystemFilePdf


class CleanFolder:

    def __init__(self, folder_path, destination_path):
        self.folder_path = folder_path
        self.destination_path = destination_path
        self.system_folder = SystemFolder(self.folder_path)

        if not self.system_folder.exist():
            raise FileNotFoundError

        self.file_manager_folder_path = os.path.join(self.destination_path, "File_manager")
        self.extract_archives = os.path.join(self.file_manager_folder_path, "Archives", "Extract_archives")
        self.unzipped_archives = os.path.join(self.file_manager_folder_path, "Archives", "Archives")
        self.application_folder = os.path.join(self.file_manager_folder_path, "Applications")
        self.pdf_folder = os.path.join(self.file_manager_folder_path, "Documents", "Pdf")
        self.images_folder = os.path.join(self.file_manager_folder_path, "Images")
        self.plain_text_folder = os.path.join(self.file_manager_folder_path, "Documents", "Plain text")
        self.document_folder = os.path.join(self.file_manager_folder_path, "Documents", "Documents")

    def get_folder_files(self):
        return [
            SystemFile(system_item.file_path)
            for system_item in self.system_folder.list_files() if system_item.is_file()]

    def get_archives(self):
        return [SystemArchive(system_file.file_path)
                for system_file in self.get_folder_files() if system_file.get_type() == FileTypes.ARCHIVE]

    def get_applications(self):
        return [SystemApplication(system_file.file_path)
                for system_file in self.get_folder_files() if system_file.get_type() == FileTypes.APPLICATION]

    def clean_archives(self):
        for archive in self.get_archives():
            try:
                archive.extract(self.extract_archives)
                archive.move(self.unzipped_archives)
            except zipfile.BadZipFile:
                print(archive.file_path)
                pass
        return

    def clean_application(self):
        for application in self.get_applications():
            application.move(self.application_folder)
        return

    def clean_pdf(self):
        for system_file in self.get_folder_files():
            if system_file.get_extension() == "pdf":
                system_pdf = SystemFilePdf(system_file.file_path)
                system_pdf.move(self.pdf_folder)

    def clean_images(self):
        for system_file in self.get_folder_files():
            if system_file.get_type() == FileTypes.IMAGE:
                system_file.move(self.images_folder)

    def clean_document(self):
        for system_file in self.get_folder_files():
            if system_file.get_type() == FileTypes.DOCUMENT:
                system_file.move(self.document_folder)

    def clean_plain_text(self):
        for system_file in self.get_folder_files():
            if system_file.get_type() == FileTypes.PLAIN_TEXT:
                system_file.move(self.plain_text_folder)

    def clean_empty_folders(self):
        sub_folders = self.system_folder.get_all_sub_folders()
        sub_folders.reverse()
        for element in sub_folders:
            if not element.list_files():
                element.delete()

    def clean_all(self):
        self.clean_pdf()
        self.clean_images()
        self.clean_plain_text()
        self.clean_document()
        self.clean_archives()
        self.clean_application()
        self.clean_empty_folders()
