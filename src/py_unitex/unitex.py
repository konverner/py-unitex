import os
import re
import subprocess
from subprocess import DEVNULL, STDOUT, check_call
import xml.etree.ElementTree as ET

from py_unitex.conf import UNITEX_EXECUTABLE, UNITEX_PATH


class Unitex:
    def __init__(
            self,
            version="Standard",
            lang="French",
            install_path=None,
            install_path_app=None,
            verbose=False
        ):
        self.version = version
        self.lang = lang
        self.parser = ProperNameParser()
        if install_path is None:
            self.install_path = UNITEX_PATH
        else:
            self.install_path = install_path

        if install_path_app is None:
            self.install_path_app = UNITEX_EXECUTABLE
        else:
            self.install_path_app = install_path_app+"/UnitexToolLogger"

        self.dic_path = f"{self.install_path}/{self.lang}/Dela/LOC.dic " + \
                        f"{self.install_path}/{self.lang}/Dela/Dela_fr.bin " + \
                        f"{self.install_path}/{self.lang}/Dela/motsGramf-.bin"
        self.graphs_path = f"{self.install_path}/{self.lang}/Graphs"
        self.corpus_path = f"{self.install_path}/{self.lang}/Corpus"
        self.verbose = verbose

    def run_mandatory_preprocessing(self, file_name):
        try:
            os.mkdir(f"{self.corpus_path}/{file_name}_snt")
        except:
            pass

        cmd = [
            self.install_path_app,
            "Normalize",
            f"{self.corpus_path}/{file_name}.txt",
            f"-r{self.install_path}/{self.lang}/Norm.txt",
            f"--output_offsets={self.corpus_path}/{file_name}_snt/normalize.out.offsets",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Grf2Fst2",
            f"{self.install_path}/{self.lang}/Graphs/Preprocessing/Sentence/Sentence.grf",
            "-y",
            f"--alphabet={self.install_path}/{self.lang}/Alphabet.txt",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Flatten",
            f"{self.install_path}/{self.lang}/Graphs/Preprocessing/Sentence/Sentence.fst2",
            "--rtn",
            "-d5",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Fst2Txt",
            f"-t{self.corpus_path}/{file_name}.snt",
            f"{self.install_path}/{self.lang}/Graphs/Preprocessing/Sentence/Sentence.fst2",
            f"-a{self.install_path}/{self.lang}/Alphabet.txt",
            "-M",
            f"--input_offsets={self.install_path}/{self.lang}/Corpus/{file_name}_snt/normalize.out.offsets",
            f"--output_offsets={self.install_path}/{self.lang}/Corpus/{file_name}_snt/normalize.out.offsets",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Grf2Fst2",
            f"{self.install_path}/{self.lang}/Graphs/Preprocessing/Replace/Replace.grf",
            "-y",
            f"--alphabet={self.install_path}/{self.lang}/Alphabet.txt",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Fst2Txt",
            f"-t{self.install_path}/{self.lang}/Corpus/{file_name}.snt",
            f"{self.install_path}/{self.lang}/Graphs/Preprocessing/Replace/Replace.fst2",
            f"-a{self.install_path}/{self.lang}/Alphabet.txt",
            "-R",
            f"--input_offsets={self.install_path}/{self.lang}/Corpus/{file_name}_snt/normalize.out.offsets",
            f"--output_offsets={self.install_path}/{self.lang}/Corpus/{file_name}_snt/normalize.out.offsets",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Tokenize",
            f"{self.install_path}/{self.lang}/Corpus/{file_name}.snt",
            f"-a{self.install_path}/{self.lang}/Alphabet.txt",
            f"--input_offsets={self.install_path}/{self.lang}/Corpus/{file_name}_snt/normalize.out.offsets",
            f"--output_offsets={self.install_path}/{self.lang}/Corpus/{file_name}_snt/tokenize.out.offsets",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

        cmd = [
            self.install_path_app,
            "Dico",
            f"-t{self.install_path}/{self.lang}/Corpus/{file_name}.snt",
            f"-a{self.install_path}/{self.lang}/Alphabet.txt",
            f"-m{self.install_path}/{self.lang}/Dela/LOC.dic",
            f"{self.install_path}/{self.lang}/Dela/LOC.bin",
            f"C:/Users/konst/AppData/Local/Unitex-GramLab/{self.lang}/Dela/Dela_fr.bin",
            f"C:/Users/konst/AppData/Local/Unitex-GramLab/{self.lang}/Dela/motsGramf-.bin",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)


    def run_cascade(self, cascade_name, file_name):
        self.run_mandatory_preprocessing(file_name)
        csc_path = f"{self.install_path}/{self.lang}/CasSys/{cascade_name}"
        command = [
            self.install_path_app,
            'Cassys',
            f'-a{str(self.install_path)}/French/Alphabet.txt',
            f'-t{self.corpus_path}/{file_name}.snt',
            f'-l{csc_path}',
            f'-w{self.dic_path}',
            f'-r{str(self.graphs_path)}/',
            f'--input_offsets={self.corpus_path}/{file_name}_snt/normalize.out.offsets',
            '-qutf8-no-bom'
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def build_concord(self, file_name):

        cmd = [
            self.install_path_app,
            "Concord",
            f"{self.corpus_path}/{file_name}_snt/concord.ind",
            "-fCourier new",
            "-s12",
            "-l40",
            "-r55",
            f"-a{self.install_path}/{self.lang}/Alphabet_sort.txt",
            "--CL",
            "--xml",
            "-qutf8-no-bom"
        ]
        if self.verbose:
            print(cmd)
        check_call(cmd, stdout=DEVNULL, stderr=STDOUT)


    def get_spans(self, text, cascade_name, extended_labeling=False):
        result = []
        sents = re.split(r"\. |; |! |\? ", text)
        current_length = 0
        for sent in sents:
            if len(sent) == 0:
                continue
            file_name = "tmp"
            with open(f"{self.corpus_path}/{file_name}.txt", "w", encoding="utf-8") as f:
                f.write(sent)
            self.run_mandatory_preprocessing(file_name)
            self.run_cascade(cascade_name, file_name)
            self.build_concord(file_name)
            with open(f"{self.corpus_path}/{file_name}_snt/concord.xml", encoding="utf-8") as f:
                xml_code = f.read()
            # Parse the XML
            root = ET.fromstring(xml_code)
            counts = {}

            # Extract text and spans from XML
            for concordance in root.findall('concordance'):
                label = concordance.text.split('.')[-1][:-1]

                start = int(concordance.attrib['start']) + current_length
                end = int(concordance.attrib['end']) + current_length

                if extended_labeling:
                    label = self.parser.parse_entry(concordance.text)
                result.append(
                    {
                        "start": start,
                        "end": end,
                        "label": label,
                        "text": text[start:end]
                    }
                )
            current_length += len(sent) + 2

        return result


class ProperNameParser:
    def __init__(self):
        pass

    def _get_proper_names(self, doc):
        text = doc['text']
        proper_names = []
        for item in doc['content']:
            if item['label'] in {'PN', 'ROAD_ID'}:
                proper_names.append(item['text'])
            text += item['text'] + ' '
        text = text.strip()

        syntagme = text
        for proper_name in proper_names:
            syntagme = text.replace(proper_name, '').strip()

        result = [
            {
                "label": doc['label'],
                "proper_name": proper_name.strip(),
                "syntagme": syntagme
            }
            for proper_name in proper_names
        ]
        return result

    def parse_entry(self, entry):
        text = ''
        entry = entry.replace('\\', '')
        result = {}
        result["label"] = entry.split('.')[-1][:-1]

        entry = entry[1:-1]
        result["text"] = entry.split('{')[0]
        result["content"] = []

        text += result["text"] + ' '

        content = re.findall('\{.+\}', entry)[0]
        content = content[1:-1]

        result["content"].append(
            {
                "label": content.split(',.')[1],
                "text": content.split(',.')[0],
                "content": None
            }
        )
        result = self._get_proper_names(result)
        return result
