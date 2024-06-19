from django.test import TestCase
from lxml.html import fromstring
from modules.scrapers.services.parsing_processors import Stripper, SplitAndTake, Caster, TryCaster, \
    Multi, KeyGet, Replace, SpecialCases, ExtractText, parse_single_attr


class TestValueProcessors(TestCase):

    def test_stripper(self):
        self.assertEqual(Stripper(keyword=" ").process_value("  banana  "), "banana")
        self.assertEqual(Stripper(keyword="a").process_value("apple"), "pple")
        self.assertEqual(Stripper(keyword="a").process_value("banana"), "banan")

    def test_split_and_take(self):
        processor = SplitAndTake(by=" ", take=1)
        self.assertEqual(processor.process_value("hello world"), "world")
        self.assertIsNone(processor.process_value("hello"))
        self.assertEqual(processor.process_value("one two three"), "two")

    def test_caster(self):
        processor = Caster(func=int)
        self.assertEqual(processor.process_value("123"), 123)

    def test_try_caster(self):
        processor = TryCaster(func=int)
        self.assertEqual(processor.process_value("123"), 123)
        self.assertIsNone(processor.process_value("abc"))

    def test_multi(self):
        processor = Multi(processors=[Stripper(keyword=" "), Replace(to_be_repl="hello", replace_to="hi")])
        self.assertEqual(processor.process_value("  hello world  "), "hi world")

    def test_key_get(self):
        processor = KeyGet(key_name="key")
        self.assertEqual(processor.process_value({"key": "value"}), "value")
        self.assertIsNone(processor.process_value({"other_key": "value"}))

    def test_replace(self):
        processor = Replace(to_be_repl="hello", replace_to="hi")
        self.assertEqual(processor.process_value("hello world"), "hi world")

    def test_special_cases(self):
        default_processor = Stripper(keyword="a")
        special_cases = SpecialCases(map_dict={"special": "case"}, default_processor=default_processor)
        self.assertEqual(special_cases.process_value("special"), "case")
        self.assertEqual(special_cases.process_value("apple"), "pple")

    def test_extract_text(self):
        processor = ExtractText()
        html = fromstring("<div>Hello World</div>")
        self.assertEqual(processor.process_value(html), "Hello World")

    def test_parse_single_attr(self):
        xpaths_dict = {"attr": "//div/text()"}
        parse_dict = {"attr": Stripper(keyword=" ")}
        html = fromstring('<div>  some text  </div>')
        result = parse_single_attr(xpaths_dict, parse_dict, html, "attr")
        self.assertEqual(result, "some text")

        html_empty = fromstring('<div></div>')
        result_empty = parse_single_attr(xpaths_dict, parse_dict, html_empty, "attr")
        self.assertIsNone(result_empty)
