from clean_folder import CleanFolder
import argparse
import os
from dotenv import load_dotenv
load_dotenv()


class FileHandlerException(Exception):
    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-src', required=False, help="chemin du dossier a nettoyer", type=str,
                        default=os.getenv('CLEAN_SRC'))
    parser.add_argument('-dest', required=False, help="Chemin ou mettre les fichiers nettoyés", type=str,
                        default=os.getenv('CLEAN_DEST'))
    args = parser.parse_args()

    src = getattr(args, 'src')
    dest = getattr(args, 'dest')

    if not src or not dest:
        raise FileHandlerException(
            "le chemin du dossier à nettoyer et le chemin de "
            "destination doivent être renseignés dans l'environnement ou en argument")

    clean_folder = CleanFolder(src, dest)
    clean_folder.clean_all()
