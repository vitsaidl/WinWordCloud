from custom_wordcloud import odstran_interpunkci

def test_odstranuje_interpunkci_z_balicku_string():
    retezec = "Jedna, dva tři! !!!? Co ke toto :"
    ocekavany = "Jedna dva tři  Co ke toto "
    skutecny = odstran_interpunkci(retezec)
    assert ocekavany == skutecny

def test_odstranuje_specialni_interpunkci():
    retezec = "Jedna, dva tři“ ”• Co ke toto –"
    ocekavany = "Jedna dva tři  Co ke toto "
    skutecny = odstran_interpunkci(retezec)
    assert ocekavany == skutecny

def test_s_textem_bez_interpunkce_nic_nedela():
    retezec = "Jedna dva tři  Co ke toto "
    ocekavany = "Jedna dva tři  Co ke toto "
    skutecny = odstran_interpunkci(retezec)
    assert ocekavany == skutecny
