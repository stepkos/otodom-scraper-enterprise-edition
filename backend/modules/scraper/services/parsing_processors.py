from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from lxml.html import HtmlElement

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


class SplitAndTake(ValueProcessor[str, str]):
    def __init__(self, by: str = " ", take: int = 0):
        self.by = by
        self.take = take

    def process_value(self, raw_value: str) -> str | None:
        splitted = raw_value.split(self.by)
        if self.take >= len(splitted):
            return None
        return splitted[self.take]


class Caster(ValueProcessor[A, T]):
    def __init__(self, func: Callable[[A], T]):
        self.func = func

    def process_value(self, raw_value: A) -> T:
        return self.func(raw_value)


class TryCaster(Caster[A, T]):
    def __init__(self, func: Callable[[A], T]):
        super().__init__(func)

    def process_value(self, raw_value: A) -> T | None:
        try:
            return self.func(raw_value)
        except (ValueError, TypeError):
            return None


class Multi(ValueProcessor[A, T]):
    def __init__(self, processors: list[ValueProcessor] = ()):
        self.processors = processors

    def process_value(self, raw_value: A) -> T:
        result = raw_value
        for processor in self.processors:
            if result:
                result = processor.process_value(result)
        return result


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
        try_get = self.map_dict.get(raw_value.strip(), None)
        if try_get is not None:
            return try_get
        return self.default_processor.process_value(raw_value)


class ExtractText(ValueProcessor[HtmlElement, str]):
    def process_value(self, raw_value: HtmlElement) -> str:
        return raw_value.text_content()


class SkipIfIn(ValueProcessor[str, str | None]):
    def __init__(self, keywords_to_skip: list[str]):
        self.keywords_to_skip = keywords_to_skip

    def process_value(self, raw_value: HtmlElement) -> str | None:
        value = str(raw_value).lower()
        if any(keyw.lower() in value for keyw in self.keywords_to_skip):
            return None
        return value


class ExctractAndSkipIfIn(Multi[HtmlElement, str | None]):
    def __init__(self, keywords_to_skip: list[str]):
        super().__init__(
            [
                ExtractText(),
                SkipIfIn(keywords_to_skip),
            ]
        )


ProcessorDict = dict[str, ValueProcessor]
