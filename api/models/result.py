from typing import TypeVar, Generic, Optional

_R = TypeVar('_R')


class Result(Generic[_R]):
    _data: Optional[_R] = None
    _exception: Optional[Exception] = None

    @property
    def success(self) -> bool: return self._data is not None

    @property
    def failed(self) -> bool: return not self.success

    class Success('Response[_R]'):
        def __init__(self, data: _R) -> None:
            super().__init__()
            self._data = data

    class Failure('Response[_R]'):
        def __init__(self, exception: Exception) -> None:
            super().__init__()
            self._exception = exception


