from system_file import SystemFolder, SystemFile, SystemArchive
from file_types import FileTypes


class CleanFolder:

    def __init__(self, folder_path, destination_path):
        self.folder_path = folder_path
        self.destination_path = destination_path
        self.system_folder = SystemFolder(self.folder_path)

        self.file_manager_folder_path = SystemFolder(self.destination_path).add_folder("file_manager")
        self.archives_folder = SystemFolder(self.file_manager_folder_path).add_folder("archives")
        self.extract_archives = SystemFolder(self.archives_folder).add_folder("extract_archives")
        self.unzipped_archives = SystemFolder(self.archives_folder).add_folder("archives")

        if not self.system_folder.exist():
            raise FileNotFoundError

    def get_folder_files(self):
        return [
            SystemFile(system_item.file_path)
            for system_item in self.system_folder.list_files() if system_item.is_file()]

    def get_archives(self):
        return [SystemArchive(system_file.file_path)
                for system_file in self.get_folder_files() if system_file.get_type() == FileTypes.ARCHIVE]

    def clean_archives(self):
        for archive in self.get_archives():
            archive.extract(self.extract_archives)
            archive.move(self.unzipped_archives)
        return

    def routine(self):

        self.clean_archives()



path = r"C:\Users\jack\Downloads"
destination = r"C:\Users\jack\Downloads"
clean_folder = CleanFolder(path, destination)
clean_folder.routine()
