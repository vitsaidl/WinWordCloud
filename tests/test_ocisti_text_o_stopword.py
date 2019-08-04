from custom_wordcloud import ocisti_text_o_stopwords

def test_vyhozeni_anglickych_stopwords():
    zdrojovy_list = ["is", "this", "a", "word", "or", "a", "part", "of", "a", "sentence"]
    ocekavany = ["word", "part", "sentence"]
    ocisti_text_o_stopwords("Anglická stopwords", zdrojovy_list)
    assert ocekavany == zdrojovy_list

def test_vyhozeni_ceskych_stopwords():
    zdrojovy_list = ["toto", "je", "slovo", "a", "toto", "taky"]
    ocekavany = ["slovo"]
    ocisti_text_o_stopwords("Česká stopwords", zdrojovy_list)
    assert ocekavany == zdrojovy_list

def test_nevyhazovani_stopwords():
    zdrojovy_list = ["toto", "je", "slovo", "a", "toto", "taky"]
    ocekavany = ["toto", "je", "slovo", "a", "toto", "taky"]
    ocisti_text_o_stopwords("Žádná stopwords", zdrojovy_list)
    assert ocekavany == zdrojovy_list