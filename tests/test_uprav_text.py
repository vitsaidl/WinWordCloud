from custom_wordcloud import uprav_text

def test_zmenseni_pismen():
    retezec = "jedNA DVA Tri ctyri "
    ocekavany = "jedna dva tri ctyri "
    skutecny = uprav_text(retezec)
    assert ocekavany == skutecny

def test_odstranuje_interpunkci_z_balicku_string():
    retezec = "jedna, dva tři! !!!? co ke toto :"
    ocekavany = "jedna dva tři  co ke toto "
    skutecny = uprav_text(retezec)
    assert ocekavany == skutecny

def test_odstranuje_specialni_interpunkci():
    retezec = "jedna, dva tři“ ”• co ke toto –"
    ocekavany = "jedna dva tři  co ke toto "
    skutecny = uprav_text(retezec)
    assert ocekavany == skutecny

def test_text_bez_velkych_pismen_a_interpunkce():
    retezec = "jedna dva tři  co ke toto "
    ocekavany = "jedna dva tři  co ke toto "
    skutecny = uprav_text(retezec)
    assert ocekavany == skutecny