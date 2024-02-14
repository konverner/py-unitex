import sys
sys.path.append('./src')

from unitex import Unitex, ProperNameParser


def test_cassys():
    unitex_path = r'C:\Users\konst\Documents\Unitex-GramLab\Unitex'
    executable_path = r"C:\Users\konst\PycharmProjects\textmining_project\Unitex-GramLab-3.3\App"
    cascade_name = 'loc.csc'
    lang = 'French'

    unitex_instance = Unitex(install_path=unitex_path,
                       install_path_app=executable_path,
                       lang=lang)

    test_cases = [
        ("On peut voir le lac de Montréal", ("lac de Montréal", "GEO")),
        ("qui dessert le refuge de la Jasse des Cortalets", ("refuge de la Jasse des Cortalets", "INF")),
        ("Tournez à droite sur la N33 et continuez sur 2 km.", ("N33", "INF")),
        ("Du col de la Valette, prendre le chemin", ("col de la Valette", "GEO")),
        ("Rester sur le sentier qui, en corniche, surplombe majestueusement le grotte du Chassezac.", ("grotte du Chassezac", "GEO")),
        ("Depart de la Gare de Landry.", ("Gare de Landry", "INF")),
        ("Tournez vers autoroute A 13", ("autoroute A 13", "INF")),
        ("Tournez vers la route départementale 66", ("route départementale 66", "INF")),
        ("Je habite à 33 rue de la Paix", ("33 rue de la Paix", "INF")),
        ("Il habite 3 Rue du 7 Août 79000 Niort", ("3 Rue du 7 Août 79000 Niort", "INF")),
        ("Vue sur le Mont Blanc de Courmayeur.", ("Mont Blanc de Courmayeur", "GEO")),
        ("Le site naturel du Nez de Jobourg", ("site naturel du Nez de Jobourg", "INF")),
        ("Traverser successivement les hameaux de Mouchel et de Samson", ("hameaux de Mouchel et de Samson", "GPE")),
        ("Départ carrefour D24 et D 643 vers le hameau.", ("carrefour D24 et D 643", "INF")),
        ("La statue est à gauche et le sommet se trouve sur votre droite.. Rocher d'Abraham au sommet belle vue.", ("Rocher d'Abraham", "GEO")),
    ]

    for test_case in test_cases:
        spans = unitex_instance.get_spans(test_case[0], cascade_name)
        assert len(spans) == 1, f"Sample {test_case[0]}"
        assert spans[0]['text'] == test_case[1][0], f"Sample: {test_case[0]}, expected: {test_case[1][0]}, got: {spans[0]['text']}"
        assert spans[0]['label'] == test_case[1][1], f"Sample: {test_case[0]}, expected: {test_case[1][1]}, got: {spans[0]['label']}"


def test_spans_alignment():
    unitex_path = r'C:\Users\konst\Documents\Unitex-GramLab\Unitex'
    executable_path = r"C:\Users\konst\PycharmProjects\textmining_project\Unitex-GramLab-3.3\App"
    cascade_name = 'loc.csc'
    lang = 'French'

    unitex_instance = Unitex(install_path=unitex_path,
                       install_path_app=executable_path,
                       lang=lang)

    test_cases = [
        ("Je voyage par GR33 j'aime GR33", [(14, 18, "GR33"), (26, 30, "GR33")]),
        ("Vue sur le Mont Blanc de Courmayeur. La panorama pendant de longs moments sur le Mont Blanc italien",
         [(11, 35, "Mont Blanc de Courmayeur"), (81, 91, "Mont Blanc")]),
        ("Je habite à 33 rue de la Paix; mon ami habite à 33 avenue du 11 Novembre",
         [(12, 29, "33 rue de la Paix"), (48, 72, "33 avenue du 11 Novembre")]),
        ("J'ai vu la rivière de la Dordogne ce matin! Il a vu massif des Aiguilles Rouges",
         [(11, 33, "rivière de la Dordogne"), (52, 79, "massif des Aiguilles Rouges")]),
    ]

    for test_case in test_cases:
        spans = unitex_instance.get_spans(test_case[0], cascade_name)
        assert len(spans) == len(test_case[1])
        for i in range(len(spans)):
            assert spans[i]['start'] == test_case[1][i][0]
            assert spans[i]['end'] == test_case[1][i][1]
            assert spans[i]['text'] == test_case[1][i][2]

def test_parser():
    parser = ProperNameParser()
    test_cases = [
        (
            r"{route départementale \{D202\,\.ROAD_ID\},.INF}",
            [{'label': 'INF', 'proper_name': 'D202', 'syntagme': 'route départementale'}]
        ),
        (
            r"{\{D202\,\.ROAD_ID\},.INF}",
            [{'label': 'INF', 'proper_name': 'D202', 'syntagme': ''}]
        ),
        (
            r"{Chemin des\{ Médecins\,\.PN\},.INF}",
            [{'label': 'INF', 'proper_name': 'Médecins', 'syntagme': 'Chemin des'}]
        )
    ]
    for test_case in test_cases:
        result = parser.parse_entry(test_case[0])
        for i in range(len(result)):
            assert result[i]['label'] == test_case[1][i]['label']
            assert result[i]['proper_name'] == test_case[1][i]['proper_name']
            assert result[i]['syntagme'] == test_case[1][i]['syntagme']
