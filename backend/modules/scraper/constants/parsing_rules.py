from functools import partial

from modules.scraper.services.parsing_processors import *

FIELD_MAP: ProcessorDict = {
    "price": Multi[HtmlElement, str](
        [
            ExtractText(),
            Replace("\xa0", ""),
            Stripper("zł"),
            TryCaster(int),
        ]
    ),
    "title": ExtractText(),
    "subpage": KeyGet("href"),
    "rooms": Multi[HtmlElement, str](
        [
            ExtractText(),
            SplitAndTake(),
            SpecialCases[str, int](
                {
                    "10+": 11,
                },
                Caster(int),
            ),
        ]
    ),
    "area": Multi[HtmlElement, float]([ExtractText(), Stripper(" m²"), Caster(float)]),
    "floor": Multi[HtmlElement, str](
        [
            ExtractText(),
            SplitAndTake(),
        ]
    ),
    "address": ExtractText(),
}

ExtractAndSkipHidden = partial(ExctractAndSkipIfIn, ["brak informacji", "zapytaj"])

SUBPAGES_FIELD_MAP: ProcessorDict = {
    "max_floor": Multi[HtmlElement, str](
        [
            ExtractAndSkipHidden(),
            SplitAndTake("/", 1),
            TryCaster(int),
        ]
    ),
    "rent": Multi[HtmlElement, str](
        [
            ExtractAndSkipHidden(),
            SplitAndTake(),
            TryCaster(int),
        ]
    ),
    "energy_certificate": ExtractAndSkipHidden(),
    "form_of_the_property": ExtractAndSkipHidden(),
    "finishing_condition": ExtractAndSkipHidden(),
    "balcony_garden_terrace": ExtractAndSkipHidden(),
    "parking_place": ExtractAndSkipHidden(),
    "heating": ExtractAndSkipHidden(),
    "description": ExtractAndSkipHidden(),
    "market": Multi[HtmlElement, str](
        [ExtractAndSkipHidden(), SplitAndTake("}", -1)]  # losowy css
    ),
    "advertisement_type": ExtractAndSkipHidden(),
    "year_of_construction": ExtractAndSkipHidden(),
    "type_of_development": ExtractAndSkipHidden(),
    "windows": ExtractAndSkipHidden(),
    "is_elevator": Multi[HtmlElement, bool](
        [
            ExtractAndSkipHidden(),
            SpecialCases[str, int](
                {
                    "tak": True,
                    "nie": False,
                },
                Multi(),
            ),
        ]
    ),
    "exact_rooms": Multi[HtmlElement, bool](
        [
            ExtractAndSkipHidden(),
            Caster(int),
        ]
    ),
    "exact_floors": Multi[HtmlElement, bool](
        [
            ExtractAndSkipHidden(),
            SplitAndTake("/", 0),
            Caster(int),
        ]
    ),
}
