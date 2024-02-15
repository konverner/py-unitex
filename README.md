## PyUnitex

PyUnitex is a python bindings for the [Unitex](https://unitexgramlab.org/fr) C++ Library. It provides python interface for CasSys algorithm used for text processing (syntactic analysis, chunking, information extraction, etc.)

## Installation

1. Install [Unitex/GramLab](https://unitexgramlab.org/fr#downloads)

2. Clone the repository `git clone https://github.com/konverner/py-unitex.git`

3. Set paths to installed Unitex files in [src/unitex/conf.py](https://github.com/konverner/py-unitex/blob/master/src/unitex/conf.py)

## Apply CasSys algorithm

To apply a cascade, use `main.py` script:

```
python main.py --input_file "input/example.csv" --output_file "input/example_spans.json" --cascade_name "loc.csc" --lang "French"
```

arguments:

`--input_file` : csv file with corpus (one line ia one text), see [example.csv](https://github.com/konverner/py-unitex/blob/master/input/example.csv).

`--output_file` : json file with spans of text extracted with the algorithm, see [example_spans.csv](https://github.com/konverner/py-unitex/blob/master/output/example_spans.json).

`--cascade_name` : csc file with cascade kept in `UNITEX_PATH/lang/CasSys/`.

`--lang` : a language of the corpus.


