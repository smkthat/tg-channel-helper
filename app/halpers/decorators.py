import functools
from typing import Any


def singleton(cls):
    """Decorator to set class as singleton

    This decorator set class as singleton, meaning it can be created only once and all other references will
    point to the same object. This class is used to ensure that all the other classes that need one
    instance only will have the same one.

    Attributes:
        __instances (dict): Dictionary of singleton instances
    """

    @functools.wraps(cls)
    def get_instance(*args, **kwargs) -> Any:
        """Get instance of the singleton class

        This class method will return the instance of the singleton class if it's already been created,
        otherwise creates a new instance.

        :param args: Variable length argument list to provide in class
        :param kwargs: Arbitrary keyword arguments to provide in class

        :return: Instance of the singleton class
        """
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]

    __instances = {}
    return get_instance
