from modules.scraper.services.parsing_processors import *

FIELD_MAP: ProcessorDict = {
    'price': Multi[HtmlElement, str]([
        ExtractText(),
        Replace('\xa0', ''),
        Stripper("zł"),
        TryCaster(int),
    ]),
    'title': ExtractText(),
    'subpage': KeyGet("href"),
    'rooms':
        Multi[HtmlElement, str](
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
    'area': Multi[HtmlElement, float]([
        ExtractText(),
        Stripper(' m²'),
        Caster(float)
    ]),
    'floor':
        Multi[HtmlElement, str](
            [
                ExtractText(),
                SplitAndTake(),
                SpecialCases[str, int](
                    {
                        "parter": 0,
                        "10+": 11,
                        "poddasze": 12,
                        "suterena": 13,
                    },
                    Caster(int)
                ),
            ]
        ),
    'address': ExtractText(),
}

SUBPAGES_FIELD_MAP: ProcessorDict = {
    'max_floor': Multi[HtmlElement, str]([
        ExtractText(),
        SplitAndTake("/", 1),
        TryCaster(int),
    ]),
    'rent': Multi[HtmlElement, str]([
        ExtractText(),
        SplitAndTake(),
        TryCaster(int),
    ]),
    "energy_certificate": ExtractText(),
    "form_of_the_property": ExtractText(),
    "finishing_condition": ExtractText(),
    "balcony_garden_terrace": ExtractText(),
    "parking_place": ExtractText(),
    "heating": ExtractText(),
    "description": ExtractText(),
    "market": Multi[HtmlElement, str]([  # losowy css
        ExtractText(),
        SplitAndTake("}", -1)
    ]),
    "advertisement_type": ExtractText(),
    "year_of_construction": ExtractText(),
    "type_of_development": ExtractText(),
    "windows": ExtractText(),
    "is_elevator": Multi[HtmlElement, bool]([
        ExtractText(),
        SpecialCases[str, int](
            {
                "tak": True,
                "nie": False,
            },
            Multi(),
        ),
    ]),
}
