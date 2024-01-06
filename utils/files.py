import utils
from pathlib import Path


def abs_project_file_path(relative_path: str):
    return (
        Path(utils.__file__).parent.parent.joinpath(relative_path).absolute().__str__()
    )
