import sys
sys.path.append('.')

from src.unitex.utils import fix_span


def test_fix_span():
    test_cases = [
        {
            "text": "I live in Washington DC with Paul Smith",
            "spans":
            [
                {"start": 11, "end": 24, "label": "GEO"},
                {"start": 28, "end": 39, "label": "PER"}
            ]
        },
        {
            "text": "New York is a city in the United States.",
            "spans":
            [
                {"start": 0, "end": 8, "label": "GEO"},
                {"start": 23, "end": 39, "label": "GEO"}
            ]
        },
        {
            "text": "- Au carrefour de la motte; continuer en face sur le meme chemin et un carrefour en T.",
            "spans": [
                {"start": 5, "end": 27, "label": "INF"},
                {"start": 71, "end": 86, "label": "INF"}
            ]
        },
    ]

    expected_spans = [
        [{"start": 10, "end": 23}, {'start': 29, 'end': 39}],
        [{'start': 0, 'end': 8}, {'start': 22, 'end': 39}],
        [{'start': 5, 'end': 26}, {"start": 71, "end": 85}],
    ]

    for test_case, expected_span in zip(test_cases, expected_spans):
        for i, span in enumerate(test_case["spans"]):
            fixed_span = fix_span(test_case["text"], span)
            print(f"Fixed span: {fixed_span} with text: {test_case['text'][fixed_span['start']:fixed_span['end']]}")
            print(f"Expected span: {expected_span[i]} with text: {test_case['text'][expected_span[i]['start']:expected_span[i]['end']]}")
            assert fixed_span["start"] == expected_span[i]["start"]
            assert fixed_span["end"] == expected_span[i]["end"]

test_fix_span()
