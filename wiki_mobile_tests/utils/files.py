import wiki_mobile_tests
from pathlib import Path


def abs_project_file_path(relative_path: str):
    return (
        Path(wiki_mobile_tests.__file__).parent.parent.joinpath(relative_path).absolute().__str__()
    )
