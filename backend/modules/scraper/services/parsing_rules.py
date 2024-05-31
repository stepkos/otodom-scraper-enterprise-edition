from parsing_processors import *

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
                SplitAndFirst(),
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
                SplitAndFirst(),
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
