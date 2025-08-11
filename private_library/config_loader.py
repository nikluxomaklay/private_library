from typing import overload
import os

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Config(dict):
    def __init__(self, file_path, *args, **kwargs) -> None:
        try:
            with open(file_path, 'r') as f:
                config = load(f, Loader)
                kwargs.update(**config)
        except FileNotFoundError:
            pass

        super().__init__(*args, **kwargs)

    def get(self, __key, *args):
        try:
            value = os.environ[__key]
            if value in (None, '') and len(args):
                return args[0]
            return value
        except KeyError:
            return super().get(__key, *args)


    def __getitem__(self, __key):
        try:
            return os.environ[__key]
        except KeyError:
            return super().__getitem__(__key)

    def __getattr__(self, __name):
        try:
            return os.environ[__name]
        except KeyError:
            return super().__getattr__(__name)
