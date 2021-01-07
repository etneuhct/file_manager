
class FileTypes:
    IMAGE, VIDEO, AUDIO, DOCUMENT, ARCHIVE, APPLICATION, PLAIN_TEXT = range(7)


def get_file_types():
    file_types = {
        FileTypes.ARCHIVE: ["zip"],
        FileTypes.IMAGE: ["png", "jfif"],
        "audio": ["mp3"],
        "video": ["mp4"],
        FileTypes.DOCUMENT: ["docx", "doc", "xlsx", "xls", "rtf"],
        FileTypes.PLAIN_TEXT: ["txt", "csv", "nbib", "ris", ],
        FileTypes.APPLICATION: ["exe"]

    }

    return file_types
