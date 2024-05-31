from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

A = TypeVar("A")
T = TypeVar("T")


class ValueProcessor(ABC, Generic[A, T]):
    @abstractmethod
    def process_value(self, keyword: str):
        raise NotImplementedError


class Stripper(ValueProcessor[str, str]):
    def __init__(self, keyword: str):
        self.keyword = keyword

    def process_value(self, raw_value: str) -> str:
        return raw_value.strip(self.keyword)


class SplitAndFirst(ValueProcessor[str, str]):
    def process_value(self, raw_value: str) -> str:
        return raw_value.split(' ')[0]


class Caster(ValueProcessor[A, T]):
    def __init__(self, func: Callable[[A], T]):
        self.func = func

    def process_value(self, raw_value: A) -> T:
        return self.func(raw_value)


class Multi(ValueProcessor[A, T]):
    def __init__(self, processors: list[ValueProcessor] = ()):
        self.processors = processors

    def process_value(self, raw_value: A) -> T:
        result = raw_value
        for processor in self.processors:
            result = processor.process_value(processor)
        return result


class AttrGet(ValueProcessor[A, T]):
    def __init__(self, attr_name: str):
        self.attr_name = attr_name

    def process_value(self, raw_value: A) -> T:
        return getattr(raw_value, self.attr_name)


class KeyGet(ValueProcessor[A, T]):
    def __init__(self, key_name: A):
        self.key_name = key_name

    def process_value(self, raw_value: dict[A, T]) -> T | None:
        return raw_value.get(self.key_name, None)


class Replace(ValueProcessor[str, str]):
    def __init__(self, to_be_repl: str, replace_to: str):
        self.to_be_repl = to_be_repl
        self.replace_to = replace_to

    def process_value(self, raw_value: str) -> str:
        return raw_value.replace(self.to_be_repl, self.replace_to)


class SpecialCases(ValueProcessor[A, T]):
    def __init__(self, map_dict: dict[A, T], default_processor: ValueProcessor[A, T]):
        self.map_dict = map_dict
        self.default_processor = default_processor

    def process_value(self, raw_value: A) -> T | None:
        try_get = self.map_dict.get(raw_value, None)
        if try_get:
            return try_get
        return self.default_processor.process_value(raw_value)


class SplitFirstIntCast(Multi[str, int]):
    def __init__(self):
        super().__init__([
            SplitAndFirst(), Caster(int)
        ])


ProcessorDict = dict[str, ValueProcessor]

FIELD_MAP: ProcessorDict = {
    'price': Multi[str, str]([AttrGet("text"), Replace('\xa0', ''), Stripper("zł")]),
    'title': AttrGet("text"),
    'subpage': KeyGet("href"),
    'rooms': SpecialCases[str, int](
        {
            "10+": 11,
        },
        SplitFirstIntCast()
    ),
    'area': Multi[str, float]([Stripper(' m²'), Caster(float)]),
    'floor': SpecialCases[str, int](
        {
            "parter": 0,
            "10+": 11,
            "poddasze": 12,
            "suterena": 13,
        },
        SplitFirstIntCast()
    ),
    'address': Multi(),
}
