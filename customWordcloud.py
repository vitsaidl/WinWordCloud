# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 21:58:39 2018

@author: NewNotebook
"""

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  #dokumentace k wordcloudu na http://amueller.github.io/word_cloud/
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from string import punctuation
from PIL import Image
import numpy as np


ceskaStopSlova = ["a","i","nebo", "ten", "tam", "jak", "v", "je", "na", "že", "ze", "se", "s", "z", "o", "mezi", "to", "po", "by", "k", "tak", "ve", "ke", "aby", "co","ja", "já", "jsem", "ale", "ty", "no", "si", "uz", "už", "do", "tedy", "jsou", "u", "za", "ti", "pro", "neni", "není", "bude", "nez", "než", "vy", "ta", "tady", "jsme", "jste","me", "mě", "mne", "bylo", "jako", "tom", "at", "ať", "tu", "te", "té", "tě", "od", "na", "protoze", "protože", "kdyz", "když", "pokud", "ktere", "které", "ten", "tam", "jak", "tomu", "toho", "ma", "má", "vam", "Vám", "Vam", "Vy", "vám", "jeste", "ještě", "těch", "ktery", "který", "tím", "tim", "nas", "nás", "mam", "mám", "toto", "nad", "byl", "budu", "take", "také", "jeho", "však", "vsak","byla","již", "jiz", "svou", "sve", "své", "kterou", "pred", "před", "pak", "az", "až", "či", "ci", "mu" ]


def nacteniDokumentu(jmeno):
    dokument = ""
    with open(jmeno, "r",encoding="utf-8") as f:           #takto se soubor zavre i kdyz dojde k chybe; pokud hrozi specialni (treba ceske) znaky, nutno zadat encoding; jinak si asi mysli, ze ma ascii, a pak to pada
        dokument = f.read()                                 #nezapominat na zavorky, jinak to vrati <built-in method read of _io.TextIOWrapper object at 0x0000023A5A324708>
    return dokument

def upravaTextu(text):                      #nasledujici prikazy potrebuje jak serazovac frekvenci, tak wordcloud, takze jsem udelal separatni funkci
    text = text.lower()                     #nejdriv se vsechna pismena prevedou na mala
    for p in list(punctuation):             #nasledne se odstrani interpunkce
       text=text.replace(p,"")
    for q in ["“","”", "•","–"]:            #protože tenhle typ interpunkkce v punctuation není
        text=text.replace(q,"")
    return text

def udelejFrekvenciSlov(jazyk):
    text = nacteniDokumentu(labelNahraniSouboru.cget("text"))
    text = upravaTextu(text)
    textNaFrekvence = text.split()                              #split rozdeli text podle separatoru v parametru; pokud zadny parametr neni, bere se jako separator mezera
    stopSlova = []
    
    if(jazyk == "Česká stopwords"): stopSlova = ceskaStopSlova
    elif (jazyk == "Anglická stopwords"): stopSlova = STOPWORDS
    for stopSlovo in stopSlova:                                 #pro kazde slovo v STOPWORDS
        while stopSlovo in textNaFrekvence: textNaFrekvence.remove(stopSlovo)   #se odebira z textNaFrekvence, dokud to jde; pokud bych misto while dal if, odstranil by se jen prvni vyskyt
    
    frekvence = []                                              #inicializace listu
    
    for slovo in textNaFrekvence:                               #pro kazde slovo v textu (a to i kdyz se opakuje)
        frekvence.append(textNaFrekvence.count(slovo))          #se do listu "frekvecne" vlozi pocet vyskytu onoho slova 
    seznam = dict(zip(textNaFrekvence, frekvence))              #zip tvori tuple z i-tych prvku listu v argumentu - zde spojuje slova a pocet jejich vyskytu; nasledne se to prevede na dictionary, cimz se eliminuji duplicity - slovnik je mnozina
    serazenySeznam = []
    for klic in seznam:                                         #problem se slvonike je, ze nemuze byt serazen
        serazenySeznam.append((seznam[klic], klic))             #proto se do noveho listu vlozi tuply - dvojice pocet vyskytu slova, slovo
    serazenySeznam.sort()                                         #prvky tohot o seznamu se seradi
    serazenySeznam.reverse()                                      #a to sice reverzne, tj. od nejcetnejsiho slova
    return serazenySeznam
    
def vygenerujWordcloud(maxSlov, jazyk):
    jmenoSouboru = labelNahraniSouboru.cget("text")             #z labelu se vezmou adresy text. souboru a masky
    jmenoMasky = labelNahraniMasky.cget("text")
    text = nacteniDokumentu(jmenoSouboru)                       #text se musi nacist vzdy
    text = upravaTextu(text)                                    #a pak se upravi
    stopSlova = []
    if(jazyk == "Česká stopwords"): 
        stopSlova = ceskaStopSlova
        normalizaceMnozCisla = False
    elif (jazyk == "Anglická stopwords"): 
        stopSlova = STOPWORDS
        normalizaceMnozCisla = True
    if(checkBoxMasky.state() == ('selected',)):                 #pokud je checkbox u masky zatrzen
        maska = np.array(Image.open(jmenoMasky))                #nacte se maska
        image_colors = ImageColorGenerator(maska)               #a nastavi se jeji barvy (bez tohoto by byly barvy nahodne)
        wc = WordCloud(background_color="white", max_words=maxSlov, stopwords = stopSlova,  mask = maska,width = 1040, height = 520, normalize_plurals = normalizaceMnozCisla) #vytvori objekt typu wordcloud
    else:
        wc = WordCloud(background_color="white", max_words=maxSlov, stopwords = stopSlova, width = 1040, height = 520, normalize_plurals = normalizaceMnozCisla) #vytvori objekt typu wordcloud
        image_colors = None
    wc.generate(text)                                                                   #a naplni ho textem
    return (wc, image_colors) #vracet chci totiz dve ruzne veci

def nastavWC(*args):
    global a                                    #aby promenna (blbe davana do parametru funkce) byla globalni a my ji tady mohli upravovat
    cislo = spinnerMaxSlov.get()                #do promenne cislo se ulozi aktualni cifra v spinneru
    jazyk = jazykStopwords.get()
    frekvence = udelejFrekvenciSlov(jazyk)
    poleFrekvenceSlov.config(state=tk.NORMAL) #docasne otevreni textoveho pole pro upravy
    poleFrekvenceSlov.delete("1.0", tk.END)     #vymaže celý obsah tkinterovskeho elementu
    for dvojice in frekvence:
      poleFrekvenceSlov.insert(tk.END, str(dvojice[0]) + " " + dvojice[1] + "\n")  #do textoveho pole se radek po radku vlozi slovo a pocet jeho vyskytu
    poleFrekvenceSlov.config(state=tk.DISABLED)  #aby uzivatel nemohl textove pole upravovat
    a.clear                                     #vyciteny acka od predchoziho kresleni
    wordcloud, image_colors = vygenerujWordcloud(int(cislo), jazyk)  #prijimam dve ruzne veci
    
    
    if(image_colors == None):                       #pokud se z fce vygenerujWordcloud vratila image_color = None, znamena to, ze maska nebyla nactena a tudiz se ani nema pri vytvareni wordcloudu volat
        a.imshow(wordcloud, interpolation='bilinear') #prekresleni acka; kdybych nechtel barvy podle masky, tak by prvni parametr byl pouze nazev wordcloudoveho objektu
    else:
        a.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear') #prekresleni acka; kdybych nechtel barvy podle masky, tak by prvni parametr byl pouze nazev wordcloudoveho objektu
    canvas.draw()                               #prekresleni platna                     

def nahrajLokaciSouboru(*args):
    jmenoSouboru =filedialog.askopenfilename(initialdir = "/",title = "Výběr textového souboru", filetypes = (("txt soubory","*.txt"),("Všechny soubory","*.*")))  #initialdir je tady root, aby to nekoukalo do user/documents
    labelNahraniSouboru.config(text = jmenoSouboru)
        
def nahrajLokaciMasky(*args):
    jmenoSouboru = filedialog.askopenfilename(initialdir = "/",title = "Výběr masky", filetypes = (("png soubory","*.png"),("jpeg soubory","*.jpg"),("Všechny soubory","*.*")))  #initialdir je tady root, aby to nekoukalo do user/documents
    labelNahraniMasky.config(text = jmenoSouboru)
    
def ulozeniObrazku(*args):
    global canvas
    jmenoSouboru = filedialog.asksaveasfilename(title = "Uložení wordcloudu", defaultextension = "jpg")
    if(jmenoSouboru != ""):
        canvas.print_jpg(jmenoSouboru)
    



root = tk.Tk()     #vytvoření základního okna, jelikož ale v tomhle nemůžou být specializované widgety, musí se udělat mainframe jako dítě rootu
root.title("Wordcloudy")  #název okna

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))   #vytvoreni hlavniho framu; prvni parametr je rodic framu, druhy padding neboli odsazeni od kraju
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

tlacitkoNahrajSoubor = ttk.Button(mainframe, text= "Nahranání textového souboru", command = nahrajLokaciSouboru)
tlacitkoNahrajSoubor.grid(column=0, row=0, sticky =tk.W)

labelNahraniSouboru = ttk.Label(mainframe, text="Zatím nebyl nahrán žádný textový soubor")
labelNahraniSouboru.grid(column=0, row=1, sticky = tk.W)

jazykStopwords = ttk.Combobox(mainframe, values=("Anglická stopwords", "Česká stopwords"), state = "readonly", width = 30)
jazykStopwords.set("Anglická stopwords")
jazykStopwords.grid(column = 0, row  = 2, sticky = tk.W)

spinnerMaxSlov = tk.Spinbox(mainframe, from_=1, to=500)
spinnerMaxSlov.grid(column=0, row=0)

labelSpinner = ttk.Label(mainframe, text="Maximální počet slov v obrázku:")
labelSpinner.grid(column=0, row=1)

tlacitkoUlozObrazek = ttk.Button(mainframe, text= "Uložení obrázku", command = ulozeniObrazku)
tlacitkoUlozObrazek.grid(column=0, row=2)

tlacitkoNahrajMasku = ttk.Button(mainframe, text= "Nahranání masky wordcloudu", command = nahrajLokaciMasky)
tlacitkoNahrajMasku.grid(column=0, row=0, sticky =tk.E)

labelNahraniMasky = ttk.Label(mainframe, text="Zatím nebyla nahrána žádná maska")
labelNahraniMasky.grid(column=0, row=1, sticky = tk.E)

checkBoxMasky = ttk.Checkbutton(mainframe, text = "Použít masku")
checkBoxMasky.state(['!alternate'])                                     #aby se z checkboxu vymazal mezistav (ani zatrzene, ani nezatrzene)
checkBoxMasky.state(['!selected'])                                      #aby se checkbox natvrdo nastavil do unchecked modu; bez predchoziho by to nefungovalo
checkBoxMasky.grid(column = 0, row = 2, sticky = tk.E)



tlacitko = ttk.Button(mainframe, text= "Vytvoř wordcloud obrázek", command = nastavWC)
tlacitko.grid(column=1, row=0)


frameObrazku = ttk.Frame(mainframe, padding=(3, 3, 3, 3))   #z nejakeho duvodu platno bere na organizaci jenom pack; aby se ale se zbytkem rozhrani dalo rozumne pracovat, je platno strceno do Framu, ktery se uz k ostatnim castem rozhrani vztahuje gridem
frameObrazku.grid(column=0, row=3)

f = Figure(figsize=(10,5), dpi=100)                         #figsize je tuple(vyska,sirka) - oboje v palcich, dpi rozliseni
a = f.add_subplot(111)                                      #udava relativni polohu (X Y Z) je X-ta pozice na radku Y a sloupci Z; tady je to jedno, neb tu mame jen jednu vec
a.axis("off")                                               #na odstraneni os (a cisel u os)
f.subplots_adjust(left=0,right=1,bottom=0,top=1)            #na odstraneni bilych okraju

canvas = FigureCanvasTkAgg(f, frameObrazku)                    #vytvori se canvas, ve kterem se vyklesi Figure
canvas.draw()                                               #az timto prikaze mdochazi k samotnemu vykresleni
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) #na platne jsou prvky nejak drzeny pomoci packu
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


labelPopisekSlov = ttk.Label(mainframe, text="Počet výskytů slov v textu")
labelPopisekSlov.grid(column=1, row=2)


poleFrekvenceSlov = tk.Text(mainframe, height = 31, width = 25)
poleFrekvenceSlov.config(state=tk.DISABLED)  #aby uzivatel nemohl textove pole upravovat
poleFrekvenceSlov.grid(column = 1, row = 3)

root.mainloop()   