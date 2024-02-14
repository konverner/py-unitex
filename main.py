import logging
import argparse
import json

from src.unitex.unitex import Unitex
from src.unitex.conf import UNITEX_EXECUTABLE, UNITEX_PATH


def init_parser():
    parser = argparse.ArgumentParser(description='Extract spans from text using Unitex')
    parser.add_argument('--input_file', type=str, help='Input file with text samples')
    parser.add_argument('--output_file', default="output/example_spans.json", type=str, required=False,
                        help='Output file with spans')
    parser.add_argument('--cascade_name', type=str, help='Cascade name')
    parser.add_argument('--lang', default="French", required=False, type=str, help='Language')
    return parser


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    parser = init_parser()
    args = parser.parse_args()

    unitex_instance = Unitex(
        install_path=UNITEX_PATH,
        install_path_app=UNITEX_EXECUTABLE,
        lang=args.lang
    )

    input_file = args.input_file
    with open(input_file, 'r', encoding='utf-8') as f:
        samples = f.readlines()
    logger.info(f"Reading from {input_file} ({len(samples)} samples)")
    spans = [
        unitex_instance.get_spans(sample, args.cascade_name, True)
        for sample in samples
    ]

    output_file = args.output_file
    if output_file == '':
        output_file = f"output/{input_file}_spans.json"

    with open(args.output_file, "w", encoding='utf-8') as f:
        json.dump(spans, f, indent=4)
    logger.info(f"Annotations have been saved as {output_file}")
