# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 21:58:39 2018

@author: Vit Saidl
"""

from collections import OrderedDict
from string import punctuation
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class JmenoSouboruNeuvedeno(Exception):
    """Exception třída na ošetření situace, kdy uživatel nezadá zdroj. soubor
    """

class NeznameKodovani(Exception):
    """Exception třída na zachycování problémů s kódováním načítaných souborů
    """

def nahraj_stopslova_ze_souboru(jmeno_souboru):
    """Nahrává (česká) stop slova ze souboru

    Args:
        jmeno_souboru: Jméno souboru vč. přípony
    """
    with open(jmeno_souboru, "r", encoding="utf8") as soubor:
        obsah_souboru = soubor.read()
        tokenizovany_obsah_souboru = obsah_souboru.split(", ")
    return tokenizovany_obsah_souboru

def otevri_soubor(jmeno_souboru, kodovani):
    """Fce načítá soubor a vrací jeho obsah v podobě stringu

    Může se stát to, že se soubor pokusíme otevřít ve špatném kódování. Tehdy
    se vrátí False a počítá se s tím, že volající fce zavolá otevri_soubor
    s jiným kódováním anebo to vzdá a vyhodí výjimku neznameKodovani

    Args:
        jmeno_souboru (string): Jméno txt souboru vč. cesty a přípony
        kodovani (string): Zkratka kódování (např. utf-8, ascii či cp1250)

    Returns:
        string: Obsah souboru (při nezdaru se vrací False)
    """
    try:
        with open(jmeno_souboru, "r", encoding=kodovani) as soubor:
            dokument = soubor.read()
        print(f"Nacteni souboru s pouzitim kodovani {kodovani} se zdarilo")
        return dokument
    except UnicodeDecodeError:
        print(f"Nacteni souboru s pouzitim kodovani {kodovani} se nepovedlo")
        return False

def nacti_dokument(jmeno_souboru):
    """Fce otevírá soubor s použitím několika kódování. Při nezdaru vyvolá výjimku.

    Pokud soubor nebyl vůbec zvolen, tak to vyvolá taky výjimku.

    Args:
        jmeno_souboru (string): Jméno txt souboru vč. cesty a přípony

    Returns:
        string: Obsah souboru (při nezdaru volaná výjimka)
    """
    default_label = "Zatím nebyl nahrán žádný textový soubor"
    if jmeno_souboru in ("", default_label):
        raise JmenoSouboruNeuvedeno("Před vytvořením wordcloudu je nutné uvést "
                                    "jméno souboru, který poslouží jako podklad "
                                    "pro wordcloud.")

    dokument = otevri_soubor(jmeno_souboru, "utf-8")
    if not dokument:
        dokument = otevri_soubor(jmeno_souboru, "ascii")
    if not dokument:
        dokument = otevri_soubor(jmeno_souboru, "cp1250")
    if not dokument:
        raise NeznameKodovani("Bohuzel se soubor nepodarilo otevrit s zadnym "
                              "kodovanim (pouzity byly utf-8, ascii a cp1250. "
                              "Neni v souboru nejaky podezrely paznak?")
    return dokument

def odstran_interpunkci(text):
    """Fce odstraňuje z textu veškerá interpunkční znaménka

    Args:
        text (string): Vstupní text načtený ze souboru

    Returns:
        string: Text očištěný o interpunkci
    """
    for znak_interpunkce in list(punctuation):
        text = text.replace(znak_interpunkce, "")
    #protože určité znaky interpunkce v punctuation nejsou
    for spec_znak_interpunkce in ["“", "”", "•", "–", "—"]:
        text = text.replace(spec_znak_interpunkce, "")
    return text

def uprav_text(text):
    """Úprava textu, aby se dal dále zpracovávat

    Aktuálně se všechna písmena převádí na malá a ostraňuje se interpunkce
    Args:
        text (string): Vstupní text načtený ze souboru

    Returns:
        string: vstupní text po určitých úpravách
    """
    text = text.lower()
    text = odstran_interpunkci(text)
    return text

def ocisti_text_o_stopwords(jazyk_stopwords, list_slov):
    """Fce z tokenizovaného textu odstraňuje stopwords

    Úpravy probíhají na listu, jehož reference se předává. Fce tak nic nevrací

    Args:
        jazyk_stopwords (string): Jazyk stopwords zvolený uživatelem
        list_slov (list): List stringů alias tokenizovaný text
    """

    if jazyk_stopwords == "Česká stopwords":
        stop_slova = nahraj_stopslova_ze_souboru("ceska_stop_slova.txt")
    elif jazyk_stopwords == "Anglická stopwords":
        stop_slova = STOPWORDS
    else:
        stop_slova = []

    for stop_slovo in stop_slova:
        #pokud by namísto while byl if, odstranil by se jen 1. výskyt stopslova
        while stop_slovo in list_slov:
            list_slov.remove(stop_slovo)

def vytvor_seznam_poctu_slov(text, jazyk_stopwords):
    """Načte soubor a vrátí OrderedDict počtu slov v něm

    Args:
        text (string): Obsah souboru, obvykle už předzpracovaný
        jazyk_stopwords (string): Jazyk stopwords zvolený uživatelem

    Returns:
        OrderedDict: Reverz. dle hodnoty (počtu slov) seřazený slovník; klíč = slovo
    """
    #text tokenizujeme podle mezer
    tokenizovany_text = text.split()
    ocisti_text_o_stopwords(jazyk_stopwords, tokenizovany_text)

    pocet_slov = []
    #pro každé slovo ukládáme počet jeho výskytů
    #a to i když se opakuje
    for slovo in tokenizovany_text:
        pocet_slov.append(tokenizovany_text.count(slovo))
    #převodem na slovík (který je množinou) se duplicity eliminují
    seznam = dict(zip(tokenizovany_text, pocet_slov))
    serazeny_seznam = OrderedDict(sorted(seznam.items(),
                                         key=lambda serazovany: serazovany[1],
                                         reverse=True)
                                  )
    return serazeny_seznam

def vygeneruj_wordcloud(max_pocet_slov, jazyk, text_dokumentu,
                        jmeno_souboru_masky, pouziti_masky, sirka_obrysu):
    """Fce zajišťující vytvoření wordcloudu

    Args:
        max_pocet_slov (integer): Počet slov, ze kterých se wordcloud vytvoří
        jazyk (string): Udává jazyk použitých stopslov
        text_dokumentu (string): Text sloužící jako podklad pro wordcloud
        jmeno_souboru_masky (string): Jméno obrázku vč. cesty a přípony
        pouziti_masky (bool): Zda se použije maska nebo wordcloud bude v obdelníku
        sirka_obrysu (integer): Šířka obrysu masky; 0 = obrys není

    Returns:
        wordcloud.wordcloud.WordCloud: Objekt - wordcloud
        wordcloud.color_from_image.ImageColorGenerator: Objekt s barvami masky
    """
    #očišťování o stopslova v obrazku zajišťuje wordcloudí balíček
    #nevoláme tudíž fci ocisti_text_o_stopwords
    if jazyk == "Česká stopwords":
        stop_slova = nahraj_stopslova_ze_souboru("ceska_stop_slova.txt")
        normalizace_mnoz_cisla = False
    elif jazyk == "Anglická stopwords":
        stop_slova = STOPWORDS
        normalizace_mnoz_cisla = True
    else:
        stop_slova = []
        normalizace_mnoz_cisla = False
    if pouziti_masky:
        maska = np.array(Image.open(jmeno_souboru_masky))
        #nastaveni objektu s barvou masky (bez tohoto by byly barvy nahodne)
        image_colors = ImageColorGenerator(maska)
        w_cloud = WordCloud(background_color="white", max_words=max_pocet_slov,
                            stopwords=stop_slova, mask=maska, width=1040,
                            height=520, normalize_plurals=normalizace_mnoz_cisla,
                            contour_width=sirka_obrysu)
    else:
        image_colors = None
        w_cloud = WordCloud(background_color="white", max_words=max_pocet_slov,
                            stopwords=stop_slova, width=1040, height=520,
                            normalize_plurals=normalizace_mnoz_cisla,
                            contour_width=sirka_obrysu)

    w_cloud.generate(text_dokumentu)
    return w_cloud, image_colors

def napln_oblast_pocet_slov(slovnik_poctu_slov):
    """Naplní oblast_poctu_slov dvojicemi počet výskytů slova - slovo

    Fce otevře oblast pro úpravy, celou ji smaže, vloží dvojice a opětovně oblast
    uzavře.

    Args:
        slovnik_poctu_slov(Dict): Klíčem je slovo a hodnotou počet jeho výskytů
    """
    pole_frekvence_slov.config(state=tk.NORMAL)
    pole_frekvence_slov.delete("1.0", tk.END)
    for klic, hodnota in slovnik_poctu_slov.items():
        pole_frekvence_slov.insert(tk.END,
                                   klic + " " + str(hodnota) + "\n")
    pole_frekvence_slov.config(state=tk.DISABLED)

def nastav_wc(kreslici_plocha, pouzite_platno):
    """Fce na základě vstupů (v rozhraní i ze souborů) nakreslí wordcloud

    Args:
        kreslici_plocha (AxesSubplot): (Sub)figure, ve kterém vykreslování probíhá
        pouzite_platno (FigureCanvasTkAgg): Samotný canvas, který je ve figuru
    """
    pocet_slov_obrazek = spinner_max_slov.get()
    jazyk_stopwords = combo_jazyk_stopwords.get()
    jmeno_souboru = label_nahrani_souboru.cget("text")
    jmeno_masky = label_nahrani_masky.cget("text")
    pouzit_masku = (checkbox_masky.state() == ('selected',))
    sirka_obrysu = spinner_obrys_sirka.get()

    try:
        nacteny_dokument = nacti_dokument(jmeno_souboru)
        predzpracovany_text = uprav_text(nacteny_dokument)
        slovnik_slov = vytvor_seznam_poctu_slov(predzpracovany_text,
                                                jazyk_stopwords)
        napln_oblast_pocet_slov(slovnik_slov)
        wordcloud, image_colors = vygeneruj_wordcloud(int(pocet_slov_obrazek),
                                                      jazyk_stopwords,
                                                      predzpracovany_text,
                                                      jmeno_masky,
                                                      pouzit_masku,
                                                      int(sirka_obrysu))
        if image_colors is None:
            kreslici_plocha.imshow(wordcloud,
                                   interpolation='bilinear')
        else:
            kreslici_plocha.imshow(wordcloud.recolor(color_func=image_colors),
                                   interpolation='bilinear')
        pouzite_platno.draw()

    except NeznameKodovani as problem_kodovani:
        messagebox.showerror("Error", problem_kodovani)
    except JmenoSouboruNeuvedeno as problem_zdroj_soubor:
        messagebox.showerror("Error", problem_zdroj_soubor)
    except FileNotFoundError as soubor_neni:
        messagebox.showerror("Error", str(soubor_neni))

def nahraj_lokaci_souboru():
    """Fce dovolí uživateli vybrat soubor, jehož jméno (vč. cesty) se uloží do labelu

    Fce je volaná po kliknutí na tlačítko "Nahrání textového souboru". Soubor
    by měl být typu txt (resp. měl by mít stejnou strukturu). Dialogové okno
    se otevírá v rootu, aby to uživatele zbytečně neházelo do jeho user složky.
    Label není měněn ničím jiným, takže zde slouží jako kontejner na jméno souboru.
    """
    jmeno_souboru = filedialog.askopenfilename(initialdir="/",
                                               title="Výběr textového souboru",
                                               filetypes=(("txt soubory", "*.txt"),
                                                          ("Všechny soubory", "*.*")))
    label_nahrani_souboru.config(text=jmeno_souboru)

def nahraj_lokaci_masky():
    """Fce dovolí uživateli vybrat soubor, jehož jméno (vč. cesty) se uloží do labelu

    Fce je volaná po kliknutí na tlačítko "Nahrání masky wordcloudu". Soubor
    by měl být typu png či jpeg . Dialogové okno se otevírá v rootu, aby to
    uživatele zbytečně neházelo do jeho user složky.
    Label není měněn ničím jiným, takže zde slouží jako kontejner na jméno souboru.
    """
    jmeno_souboru = filedialog.askopenfilename(initialdir="/",
                                               title="Výběr masky",
                                               filetypes=(("png soubory", "*.png"),
                                                          ("jpeg soubory", "*.jpg"),
                                                          ("Všechny soubory", "*.*")))
    label_nahrani_masky.config(text=jmeno_souboru)

def ulozeni_obrazku(pouzite_platno):
    """Uložení obrázku wordcloudu

    Args:
        pouzite_platno (FigureCanvasTkAgg): Samotný canvas, který je ve figuru
    """
    jmeno_souboru = filedialog.asksaveasfilename(title="Uložení wordcloudu",
                                                 defaultextension="jpg",
                                                 filetypes=[("jpeg soubory", "*.jpg")])
    if jmeno_souboru != "":
        pouzite_platno.print_jpg(jmeno_souboru)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wordcloudy")
    root.resizable(0, 0)

    hlavni_frame = ttk.Frame(root, padding=(3, 3, 12, 12))
    hlavni_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    hlavni_frame.columnconfigure(0, weight=1)
    hlavni_frame.rowconfigure(0, weight=1)

    labelframe_text = ttk.Labelframe(hlavni_frame, text="Zdrojový text")
    labelframe_text.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)

    button_nahrani_souboru = ttk.Button(labelframe_text,
                                        text="Nahrání textového souboru",
                                        command=nahraj_lokaci_souboru)
    button_nahrani_souboru.grid(column=0, row=0, padx=10)

    label_nahrani_souboru = ttk.Label(labelframe_text,
                                      text="Zatím nebyl nahrán žádný textový soubor")
    label_nahrani_souboru.grid(column=1, row=0, padx=10)

    labelframe_wc_prvky = ttk.Labelframe(hlavni_frame, text='Parametry wordcloudu')
    labelframe_wc_prvky.grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)

    label_spinner = ttk.Label(labelframe_wc_prvky,
                              text="Maximální počet slov v obrázku:")
    label_spinner.grid(column=0, row=0, padx=10)

    spinner_max_slov = tk.Spinbox(labelframe_wc_prvky, from_=1, to=500)
    spinner_max_slov.grid(column=1, row=0, padx=10)

    combo_jazyk_stopwords = ttk.Combobox(labelframe_wc_prvky,
                                         values=("Anglická stopwords",
                                                 "Česká stopwords",
                                                 "Žádná stopwords"),
                                         state="readonly", width=30)
    combo_jazyk_stopwords.set("Anglická stopwords")
    combo_jazyk_stopwords.grid(column=3, row=0, padx=10)

    labelframe_maska = ttk.Labelframe(hlavni_frame, text='Maska')
    labelframe_maska.grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)

    tlacitko_nahrani_masky = ttk.Button(labelframe_maska,
                                        text="Nahrání masky wordcloudu",
                                        command=nahraj_lokaci_masky)
    tlacitko_nahrani_masky.grid(column=0, row=0, padx=10)

    label_nahrani_masky = ttk.Label(labelframe_maska,
                                    text="Zatím nebyla nahrána žádná maska")
    label_nahrani_masky.grid(column=1, row=0, padx=10)

    checkbox_masky = ttk.Checkbutton(labelframe_maska, text="Použít masku")
    #aby se z checkboxu vymazal mezistav (ani zatržené, ani nezatržené)
    checkbox_masky.state(['!alternate'])
    #aby se checkbox natvrdo nastavil do unchecked modu; bez předchozího by
    #to nefungovalo
    checkbox_masky.state(['!selected'])
    checkbox_masky.grid(column=2, row=0, padx=10)

    label_obrys_sirka = ttk.Label(labelframe_maska, text="Šířka obrysu:")
    label_obrys_sirka.grid(column=3, row=0, padx=10)

    spinner_obrys_sirka = tk.Spinbox(labelframe_maska, from_=0, to=500)
    spinner_obrys_sirka.grid(column=4, row=0, padx=10)

    #z nejakeho duvodu platno bere na organizaci jenom pack; aby se ale se zbytkem
    #rozhrani dalo rozumne pracovat, je platno strceno do Framu, ktery se uz
    #k ostatnim castem rozhrani vztahuje gridem
    frame_obrazku = ttk.Frame(hlavni_frame, padding=(3, 3, 3, 3))
    frame_obrazku.grid(column=0, row=3)

    #do figsize jde tuple(vyska,sirka) - oboje v palcich
    obal_ramu = Figure(figsize=(10, 5), dpi=100)
    #používáme subplot, neb objekt Figure nemá metodu imshow
    #pro argument udávájící relativní polohu (X Y Z) je X-tá pozice
    #na řádku Y a sloupci Z
    #tady je to jedno, neb tu máme jen jeden subplot
    ram = obal_ramu.add_subplot(111)
    #na odstranění os (a čísel u os)
    ram.axis("off")
    #na odstranění bílých okrajů
    obal_ramu.subplots_adjust(left=0, right=1, bottom=0, top=1)

    platno = FigureCanvasTkAgg(obal_ramu, frame_obrazku)
    platno.draw()
    platno.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    button_vytvor_wc = ttk.Button(hlavni_frame, text="Vytvoř wordcloud obrázek",
                                  command=lambda: nastav_wc(ram, platno))
    button_vytvor_wc.grid(column=1, row=0)

    tlacitko_uloz_obrazek = ttk.Button(hlavni_frame, text="Uložení obrázku",
                                       command=lambda: ulozeni_obrazku(platno))
    tlacitko_uloz_obrazek.grid(column=1, row=1)

    label_popisek_slov = ttk.Label(hlavni_frame, text="Počet výskytů slov v textu")
    label_popisek_slov.grid(column=1, row=2)

    pole_frekvence_slov = tk.Text(hlavni_frame, height=31, width=25)
    pole_frekvence_slov.config(state=tk.DISABLED)
    pole_frekvence_slov.grid(column=1, row=3)

    root.mainloop()
