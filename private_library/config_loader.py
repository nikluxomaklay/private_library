from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Config(dict):
    def __init__(self, file_path, *args, **kwargs) -> None:
        with open(file_path, 'r') as f:
            config = load(f, Loader)
            kwargs.update(**config)

        super().__init__(*args, **kwargs)
