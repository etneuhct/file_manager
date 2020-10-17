
class FileTypes:
    VIDEO, AUDIO, DOCUMENT, ARCHIVE = range(4)


def get_file_types():
    file_types = {
        FileTypes.ARCHIVE: ["zip"],
        "audio": ["mp3"],
        "video": ["mp4"],
        "document": ["docx", "doc", "xlsx", "txt"],
        "executable": ["ext"]

    }

    return file_types
