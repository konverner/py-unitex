import re

import spacy
from tqdm import tqdm
from spacy.training import biluo_to_iob
from spacy.training.iob_utils import doc_to_biluo_tags

def fix_span(text, span):
    # let us check that spans are correctly extracted

    fixed_span = span.copy()

    # span starts with a space or a punctuation
    while text[fixed_span["start"]] in [" ", ".", ",", ";", ":", "!", "?"]:
        fixed_span["start"] += 1

    # span is cut in the begging: e.g. "ashington DC"
    if fixed_span["start"] > 0:
        while text[fixed_span["start"] - 1] != " ":
            fixed_span["start"] -= 1
            if fixed_span["start"] == 0:
                break

    # span ends with a space or a punctuation: e.g. "Washington DC? "
    while text[fixed_span["end"] - 1] in [" ", ".", ",", ";", ":", "!", "?"]:
        fixed_span["end"] -= 1
        if fixed_span["end"] == 0:
            break

    # span is cut in the end: e.g. "Washington D"
    if fixed_span["end"] < len(text) - 1:
        while text[fixed_span["end"]] not in [" ", ".", ",", ";", ":", "!", "?"]:
            fixed_span["end"] += 1
            if fixed_span["end"] == len(text) - 1:
                break

    fixed_span["text"] = text[fixed_span["start"]:fixed_span["end"]]
    return fixed_span


def spans_to_conll(samples, output_path):
    nlp = spacy.load("fr_core_news_sm")
    with open(output_path, 'w', encoding='utf-8') as f:
        for sample in tqdm(samples):

            # Process the text with spaCy
            doc = nlp(sample["text"])

            # Get BIO tags from spaCy's biluo_tags_from_offsets
            entities = []
            for span in sample["spans"]:
                spacy_span = doc.char_span(span["start"], span["end"], label=span["label"])
                if spacy_span is None:
                    print(f"Skipping entity {span['label']} in the '{sample['text'][span['start']:span['end']]}'")
                else:
                    entities.append(spacy_span)

            doc.ents = entities
            for token, iob_tag in zip(doc, biluo_to_iob(doc_to_biluo_tags(doc))):
                f.write(f"{token.text}\t{iob_tag}\n")
            f.write('\n')
