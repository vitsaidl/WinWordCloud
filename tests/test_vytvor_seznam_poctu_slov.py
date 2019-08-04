from collections import OrderedDict
from custom_wordcloud import vytvor_seznam_poctu_slov

def test_vraci_se_spravny_pocet_slov():
    zdrojovy_text = "toto je slovo a slovo a ty tvoří větu"
    vraceny_seznam = vytvor_seznam_poctu_slov(zdrojovy_text, "Česká stopwords")
    ocekavany_seznam = OrderedDict({"slovo":2, "tvoří":1, "větu":1})
    assert ocekavany_seznam == vraceny_seznam