import pathlib

def get_testfile_path(filename):
    return str(pathlib.Path(__file__).parent.absolute() / 'testfiles' / filename)

