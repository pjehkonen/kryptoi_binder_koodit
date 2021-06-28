# Author: Petri Jehkonen (at) xiphera.com

import random, math, string, glob, os
from random import choices
import numpy as np
from numpy import binary_repr
import matplotlib.pyplot as plt
import pprint
from scipy.interpolate import interp1d
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels.api as sm
import warnings
from datetime import date
from datetime import datetime
from dateutil import relativedelta


def salaa_merkeittäin(viesti=None, avain=0x6A, debugging=False):
    if viesti is None:
        viesti = "Kahvi Charlotassa on hyvää ja vahvaa!"

    # Unicodesta Latin-1 koodaukseen ja tavuihin, tekninen seikka, ei oleellista
    b_viesti = bytes(viesti, encoding="latin_1")
    # Paikka enkoodatulle viestille
    c_enkoodattu = []

    # Suoritetaan salaus merkeittäin
    for tavu in b_viesti:
        if debugging:
            print("Merkki  {}".format(chr(tavu)))
            print("Bitit   {}".format(binary_repr(tavu,8)))
            print("Avain   {}".format(binary_repr(avain,8)))
            print("XOR     {}".format(binary_repr(avain^tavu,8)))
            print("Sala    {}".format(chr(avain^tavu)))
        c_enkoodattu.append(avain^tavu)

    if debugging:
        print("Viesti joka enkoodataan on:")
        print(viesti+"\n")

        print("Avain jota käytämme salauksessa on:",hex(k),"\n")

        print("Tavuittain enkoodattu viesti näyttää seuraavalta:")
        for tavu in c_enkoodattu:
            print(chr(tavu),end='')
    return c_enkoodattu


def vertaa_maailmankaikkeuden_ikään(avaimiin_kuluva_aika_a):
    # Verrataan maailmankaikkeuden arveltuun ikään.
    maailmankaikkeudenikä_vuosina = 13787000000
    print("Maailmankaikkeuden ikä vuosina: {} vuotta.".format(maailmankaikkeudenikä_vuosina))

    kertaa_maailmankaikkeuden_ikä= avaimiin_kuluva_aika_a/maailmankaikkeudenikä_vuosina
    print("Avainten laskenta vaatii {:.3e} -kertaa maailmankaikkeuden iän.".format(kertaa_maailmankaikkeuden_ikä))

    erotus = avaimiin_kuluva_aika_a - maailmankaikkeudenikä_vuosina

    if erotus <0:
        print("Tämä olisi keretty laskemaan maailmankaikkeuden arvioidussa elinajassa")
    else:
        if erotus>20000:
            print("Ihmisellä ei ole ollut mitään toivoa laskea tätä avainta")
        else:
            print("Ihmiskunta olisi kerennyt jääkauden jälkeen laskemaan avaimen")


def avaimen_laskemiseen_kuluva_aika(bittejä=None, avainta_sekunnissa=None, debugging=False):
    # Tuotetaan avainten määrä, voit vaihtaa bittimäärää.
    if bittejä is None:
        bittejä = 128

    if avainta_sekunnissa is None:
        avainta_sekunnissa=10**12


    avainten_lukumäärä = 2**bittejä
    avaimiin_kuluva_aika_s = avainten_lukumäärä/avainta_sekunnissa # sekunteina
    avaimiin_kuluva_aika_a = avaimiin_kuluva_aika_s/(60*60*24*365) # vuosina
    print("{}-bittisen avaimen laskemiseen nopeudella {:.2e} avainta sekunnissa,".format(bittejä,avainta_sekunnissa))
    print("kuluu {:.3e} vuotta".format( avaimiin_kuluva_aika_a))
    return avaimiin_kuluva_aika_a


def nist112bits_diff(debugging=False):
    nist_112bits = date.fromisoformat('2015-01-01')
    tänään = date.today()
    ero_kuukausia = (tänään.year-nist_112bits.year)*12 + tänään.month-nist_112bits.month
    if debugging:
        print("Ero kuukausina:",ero_kuukausia)

    mooren_laki_kk = 18
    bittiä_lisää = ero_kuukausia//mooren_laki_kk
    if debugging:
        print("Tarvitaan {} bittiä lisää.".format(bittiä_lisää))
    return bittiä_lisää


def näytäkorrelaatiot(data, siirrokset=40, otsikko="Ei otsikkoa"):
    fig, ax = plt.subplots(1,2,figsize=(10,5))
    sm.graphics.tsa.plot_acf(data, lags=siirrokset, ax=ax[0])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sm.graphics.tsa.plot_pacf(data, lags=siirrokset, zero=True, ax=ax[1])
    plt.suptitle("{}".format(otsikko))
    plt.show()


def tuotajakaumia(n=10000):
    x  = np.arange(n)
    y1 = np.arange(n)
    nolla_ysi = [0,1,2,3,4,5,6,7,8,9]
    y2 = np.repeat(nolla_ysi,int(n/len(nolla_ysi)))
    y3 = np.random.normal(int(n/2), int(n/7), n).astype(int)
    y4 = np.random.randint(0,n,n)

    return y1, y2, y3, y4


def heittelyt(noppa=None, kolikko=None, n=4000000, siemen=20211221, n_bins=3):

    if (noppa is None and kolikko is None) or (noppa and kolikko):
        print("Anna joko noppa=True tai kolikko=True")
        return "En ymmärrä"

    if kolikko:
        max_luku = 2
        x_paikat = np.array([0.2, 0.8])
        x_labelit=['Kruuna','Klaava']
        label = "Kolikon"
    else:
        max_luku = 6
        #x_paikat = np.arange(0, max_luku)
        x_paikat = np.array([0.22, 1.15, 2.05, 2.98, 3.85, 4.8])
        x_labelit=['1','2', '3', '4', '5', '6']
        n_bins=11
        label = "Nopan"
    # Asetetaan siemen
    np.random.seed(siemen)

    # Luodaan neljä otosta
    y1 = np.random.randint(0,max_luku,n)
    y2 = np.random.randint(0,max_luku,n)
    y3 = np.random.randint(0,max_luku,n)
    y4 = np.random.randint(0,max_luku,n)

    fig, axes = plt.subplots(2, 2, figsize=(9,9), sharex=False, sharey=False)
    fig.suptitle('{} heittokertojen vertailu histogrammeilla n ={}'.format(label,n))
    axes[0, 0].hist(y1, bins=n_bins)
    axes[0, 0].set_title('Ensimmäinet {} heittoa'.format(n))
    axes[0, 1].hist(y2, bins=n_bins)
    axes[0, 1].set_title('Toiset {} heittoa'.format(n))
    axes[1, 0].hist(y3, bins=n_bins)
    axes[1, 0].set_title('Kolmannet {} heittoa'.format(n))
    axes[1, 1].hist(y4, bins=n_bins)
    axes[1, 1].set_title('Neljännet {} heittoa'.format(n))

    for ax in axes.flat:
        ax.set_xticks(x_paikat)
        ax.set_xticklabels(x_labelit)

    for ax in axes.flat:
        ax.set(xlabel='Tulos', ylabel='Lukumäärä')

    fig.tight_layout()
    plt.show()


def näytäjakaumia(n_bins=50):
    # Luodaan neljä jakaumaa joissa n-kpl näytteitä
    n  = 10000

    y1, y2, y3, y4 = tuotajakaumia()

    fig, axes = plt.subplots(2, 2, figsize=(12,6), sharex=False, sharey=False)
    fig.suptitle('Jakaumien vertailu histogrammeilla n ={} | bins={}'.format(n,n_bins))
    axes[0, 0].hist(y1, bins=n_bins)
    axes[0, 0].set_title('Tasajakauma')
    axes[0, 1].hist(y2, bins=n_bins)
    axes[0, 1].set_title('Toistuva')
    axes[1, 0].hist(y3, bins=n_bins)
    axes[1, 0].set_title('Normaalijakauma')
    axes[1, 1].hist(y4, bins=n_bins)
    axes[1, 1].set_title('Tasajakauma')

    for ax in axes.flat:
        ax.set(xlabel='Satunnaismuuttujan arvo', ylabel='Lukumäärä')

    fig.tight_layout()
    plt.show()


def salain_a(viesti):
    return atbash(viesti)


def atbash(viesti="Kahvi Charlotassa on hyvää ja vahvaa"):
    substituutio = atbash_substituutio()
    muunnos = []
    for kirjain in viesti:
        if substituutio.get(kirjain)==None:
            muunnos.append(' ')
        else:
            muunnos.append(substituutio.get(kirjain))
    return "".join(muunnos)


def atbash_substituutio():
    kirjaimet = string.ascii_uppercase + 'ÅÄÖ'
    substituutio = dict(zip(kirjaimet,kirjaimet[::-1]))
    return substituutio


# Message for wrong string arguments
def gen_alphabets_argument_error(lower_edge, upper_edge):
    print("Alphabets should be in increasing order such as abc...")
    print("Unable to generate string from "+lower_edge+" to "+upper_edge)

# Function returning alphabets in uppercase
def uppercase_alphabets():
    alphabets = string.ascii_uppercase
    return list(alphabets)

# Function returns alphabets for a range, by default a to z provided
def generate_alphabets(lower_edge='a', upper_edge='z'):
    if ord(lower_edge)>=ord(upper_edge):
        gen_alphabets_argument_error(lower_edge, upper_edge)
        alphabets = []
    else:
        alphabets = [chr(i) for i in range(ord(lower_edge),ord(upper_edge)+1)]
    return "".join(alphabets)

# Function to print given alphabets and order
def print_alphabets(alphabets=string.ascii_uppercase, print_order=True):
    print("".join(alphabets))
    idx = [i for i in range(0,len(alphabsets))]
    print(idx)


# Function keeping only the characters in dictionary
def preprocess_text(plain_text, dictionary, debug=False):
    plain_text_ok = []
    for character in plain_text:
        if character in dictionary:
            plain_text_ok.append(character)
    if debug:
        print("Plain text before preprocessing:")
        print(plain_text)
        print("Plain text after preprocessing;")
        print("".join(plain_text_ok))
    return "".join(plain_text_ok)


# Introduce caesar cipher
# Note: while decrypting names of variables are opposite (plain <-> cipher)

def salain_b(viesti, avain):
    isot, pienet = merkistot(suomi=True)
    return caesar(viesti,aakkosto=isot, avain=avain)

def caesar(esikäsitelty_teksti, aakkosto=None, avain=3, purku=False, debuggaus=False):

    if debuggaus:
        print("Saatiin viesti ", esikäsitelty_teksti)

    pienet = ""
    if aakkosto is None:
        print("Aakkostoa ei annettu, valitaan suomen aakkoset!")
        aakkosto, pienet = merkistot(suomi=True)

    if debuggaus:
        print("Aakkosto on ", aakkosto)

    # Jos argumentiksi annetaan suoraan tekstiä, se ei välttämättä ole esikäsitelty, tehdään esikäsittely.
    esikäsitelty_teksti = esikasittele_teksti(esikäsitelty_teksti,aakkosto+pienet)

    if debuggaus:
        print("Muunnettava viesti",esikäsitelty_teksti)

    # Lista johon laitetaan muunnoksen tulos
    muunnettu_teksti = []
    # Muunnos suoritetaan merkki merkiltä
    for kirjain in esikäsitelty_teksti:
        # Aakkoston oletetaan olevan järjestetty ja sisältää vain isot kirjaimet
        # Käsiteltävän kirjaimen suhteellinen paikka aakkostossa
        ennen_muunnosta = aakkosto.index(kirjain)-aakkosto.index(aakkosto[0])
        # Tässä suoritetaan muunnoksen indeksi laskenta
        if not purku:
            muunnoksen_jälkeen=(ennen_muunnosta+avain)%len(aakkosto)
        else:
            muunnoksen_jälkeen=(ennen_muunnosta-avain)%len(aakkosto)

        # Lisätään muunnokseen
        muunnettu_teksti.append(aakkosto[muunnoksen_jälkeen])
        if debuggaus:
            print("Merkki: "+ kirjain +" on muunnettuna : ",aakkosto[muunnoksen_jälkeen])
            print("Aakkoston indeksi ennen muunnosta    : ",ennen_muunnosta)
            print("Aakkoston indeksi muunnoksen jälkeen : ",muunnoksen_jälkeen)

    return "".join(muunnettu_teksti)


def laske_siirros(aakkosto, avain, purku=False, debuggaus=False):
    if not purku:
        siirros = [aakkosto.index(merkki) for merkki in list(avain)]
    else:
        siirros = [-(aakkosto.index(merkki)) for merkki in list(avain)]
    if debuggaus:
        print(siirros)
    return siirros


# Function generates offset for Vigenére cipher key based on dictionary
def generate_offset(dictionary, key, decrypt=False, debug=False):
    first_idx = ord(dictionary[0])
    if not decrypt:
        offset_idx = [ord(x)-first_idx for x in list(key)]
    else:
        offset_idx = [-(ord(x)-first_idx) for x in list(key)]
    if debug:
        print(offset_idx)
    return first_idx, offset_idx


def salain_c(viesti, avain):
    return vigenere(viesti, avain=avain)

def vigenere(viesti, aakkosto=None, avain="GIOVAN", purku=False, debuggaus=False):

    pienet=""
    if aakkosto is None:
        aakkosto, pienet = merkistot(suomi=True)

    alkuviesti = esikasittele_teksti(viesti, aakkosto+pienet)

    muunnettu_viesti = []

    # Generate ascii index of the first alphabet and offset list
    siirroslista = laske_siirros(aakkosto, avain, purku, debuggaus)

    if debuggaus:
        print("Saatu viesti  : ",viesti)
        print("Alkuviesti    : ",alkuviesti)

    for i,kirjain in enumerate(alkuviesti):
        ennen_muunnosta = aakkosto.index(kirjain)
        siirros_indeksi= (ennen_muunnosta+(siirroslista[i%len(siirroslista)]))%len(aakkosto)
        muunnettu_viesti.append(aakkosto[siirros_indeksi])
        if debuggaus:
            print("Viestin merkki : {}".format(i))
            print("Ennen muunnosta: ", ennen_muunnosta)
            print("Siirros indeksi: ", siirros_indeksi)
            print("Kirjain: "+ kirjain +" muunnetaan: ",aakkosto[siirros_indeksi])

    return "".join(muunnettu_viesti)


# Introduce vigenere chipher, decrypt setting flag
def vigenere_old(plain_text, dictionary, key="GIOVAN", decrypt=False, debug=False):
    # Convert message to contain only characters or letters in dictionary
    plain_text = preprocess_text(plain_text, dictionary)

    chipher_text = []
    # Generate ascii index of the first alphabet and offset list
    first_idx, offset_idx = generate_offset(dictionary,key, decrypt)

    for i,letter in enumerate(plain_text):
        before_index = ord(letter)-first_idx
        chipher_index= (before_index+(offset_idx[i%len(offset_idx)]))%len(dictionary)
        after_index = chipher_index + first_idx
        chipher_text.append(dictionary[chipher_index])
        if debug:
            print("Text index: ",before_index)
            print("Transform index", chipher_index)
            print("Character: "+ letter +" is chipered to: ",dictionary[chipher_index])

    return "".join(chipher_text)


# This function generates quizz with fixed secret key and plan text
def generate_quizz_caesar():
    dictionary = generate_alphabets('A','Z')
    plain_text = "CATS RULE THE WORLD"
    secret_key = 5
    cipher_text = caesar(plain_text, dictionary, secret_key)
    #decrypt_message = caesar(cipher_text, dictionary, secret_key, decrypt=True)
    return cipher_text

# Generate array of integers covering required bits
def generate_int_table(number_of_bits):
    """Generates integer table 2^number_of_bits

    Parameters
    ----------
    number_of_bits : int
        2^number_of_bits numbers are generated

    Returns
    -------
    numpy.array(np.int64)
        a array of integers

    Raises
    ------
        If too large amount of data is required assert NoGo.

    """

    # Limit the table presentation to avoid excess wait time during print().
    if number_of_bits >=19:
        raise NoGo("Please select less than 19-bits!")
    # Generate numpy array of nuympy.int64 values to cover all given bits
    return np.array([i for i in range(2**number_of_bits)])

# Display bit table takes input as table of integers
def display_bit_table(table_n, number_of_bits):
    assert isinstance(table_n[0], np.int64), "Table elements should be numpy integers"
    for element in table_n:
        print(binary_repr(element, number_of_bits))


# Generates random key from given
def generate_key(table_n, message_len=1, text='Key', debug=False):
    r_val = np.random.choice(table_n, message_len)
    if debug:
        for i in range(len(r_val)):
            print(text,"is",r_val[i],"with bit pattern",binary_repr(r_val[i], number_of_bits))
    return r_val

# Generates random plaintext from dictionary table_n, with message lengt mesg_len
def generate_plaintext(table_n, mesg_len=1, debug=False):
    plaintext = [generate_key(table_n,text='Plaintext', debug=debug) for i in range(mesg_len)]
    if len(plaintext)==1:
        return plaintext[0]
    else:
        return plaintext

def XOR(key, text):
    return key ^ text

def S_BOX_XOR(key, block):

    block_bin_string = ""
    for element in block.T:
        for value in element:
            block_bin_string += binary_repr(value,8)
    block_as_int = int(block_bin_string,2)
    r_val = key^block_as_int
    return make_s_box(r_val)


# This is weak byt we are using pseudorandom number generator
def gen_bits(n=128, k_rand=False):
    if k_rand:
        return random.getrandbits(n)
    else:
        return 0xe9e6c63c50b95304b9db65e1ef613913

def b_to_s(in_byte):
    return "0x"+binary_repr(in_byte,8)

# Generate substitution box. Default encoding utf-8, alternative latin_1
def make_s_box(plaintext, n_sboxes=16, encoding='utf-8', aes_bits=128):
    dim = int(np.sqrt(n_sboxes))
    if isinstance(plaintext, str):
        b_plaintext = bytearray(plaintext,encoding)
        s_boxes = np.array(b_plaintext[:n_sboxes]).reshape([dim,dim]).T
        return s_boxes
    elif isinstance(plaintext, int):
        int_array =[]
        bit_string = binary_repr(plaintext, aes_bits)
        step_size = len(bit_string)//n_sboxes
        for i in range(n_sboxes):
            int_array.append(int(bit_string[i*step_size:i*step_size+step_size],2))
        s_boxes = np.array(int_array).reshape([dim,dim]).T
        return s_boxes
    else:
        print("error in make_s_box")
        return None

def print_s_boxes(s_boxes, o_format='HEX'):
    dim=s_boxes.shape[0]

    if o_format=='integers':
        print("S-box content as integers:")
        print(s_boxes)

    if o_format=='binary':
        print("S-box content as binary")
        for i in range(dim):
            print(binary_repr(s_boxes[i][0],8),binary_repr(s_boxes[i][1],8),binary_repr(s_boxes[i][2],8),binary_repr(s_boxes[i][3],8))

    if o_format=='letters':
        print("S-box content as characters:")
        for i in range(dim):
            print(chr(s_boxes[i][0]),chr(s_boxes[i][1]),chr(s_boxes[i][2]),chr(s_boxes[i][3]))

    if o_format=='HEX':
        print("S-box content as hex")
        for i in range(dim):
            print("{0:#0{1}x} ".format(s_boxes[i][0], 4),end='')
            print("{0:#0{1}x} ".format(s_boxes[i][1], 4),end='')
            print("{0:#0{1}x} ".format(s_boxes[i][2], 4),end='')
            print("{0:#0{1}x}".format(s_boxes[i][3], 4))

    print("")

def show_string_conversion(plaintext, n_sboxes=16, encoding='utf-8'):
    # Visalize first how the first part of message appears as character->integer->binary
    b_plaintext = bytearray(plaintext, encoding) # alternatively latin_1, for äöå
    for letter in b_plaintext[:n_sboxes]:
        print("Letter: {} -> {:3d} bin: {}  hex:{}".format(chr(letter), letter,binary_repr(letter,8),hex(letter)))


def give_random_text():
    text_selection = random.randint(0, len(plaintexts))
    plaintext = plaintexts[text_selection]
    return plaintext



def circ_buf(bits, direction, n_bits, word_len=128, debug=False):
    """Circular buffer rotating left or right.

    Parameters
    ----------
    bits : integer
        bitstring to be rotated
    direction : chr
        'l'->left ; 'r'->right
    n_bits : int
        Number of bits to be rotated left or right
    word_len : int, optional
        Defaulting to 128 bits for aes_bits
    debug : bool, optional
        Default 'False', if 'True' prints detailed debug values
    """

    assert n_bits < word_len, "Function support rotating less than word lenght"
    # Create string of input bits
    binary_string = binary_repr(bits, word_len)

    # Create mask applied to return rolled bits with OR operation
    if direction=='l':
        or_mask = '0'*(word_len-n_bits)+binary_string[:n_bits]
    else:
        or_mask = binary_string[word_len-n_bits:]+'0'*(word_len-n_bits)
    or_mask = int(or_mask,2)

    # Create mask limiting the word length to same as original
    and_mask = ""
    for i in range(word_len):
        and_mask+='1'
    and_mask = int('00'+and_mask,2)

    if direction=='l':
        r_val = ((bits<<n_bits) & and_mask) | or_mask
    else:
        r_val = ((bits>>n_bits) & and_mask) | or_mask

    if debug:
        if direction=='l':
            print("Rotating left")
        else:
            print("Rotating right")
        print("")
        print("Word lenght:",word_len)
        print("Shift  bits:",n_bits)
        print("Binary str :",binary_string)
        print("Or mask    : {0:#0{1}x}".format(or_mask, 2+word_len//4))
        print("Mask       :",hex(and_mask))
        print("")
        print("Input  bits:",binary_repr(bits, word_len))
        print("Output bits:",binary_repr(r_val,word_len))
        print("Input  hex :",hex(bits))
        print("Output hex :",hex(r_val))
        print("")

    return r_val


def SBOX_LUT():
    all_rows = []
    all_rows.append([0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76])
    all_rows.append([0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0])
    all_rows.append([0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15])
    all_rows.append([0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75])
    all_rows.append([0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84])
    all_rows.append([0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf])
    all_rows.append([0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8])
    all_rows.append([0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2])
    all_rows.append([0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73])
    all_rows.append([0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb])
    all_rows.append([0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79])
    all_rows.append([0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08])
    all_rows.append([0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a])
    all_rows.append([0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e])
    all_rows.append([0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf])
    all_rows.append([0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16])

    AES_LUT={}

    for r_number, list_row in enumerate(all_rows):
        row = {}
        for i in range(0x10):
            row[i]=list_row[i]
        AES_LUT[r_number]=row

    return AES_LUT


def SBOX_INVLUT():
    all_rows = []
    all_rows.append([0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb])
    all_rows.append([0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb])
    all_rows.append([0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e])
    all_rows.append([0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25])
    all_rows.append([0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92])
    all_rows.append([0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84])
    all_rows.append([0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06])
    all_rows.append([0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b])
    all_rows.append([0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73])
    all_rows.append([0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e])
    all_rows.append([0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b])
    all_rows.append([0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4])
    all_rows.append([0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f])
    all_rows.append([0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef])
    all_rows.append([0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61])
    all_rows.append([0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d])

    AES_INV_LUT={}

    for r_number, list_row in enumerate(all_rows):
        row = {}
        for i in range(0x10):
            row[i]=list_row[i]
        AES_INV_LUT[r_number]=row

    return AES_INV_LUT

# S-box or inverse S-box should be in dictionary[row][column] format.
def print_AES_SBOX(AES_SBOX):
    print("     ",end='')
    for i in range(16):
        print("{0:#0{1}x} ".format(i, 4), end='')
    print("")
    for i, row in enumerate(AES_SBOX.keys()):
        print("{0:#0{1}x} ".format(i<<4, 4), end='')
        for key in AES_SBOX[row].keys():
            print("{0:#0{1}x} ".format(AES_SBOX[row][key],4), end='')
        print("")

# Substitute bytes with given LUT, it can be iverse or forward LUT
def sub_bytes(s_boxes, LUT, debug=False):
    dim = s_boxes.shape[0]
    int_substitutes = []
    for element in s_boxes.T:
        for value in element:
            if debug:
                print("value :",hex(value))
                print("s-box :",hex(nyberg_substitution(value, LUT)))
            int_substitutes.append(nyberg_substitution(value, LUT))
    return np.array(int_substitutes).reshape([dim,dim]).T

# Function performs parsing of the current byte and returns LUT
def nyberg_substitution(u_integer, LUT, debug=False):
    high = (u_integer & 0xF0)>>4
    low  = u_integer & 0x0F
    if debug:
        print("high  :",hex(high))
        print("low   :",hex(low))
        print("LUT   :",hex(LUT[high][low]))
        print("")
    return LUT[high][low]


# AES Key Schedule

# Define round constant. Initialzation without arguments
def AES_key_schedule_round_constant(r_prev, r=1, word_len=32, debug=False):
    hex_80    = 0b10000000000000000000000000000000
    hex_1B    = 0b00011011000000000000000000000000
    if r==1:
        r_val = 0x01000000 #(32-bit)
    else:
        msb_set = r_prev & hex_80
        if debug:
            print("d:"+'0x{0:0{1}X}'.format(r_prev<<1,int(word_len/4)))
        r_val = (r_prev << 1) & 0x00FFFFFFFF

        if msb_set:
            r_val = r_val ^ hex_1B

    if debug:
        print("Round:",r, "returned value is")
        print("Bin:",binary_repr(r_val,32))
        print("Hex:"+'0x{0:0{1}X}'.format(r_val,int(word_len/4)))
    return r_val

def generate_rcon(debug=False):
    Rcon = []
    Rcon.append(AES_key_schedule_round_constant(0,1,word_len=32, debug=debug))
    for i in range(2,11):
        Rcon.append(AES_key_schedule_round_constant(Rcon[i-2],i))

    if debug:
        for element in Rcon:
            print("{}".format(binary_repr(element,32)))

    return Rcon


def key_expansion(K, Nb, Nr, Nk, key_len, word_len, LUT, debug=False):
    k_string = binary_repr(K,key_len)
    b  =[k_string[i:i+word_len] for i in range(0,key_len,key_len//Nk)]
    W = []
    Rcon = generate_rcon()

    # First four 32-bit words
    counter = 0
    for element in b:
        W.append(int(element,2))
        counter+=1

    # Rest of (4 * 11) - 4  round keys
    while ((counter-3) < (Nb*Nr+1)):
        temp = W[counter-1]
        if debug:
            print("Counter     ",counter)
            print("temp        ",hex(temp))
            print("Rcon index  ",(counter-4)//Nk)
        if (counter % Nk == 0):
            r_word = rot_word(temp)
            s_word = sub_word(r_word, LUT)
            r_con  = Rcon[(counter-4)//Nk]
            temp = s_word ^ r_con
            if debug:
                print("Rot word    ",hex(r_word))
                print("Sub word    ",hex(s_word))
                print("Rcon         0x{0:0{1}x}".format(Rcon[(counter-4)//Nk],8))
                print("Temp        ",hex(temp))
        r_res = W[counter-Nk]^temp
        if debug:
            print("W[coun-Nk-1] 0x{0:0{1}x}".format(W[counter-Nk],8))
            print("Result      ", hex(r_res))
        W.append(r_res)
        counter += 1
        if debug:
            print("")


    if debug:
        print("Cipher Key: ",hex(K))
        for i, element in enumerate(W):
            print("W_{:2d} {}".format(i,hex(element)))

    return W


# rotate word in circular buffer one byte left
def rot_word(i_word, n_bytes=4, debug=False):
    bit_string = binary_repr(i_word,n_bytes*8)
    o_string = bit_string[8:]+bit_string[:8]
    if debug:
        print("Input string  :",bit_string)
        print("Output string :",o_string)
        print("Hex(int(o,2)) :",hex(int(o_string,2)))
    return int(o_string,2)


def sub_word(i_word, LUT, n_bytes=4, debug=False):
    n = 8
    bit_string = binary_repr(i_word,n_bytes*n)
    b  =[bit_string[i:i+n] for i in range(0,len(bit_string),n)]
    sb =[nyberg_substitution(int(i,2),LUT) for i in b]
    o_word = ""
    for element in sb:
        o_word += binary_repr(element,8)

    if debug:
        print("Input word as bitstring :",bit_string)
        for i,element in enumerate(b):
            print("Byte : ",i,"{} -> {}".format(hex(int(element,2)),hex(sb[i])))

        print("Output word as bitstring:",o_word)
    return int(o_word,2)


def shiftrows(s_box, debug=False):
    dimensions = s_box.shape
    datatype = type(s_box[0][0])
    rows = dimensions[1]
    # Create same shape output as input, with same datatype as input
    r_val = np.empty(dimensions, dtype=datatype)
    for i in range(rows):
        r_val[i]=s_box[i,[i, (i+1)%rows, (i+2)%rows, (i+3)%rows]]
    if debug:
        print("Got s-box:")
        print(s_box)
        print("With rows")
        print(rows)
        print("The shiftrows output:")
        print(r_val)
    return r_val


def gf2_mul2(value, debug=False):
    msb_set = value & 0x80
    res = value << 1
    if msb_set:
        res = res ^ 0x1B
        res = res & 0x00FF
    if debug:
        print("GF2 Mul 2")
        print("input :",hex(value))
        print("output:",hex(res))
        if msb_set:
            print("MSB was set")
    return res

def gf2_mul3(value, debug=False):
    res = gf2_mul2(value,debug=debug)
    res = res ^ value
    if debug:
        print("GF2 mul 3")
        print("input :",hex(value))
        print("output:",hex(res))
    return res


def mix_columns(s_box, debug=False):
    mul_mat= np.array([[2, 3, 1, 1],[1, 2, 3, 1],[1, 1, 2, 3],[3, 1, 1, 2]])
    dimensions = s_box.shape
    datatype = type(s_box[0][0])
    r_val = np.empty(dimensions, dtype=datatype)
    if debug:
        print_s_boxes(s_box)
        print(r_val)
    for i, col in enumerate(s_box.T):
        r_val[i] = np.array([gf2_mul2(col[0])^gf2_mul3(col[1])^col[2]^col[3],
                             col[0]^gf2_mul2(col[1])^gf2_mul3(col[2])^col[3],
                             col[0]^col[1]^gf2_mul2(col[2])^gf2_mul3(col[3]),
                             gf2_mul3(col[0])^col[1]^col[2]^gf2_mul2(col[3])])
        if debug:
            print("Column i: ",i)
            print(r_val)
            print_s_boxes(r_val)
    return r_val.T



def merkistot(suomi = False):
    isot = string.ascii_uppercase
    pienet = string.ascii_lowercase
    numerot = string.digits
    if not suomi:
        return isot, pienet
    else:
        return isot+'ÅÄÖ', pienet+'åäö'

def harjoituksen_tiedostot(tunniste=None):

    if tunniste is None:
        hakemisto = "Tekstit/*.md"

    tiedostot = glob.glob(hakemisto)
    return sorted(tiedostot)

def suomi():
    sanakirja = {
        "A": 11.9,
        "I": 10.64,
        "T": 9.77,
        "N": 8.67,
        "E": 8.21,
        "S": 7.85,
        "L": 5.68,
        "O": 5.34,
        "K": 5.24,
        "U": 5.06,
        "Ä": 4.59,
        "M": 3.3,
        "V": 2.52,
        "R": 2.32,
        "J": 1.91,
        "H": 1.83,
        "Y": 1.79,
        "P": 1.74,
        "D": 0.85,
        "Ö": 0.49,
        "G": 0.13,
        "B": 0.06,
        "F": 0.06,
        "C": 0.04,
        "W": 0.01,
        "Å": 0.0,
        "Q": 0.0,
        "X": 0.0,
        "Z": 0.0
    }
    return sanakirja



def vertaa_selväkieli_salakieli(selväteksti, salateksti, otsikko="Ei otsikkoa", kurvi=False):

    aakkoset, _ = merkistot(suomi=True)

    selvä_pros  = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())
    sala_pros   = list(frekvenssi_prosenteiksi(tuota_frekvenssit(salateksti), salateksti).values())

    x = np.arange(len(aakkoset))



    fig, ax = plt.subplots(figsize=(16,6))
    plt.bar(x-0.2, selvä_pros, width=0.4, ls='dotted',lw=3, fc=(0, 0, 1, 0.5), label = "Selväteksti")
    plt.bar(x+0.2, sala_pros,  width=0.4, ls='dotted',lw=3, fc=(1, 0, 0, 0.5), label = "Salateksti")

    for i,v in enumerate(selvä_pros):
        ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

    for i,v in enumerate(sala_pros):
        ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    plt.xticks(x,x_labels)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain",fontsize=18)
    plt.legend()
    plt.title("Selvä vs Sala: {}".format(otsikko),fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max() , num=600, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    plt.show()



def show_kirjainjakauma(kirjaimet = None, osuus = None, nimi=None, vain_aineisto=False, savefile=False ):
    s_kirjaimet=('A','I','T','N','E','S','L','O','K','U','Ä','M','V','R','J','H','Y','P','D','Ö','G','B','F','C','W','Å','Q','X','Z')
    s_osuus = [11.9, 10.64, 9.77, 8.67, 8.21, 7.85, 5.68, 5.34, 5.24, 5.06, 4.59, 3.30, 2.52, 2.32, 1.91, 1.83, 1.79, 1.74, 0.85, 0.49, 0.13, 0.06, 0.06, 0.04, 0.01, 0.0, 0.0, 0.0, 0.0]

    x = np.arange(len(s_kirjaimet))

    fig, ax = plt.subplots(figsize=(16,6))

    if kirjaimet is None:
        läpinäkyvyys = 0.9
        leveys = 0.8
    else:
        läpinäkyvyys = 0.4
        leveys = 0.5

        järjestetty_lista = []
        for i,kirjain in enumerate(s_kirjaimet):
            järjestetty_lista.append(osuus[kirjaimet.index(kirjain)])


    if not vain_aineisto:
        plt.bar(x, s_osuus, width=leveys, ls='dotted',lw=3, fc=(0, 0, 1, läpinäkyvyys), label = "Suomen kielen kirjainjakauma")

    if kirjaimet is not None:
        if vain_aineisto:
            plt.bar(x, osuus, ls='dashed',lw=5, fc=(1,0,0,0.6), label="Aineisto "+nimi)
        else:
            plt.bar(x, järjestetty_lista, ls='dashed',lw=5, fc=(1,0,0,0.6), label="Aineisto "+nimi)

    if vain_aineisto:
        plt.xticks(x,kirjaimet)
    else:
        plt.xticks(x,s_kirjaimet)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain",fontsize=18)
    plt.legend()

    if not vain_aineisto:
        for i, v in enumerate(s_osuus):
            ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=läpinäkyvyys, fontweight='bold')

    if kirjaimet is not None:
        if vain_aineisto:
            for i,v in enumerate(osuus):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')
        else:
            for i,v in enumerate(järjestetty_lista):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    if nimi is None:
        plt.title("Suomen kielen kirjainjakauma",fontsize=20)
    else:
        plt.title("Aineisto: {}".format(nimi),fontsize=20)

    if savefile:
        plt.savefig("suomen_kirjainjakauma.png",dpi=150)
    else:
        plt.show()



# Funktio joka trimmaa tekstin sallittuihin merkkeihin
def esikasittele_teksti(plain_text, dictionary, debug=False):
    plain_text_ok = []
    for character in plain_text:
        if character in dictionary:
            plain_text_ok.append(character.capitalize())
    if debug:
        print("Plain text before preprocessing:")
        print(plain_text)
        print("Plain text after preprocessing;")
        print("".join(plain_text_ok))
    return "".join(plain_text_ok)


# Funktio joka palauttaa aakkoset ja frekvenssit
def tuota_frekvenssit(teksti):
    isot, _ = merkistot(suomi=True)
    kirjainesiintymät = {}
    for kirjain in isot:
        kirjainesiintymät[kirjain]=0
    for kirjain in teksti:
        kirjainesiintymät[kirjain] += 1
    return kirjainesiintymät


def frekvenssi_prosenteiksi(frekvenssi_sanakirja, teksti):
    sanakirja = {}
    for key in frekvenssi_sanakirja.keys():
        sanakirja[key]= np.round(100*frekvenssi_sanakirja[key]/len(teksti), decimals=2)
    return sanakirja


def laske_frekvenssit(teksti):
    kirjainesiintymät = tuota_frekvenssit(teksti)
    esiintymisjärjestys = sorted(kirjainesiintymät.items(), key=lambda x:x[1], reverse=True)
    kirjaimet   = []
    frekvenssit = []
    for pari in esiintymisjärjestys:
        kirjaimet.append(pari[0])
        frekvenssit.append(pari[1])

    prosentit = np.round(100*np.array(frekvenssit)/len(teksti),decimals=2)

    return kirjaimet, prosentit

def laske_frekvenssi_ero_suomeen(sanakirja, verbose=False):
    suomen_jakauma = suomi()
    rms = 0
    for key in suomen_jakauma:
        ero = suomen_jakauma[key]-sanakirja[key]
        rms += np.square(ero)
        if verbose:
            print("Ero suomen kieleen kirjaimella {} on {:5} prosenttia".format(key,np.round(ero ,decimals=2)))

    return np.round(rms,decimals=2)


# Apufunktio joka tulostaa permutaatiot.
def näytä_permutaatiot(viesti):

    viestissä_merkkejä = len(viesti)
    # luodaan indeksilista viestistä
    indeksit = [i for i in range(viestissä_merkkejä)]
    # luodaan satunnaisesti järjestetyt indeksit
    permutoidut_indeksit = random.sample(indeksit, k=viestissä_merkkejä)
    # tehdään salateksti poimimalla permutoidun indeksin järjestyksessä kirjaimet
    salateksti = [viesti[i] for i in permutoidut_indeksit]

    # Tulostetaan viestin tiedot ja yksi permutaatio
    print("Selkoviesti: {} pituus: {}".format(viesti, viestissä_merkkejä))
    print("Mahdollisia permutaatioita: {}".format(math.factorial(viestissä_merkkejä)))
    print("Alkuperäiset indeksit:\n{}\n{}".format(list(viesti),indeksit))
    print("Satunnainen permutaatio:\n{}\n{}".format(salateksti,permutoidut_indeksit))
    print("Salakieli edellisellä permutaatiolla: {}".format("".join(salateksti)))



def onetimepad(viesti="KAHVICHARLOTASSAONHYVÄÄJAVAHVAA"):
    aakkoset = string.ascii_uppercase + 'ÅÄÖ'
    viestissä_merkkejä = len(viesti)
    satunnaisotos=choices(aakkoset, k=len(viesti))
    return "".join(satunnaisotos), vigenere(viesti, aakkosto=aakkoset, avain="".join(satunnaisotos), purku=False, debuggaus=False)



def testaa_hyökkäysmallien_osaaminen(viesti,avain):
    if salain_c(viesti,avain)=='ÄZLRÖYFMVO':
        print("Hienoa, voit edetä harjoituksiin tai lounaalle!")
    else:
        print("Ei aivan, voit kysyä apuja kavereilta tai opettajilta")

def generoi_caesar_haaste(debuggaus=False, purku=False):
    viesti='Ensilumi suli, takatalvi tuli!'
    isot, pienet = merkistot(suomi=True)
    esikäsitelty_viesti = esikasittele_teksti(viesti, isot+pienet)

    if debuggaus:
        print("Alkuperäinen viesti  :", viesti)
        print("Esikäsitelty viesti  :", esikäsitelty_viesti)


    # Suoritetaan Caesar salaus edellisillä arvoilla
    salateksti=caesar(esikäsitelty_viesti,aakkosto=isot, avain=11, purku=False)
    if debuggaus:
        print("Caesar salateksti on :",salateksti)

    # Suoritetaan salauksen purku asettamalla purku-lippu arvoon True
    dekoodattu_teksti=caesar(salateksti,aakkosto=isot, avain=11, purku=True)
    if debuggaus:
        print("Caesar dekoodattu on :",dekoodattu_teksti)

    if not purku:
        return salateksti
    else:
        return dekoodattu_teksti

def freq_analyze(tiedosto, debuggaus=False):
    # Ensiksi määritellään aakkosto
    isot, pienet = merkistot(suomi=True)
    sallitut = isot + pienet
    aakkoston_koko = len(''.join(set(isot)))
    if debuggaus:
        print("Tekstistä poimitaan vain seuraavat sallitut kirjaimet")
        print(sallitut)
        print("Suomen aakkosia on {}".format(aakkoston_koko))

    tekstitiedostot = harjoituksen_tiedostot()
    nimi = os.path.basename(tekstitiedostot[tiedosto])[:-3]
    teksti = ""
    with open(tekstitiedostot[tiedosto], "r", encoding="utf_8") as file:
        teksti = file.read()
    # Muodostetaan tekstistä kirjainjono, jossa on vain sallitut aakkoset a..ö ja A..Ö
    kirjainjono = esikasittele_teksti(teksti, sallitut)
    kirjainjonon_merkit = ''.join(set(kirjainjono))

    print("Kirjainjonon pitus on {} merkkiä".format(len(kirjainjono)))
    print("Ja siinä esiintyy yhteensä {} eri aakkosta.".format(len(kirjainjonon_merkit)))
    if aakkoston_koko - len(kirjainjonon_merkit) != 0:
        print("Kirjainjonon puuttuvat kirjaimet ovat {}".format(''.join(set(isot).difference(kirjainjonon_merkit))))
    #print("Kirjainjono näyttää tältä:" +kirjainjono)

    # Lasketaan
    frekvenssi_kirjaimet, frekvenssi_prosentit = laske_frekvenssit(kirjainjono)
    show_kirjainjakauma(tuple(frekvenssi_kirjaimet),frekvenssi_prosentit, nimi)

    määrät = tuota_frekvenssit(kirjainjono)
    prosentit = frekvenssi_prosenteiksi(määrät, kirjainjono)
    poikkeaa_suomen_kielestä = laske_frekvenssi_ero_suomeen(prosentit)
    print("{} kirjoitus poikkeaa {} määrän suomen kielestä".format(nimi, poikkeaa_suomen_kielestä))

def näytä_tekstit():
    tekstitiedostot = harjoituksen_tiedostot()
    print("Saatavilla olevat tiedostot")
    for i, nimi in enumerate(sorted(tekstitiedostot)):
        print("Tiedostoindeksi: {} on {}".format(i,nimi[8:-3]))


def lue_tiedosto_merkkijonoksi(indeksi=None, debuggaus=False):
    if indeksi is None:
        print("Et antanut indeksiä.\n")
        näytä_tekstit()
        alkuperäinen_viesti=""
    else:
        tiedosto=indeksi
        isot, pienet = merkistot(suomi=True)
        sallitut = isot + pienet
        aakkoston_koko = len(''.join(set(isot)))

        if debuggaus:
            print("Tekstistä poimitaan vain seuraavat sallitut kirjaimet")
            print(sallitut)
            print("Suomen aakkosia on {}".format(aakkoston_koko))

        tekstitiedostot = harjoituksen_tiedostot()
        nimi = os.path.basename(tekstitiedostot[tiedosto])[:-3]
        teksti = ""
        with open(tekstitiedostot[tiedosto], "r", encoding="utf_8") as file:
            teksti = file.read()
        # Muodostetaan tekstistä kirjainjono, jossa on vain sallitut aakkoset a..ö ja A..Ö
        alkuperäinen_viesti = esikasittele_teksti(teksti, sallitut)
        kirjainjonon_merkit = ''.join(set(alkuperäinen_viesti))
    return alkuperäinen_viesti

def materiaalin_freq(viesti, otsikko="Ei annettu otsikkoa"):
    # Lasketaan frekvenssit
    frekvenssi_kirjaimet, frekvenssi_prosentit = laske_frekvenssit(viesti)
    show_kirjainjakauma(tuple(frekvenssi_kirjaimet),frekvenssi_prosentit, otsikko)

def vertaa_selväkieli_salakieli(selväteksti, salateksti="", otsikko=None, kurvi=False, debuggaus=False):

    salateksti_puuttuu = len(salateksti)==0
    if salateksti_puuttuu:
        print("väärä funktio, tarvitsen selvätekstin ja salatekstin")
    aakkoset, _ = merkistot(suomi=True)
    leveys = 0.8

    selvä_pros  = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())

    if not salateksti_puuttuu:
        sala_pros   = list(frekvenssi_prosenteiksi(tuota_frekvenssit(salateksti), salateksti).values())
        leveys = 0.8

    if debuggaus:
        print("selväteksti:", selväteksti)
        print("salateksti :", salateksti)
        print("selväpros  :", selvä_pros)
        print("salapros   :", sala_pros)

    x = np.arange(len(aakkoset))

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16,12))

    x_siirros = 0


    axes[0].bar(x-x_siirros, selvä_pros, width=leveys, ls='dotted',lw=3, fc=(0, 0, 1, 0.5), label = "Selväteksti")
    axes[1].bar(x+x_siirros, sala_pros,  width=leveys, ls='dotted',lw=3, fc=(1, 0, 0, 0.5), label = "Salateksti")

    if False:
        for i,v in enumerate(selvä_pros):
            axes[0].text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

        if not salateksti_puuttuu:
            for i,v in enumerate(sala_pros):
                axes[1].text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    axes[0].set_xticks(x,minor=False)
    axes[1].set_xticks(x,minor=False)
    axes[0].set_xticklabels(x_labels, fontdict=None, minor=False)
    axes[1].set_xticklabels(x_labels, fontdict=None, minor=False)

    axes[0].title.set_text('Selväteksti')
    axes[1].title.set_text('Salateksti')

    axes[0].set_ylabel('Esiintymistiheys', fontsize=16)
    axes[1].set_ylabel('Esiintymistiheys', fontsize=16)

    #axes[0].set_xlabel("Kirjain",fontsize=18)
    axes[1].set_xlabel("Kirjain",fontsize=18)

    axes[0].legend()
    axes[1].legend()



    if otsikko is None:
        otsikko="Tuntematon aineisto"

    fig.suptitle("Aineisto: {}".format(otsikko),fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max() , num=601, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    plt.show()


def tekstin_frekvenssi_aakkosissa(selväteksti, salateksti="", otsikko=None, kurvi=False, tiedostoon=False, debuggaus=False):

    salateksti_puuttuu = len(salateksti)==0
    aakkoset, _ = merkistot(suomi=True)
    leveys = 0.8

    selvä_pros  = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())

    if not salateksti_puuttuu:
        sala_pros   = list(frekvenssi_prosenteiksi(tuota_frekvenssit(salateksti), salateksti).values())
        leveys = 0.4

    if debuggaus:
        print("selväteksti:", selväteksti)
        print("salateksti :", salateksti)
        print("selväpros  :", selvä_pros)
        print("salapros   :", sala_pros)

    x = np.arange(len(aakkoset))

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16,6))

    if salateksti_puuttuu:
        x_siirros = 0
    else:
        x_siirros = 0.2

    ax.bar(x-x_siirros, selvä_pros, width=leveys, ls='dotted',lw=3, fc=(0, 0, 1, 0.5), label = "Selväteksti")

    if not salateksti_puuttuu:
        ax.bar(x+x_siirros, sala_pros,  width=leveys, ls='dotted',lw=3, fc=(1, 0, 0, 0.5), label = "Salateksti")

    if False:
        for i,v in enumerate(selvä_pros):
            ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

        if not salateksti_puuttuu:
            for i,v in enumerate(sala_pros):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    plt.xticks(x,x_labels)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain",fontsize=18)
    plt.legend()

    if otsikko is None:
        otsikko="Tuntematon aineisto"

    plt.title("Aineisto: {}".format(otsikko),fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max() , num=601, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    if tiedostoon:
        plt.savefig("frekvenssi.png")
    else:
        plt.show()

def freq_testi_a():
    return "LOQÖÖPUSÖJSYRQÖPVYPSURAVÖVQOJÖLOQÖÖPUSÖJSYRQÖNÖIROÅOYRVOÖRSYQUKJUNOUSÖORUORRIJSLUKJÖRRUSÖINNUÖÖPNÖRHYRISKYKKÖQYRSYUPSIISÖIZYPHÖUSSÖJEAORUSÖUSSYÖQIIJÖSIUPUVÖPJYYRRUKJÖSÖINNUÖKQÖLQÖJJUJUKSUPKBJÖSÖPÖSÖUSYPNBUHBBSOQYPKUNOUSÖÖTÖHÖLOUJJUKBLSYQBKJBQUJBBPQIJJÖNOUSÖVÖRIKUNEKEBJEANÖUSÖKKÖÖPKURRBPÖRSIJJÖQUKYKJÖÖPVIORUQÖJJÖHÖPVÖSÖINNUÖKYUORRIJYNBOUSYIZYPQISÖUPYPVBPKÖUVEHBPNÖRSSUOPTOSÖUKYKJÖQEEQBKJBBPYKUPYYKJBTÖORUYVJUPEJKBBKJBBTOPSUPHYLLÖPLÖVÖÖKUPBÖÖQIPÖVBPORURÖKSYKSYRRIJYJJBTOKVBPJYSUKUJEAJBTOSÖNBUHBSIJYPORUJYVPEJKUUVYPSUPÖKJUVBPYPORUKUIILÖKJYJJÖHÖHIOKUYPPYPSIUPHOUKUOKJÖÖNÖLURÖQQÖKJÖVÖRIÖUKUPNEKJEJJBBQEEPJUNAEZBPSLUKJÖRRUYKUPYURRYNOUSÖKÖPOUSÖINNUÖÖRRYKYPHOUKUNÖPPÖIRSONIORYRRYPUUPYJJBKYVOISIJJYRUKUJBPPYHBSYBSISSIRÖPTIILYRJÖQUPIRRÖYUORYORRIJSOKSÖÖPKYRRÖUKJÖNAEJBBSÖINNUÖKHÖKJÖKUUVQUKYJJALQBBHBJKUUVYPTÖKBLSYHBJSLUKJÖRRUJSIPSIRTUPRÖUJIQYRRÖRÖQNÖUJJYPUSÖPKKÖHÖÖLÖPÖORUÖUPÖYJJBPUUZYPJUYRRYOKIUKUSBBLQYTÖYJJBPYSIORUKUHÖJQIJJÖKYRRÖUKJÖOPRÖQNÖUZYPTÖNÖUQYPYPYRBQBSÖINNUÖKSBBPJEUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖVÖRIKUSORQYSLUKJÖRRURÖKUÖVBPQEUPESEBBPNÖLYQQUPSIUPSOKSÖÖPVBPYKJBJIPJIUSIUPVBPORUKUNÖRÖPPIJÖUSÖÖPTORROUPSÖJIORUORRIJJÖPWYLUPKIOKUJIUQNUÖOKJOKNÖUSSOTÖSÖINÖPSBEPJUOPJOZYRRÖHURSÖKJIPIJQYRSOUKYKJUQUYKKÖPOUNOTÖRRYÖKUÖSSÖÖPNOUKJIJJIÖQUPIRRÖQYPYYNÖRTOPNÖLYQQUPTÖKUPBHOUJOKJÖÖSOVJÖRÖQNÖÖKUQUSKUNEEJBUKUJYRBQBRJBYPYQQBPKUSKUYJJBTOSÖUKYPOPKYILÖJJÖHÖYPPIKQYLSSYTBNOUSÖKÖPOUJÖVJOQÖJJÖÖPTÖSÖJIUVYJUKÖPOTÖÖPKURRBSÖINNUÖKYUORRIJJÖHÖPPIJSOKSÖÖPSIPUPWÖKJÖKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUSOKSÖYRBQBVÖRIÖÖYJJBTOSÖUPYPKYILÖÖOQÖÖJUYJBBPHÖPVÖSIPUPWÖKORUKÖPOPIJSÖINNUÖKEQQBLKUSIUJYPSUPQUKJBNOUSÖNIVIUNOTÖPNYRSSBRBKPBOROORUORRIJVEHBYPPYTÖSIPÖUSÖSIRIUTÖLÖVÖÖÖRSOUHULLÖJÖSÖKKÖÖPVBPYRRBYUORRIJQUJBBPKEEJBSÖJIÖYJJBORUOJJÖPIJYKNÖPTÖRÖUKYPNÖRHYRISKYYPKÖNOUSÖÖPKÖUJKUYVSBYPYQQBPSIUPORUKUSIIRIPIJQIJJÖSOKSÖVBPYUORRIJIKSOPIJQEEPPUPKYPSIQQYQQUPSÖKHÖHÖPVBPORUJÖLTOPPIJNOTÖRRYNÖLYQQÖPQEEPJUNÖRSSUOPVBPORUÖTÖJYRRIJYJJBNOUSÖNÖRÖUKUNUÖPRÖQNÖUJJYPKÖRIOQUSKUVÖRIKUJNBBKJBNELÖQUZYURRYVBPSEKEUKUULJBBSKYYPSYKSIKJYRIPYKUJJYRENAEZUKJBKUSKUYJJBORYPSIIRRIJPUUKJBUSBPUNOUSÖHÖKJÖKUSYLJOQÖJJÖIPYKJÖÖPÖÖLLYORUPEJNYRSSBJIKSÖRRUPYPQIUKJOYUSBVBPVÖRIPPIJÖTÖJYRRÖSOSOÖKUÖÖYPJIPPYSYJBBPTOSÖVÖRIÖUKUSIRSYÖÖÖHUSOPNOUSSUNELÖQUZUYPHIOSKUSÖINNUÖKKÖPOUPYVBPOHÖJNYRSSBSÖKÖSUHUBHOUKUJNEKJEJJBBKYRRÖUKYPOQÖRRYJÖSÖNUVÖRRYKUJYYJJYORYVÖÖHYURRIJSOKSÖÖPNBBKYHBPPYQÖÖURQÖRRYNOUSÖHÖKJÖKUTÖRBVJUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖORUÖKJIPIJRUUSSYYKYYPSÖSKUNBUHBBQEAVYQQUPSÖINNUÖKJIRUNIVIQÖÖPNOTÖRRYQEEPJUNAEZBKJBYPNUZBQIIJOSKUKJÖVBPKÖPOUKUPBTÖQUPBYQQYORYSIUPVÖKKÖPLUSÖKSÖINNUÖKVBPJBYUVBJSBVZEJBNÖRTOÖSÖÖPHÖUSSÖJYSUKUHBBLBPKUTOUJISKYPQIJJÖQYUZBPSÖVZYPOPQÖSKYJJÖHÖHULVYUKJBQQYKYÖUPÖSUPNUJBBNÖUSSÖPKÖNOUSÖÖTÖJJYRUQUPSBHIOSKUVÖRIÖJNEKJEJJBBNAEZBPSÖINNUÖKSEKEUVÖRIÖPNBBKJBNUÖPRÖQNÖUJJYPURIOQYUZBPOPJOUQUJJÖHÖPEJSIPOPPUOPNIORYRRÖQQYTÖÖIJYJJÖHÖKUJBEVJBNÖRTOPSIUPKYÖIJJÖÖQYUJBKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUHÖPVÖSÖINNUÖKORUVYJSYPBBPYJUTÖKÖPOUHUUQYUPNLOXYYJJÖÖPJOUQYURRYSOLÖÖPUPTÖTBJJUHUUKUOVTYPIOLÖÖTOUJÖPOIZÖJJÖÖYRBQBQQYÖUSÖPÖJBLSYUPOPKYYJJBOPIKSOJJÖHÖEVJYYPÖUPOÖÖPTIQÖRÖÖPKYPRUKBSKUQYUZBPOPLISOURJÖHÖHUUKUSYLJÖÖNBUHBKKBNÖÖKJOJJÖHÖLÖQÖZÖPSIIPÖUSÖPÖTÖÖPPYJJÖHÖÖRQITÖSAEVURRYVBPHÖUSYPUVBPYPKURQBPKBJBEJJEUHBJSEEPYRUKJBVBPYPNIVIYKKÖÖPNLOXYYJÖKJÖVBPORUVILKSÖKQUYKTOSÖELUJJUSUUHÖÖKJÖRIOPJYYKJÖÖPVIORUQÖJJÖYRBBUKRÖQUPONNUYPQISÖÖPQUSBKYHUUZYKOVTYPIOLÖOPNOUSÖSEKEUKÖPOUJNÖLUNBUHBBKUJJYPYJJYPORYIPYRQOUPIJSOKSÖÖPQÖJSIKJÖQUKYKJÖSÖINNUÖKHÖKJÖKUTOSÖUKYPQIKRUQUPHUUZYKHYRHORRUKIIKOPNEVUUPHÖYRRIKQÖJSÖQYUZBPOPSBEJBHBÖUPÖSUPSYLLÖPYRBQBQQYÖUSÖPÖQYSÖKKÖNEVBKKBSÖINIPWUKKÖQYSSÖOPNÖRTOPSÖIYQNÖPÖSIUPNELÖQUZUJPIOLYPÖNBBJUPSBEJJBBHBVBJLÖVÖPUSÖINNÖPUNYLIKJÖQUKYYPÖTÖJJYRUPORYHÖPUTOPÖUPNBUHBPBPUUPLUSÖKYJJBHOUKUPRBVJYBQYSSÖÖPÖROUPHÖILÖKJIÖQIJJYPHOUPIJTBJJBBJBJBSÖUSSYÖSYPYPSBBPHÖKJIIRRYKURRBSLUKJÖRRUJOHÖJVÖILÖUJÖYKUPYUJBKÖQÖÖPÖUSÖÖPSÖJKYRUPSIUPSÖUVQUKYJHÖYRKUHÖJSÖINNÖPUOVUSOVJUQYSSÖÖQIIJÖQÖJNEVUUPHÖYRJÖTÖJORUHÖJPUUPLUSSÖUJÖYJJBVYURRBORUOQÖNÖRHYRUTOUZYPTÖSÖQYRUYPKÖÖJJIYQIJJÖIKYUQQÖJVYUKJBORUHÖJSAEVYQNUBSIUPQUPBSÖUSSURBVJUHBJNÖRÖKUHÖJJEEJEHBUKUPBTÖLUNIKJUHÖJNEVUUPHÖYRRIKQÖJSÖPKEQÄORUJNOLJJUPKÖNUYRYYPYLBKKIIJÖLUSYLJOUSIRSYPYYPKÖQYRSYUPHIOZYPÖÖHUSOPNOUSSUQIJJÖKÖPOUHBKEHBPKBNÖRTOPYPYQQBPSIPVBPYPORURBVZYJJBHBJÖPWYLUKKÖNÖLUPSOLJJYRUPNBBVBPOKJÖQÖÖPPÖVSÖÖQUSKYJJYRBVZYQYSSÖÖPPEJNOUSÖSEKEUKUSKUYJJBÖTÖJIKQYSÖKJÖNUJBBQUPIJYROKKÖKYKÖÖQUPIJSYKJBQBBPESKUJOUSSOUKYJNBUHBJPBUZYPVERRETYPQESBJSLUKJÖRRUJTÖJIOPSÖVHURÖPVULHUJJBHBJLIOÖJNYRSBBPJOJYIJJÖÖIPYRQÖÖPUSOKSÖKYPTBRSYYPQUPIRRÖYUORUKUQUJBBPKEEJBYRBBKUPBIPYRQOUJRÖQNÖUKJÖTÖNELÖQUZYUKJÖKUPBORYJYLURÖUPYPSIUPQUPBKURRBKUPBVÖRIÖJJOJYIJJÖÖIPYRQÖKUQUPBVÖRIÖPHÖUPVÖÖHYURRÖQYSÖKJÖORYPSIHUJYRRIJJIVÖPKUÖSYLJOTÖSIUPSÖSIRTYPÖÖHUSOPNOUSSUKÖÖHIPÖISUORRYTÖSUYLLBPNÖSORRUKYJKYUJKYQBPSYLJÖÖNEVBPSUHYPYPPYPSIUPSOKSYJÖPKUJBSIHUJJYRYPSYUJBOPHUYLYRRBPUTÖYZYKKBPUQUKJBSYKSIKJYRYQQYTÖQUJSBLISOISKYJLISOURYQQYEVZYKKBQIJJÖNYRSBBPNYJJEHBPUTÖJEEZEPKYPHIOSKUIPYRQOUQÖÖPKUPBNBUHBPBSÖINNUÖKÖPJOUNOTÖRRYRIHÖPNEKJEJJBBQEEPJUNAEZBPSÖUSSUYUHBJHOUJOJYIJJÖÖIPYRQUÖÖPKÖQÖRRÖJÖHÖRRÖRBVZYNÖIROÅOYRVOÖRSYQUKJUÖRSINYLBUKJYOKOPTIRSÖUKJIHIOPPÖTIRSÖUKJIKIOQYPPOKKÖPPÖNYLPILOQÖÖPUSÖJSYRQÖPVYPSURAVÖVQOJÖLOQÖÖPUSÖJSYRQÖNÖIROÅOYRVOÖRSYQUKJUNOUSÖORUORRIJSLUKJÖRRUSÖINNUÖÖPNÖRHYRISKYKKÖQYRSYUPSIISÖIZYPHÖUSSÖJEAORUSÖUSSYÖQIIJÖSIUPUVÖPJYYRRUKJÖSÖINNUÖKQÖLQÖJJUJUKSUPKBJÖSÖPÖSÖUSYPNBUHBBSOQYPKUNOUSÖÖTÖHÖLOUJJUKBLSYQBKJBQUJBBPQIJJÖNOUSÖVÖRIKUNEKEBJEANÖUSÖKKÖÖPKURRBPÖRSIJJÖQUKYKJÖÖPVIORUQÖJJÖHÖPVÖSÖINNUÖKYUORRIJYNBOUSYIZYPQISÖUPYPVBPKÖUVEHBPNÖRSSUOPTOSÖUKYKJÖQEEQBKJBBPYKUPYYKJBTÖORUYVJUPEJKBBKJBBTOPSUPHYLLÖPLÖVÖÖKUPBÖÖQIPÖVBPORURÖKSYKSYRRIJYJJBTOKVBPJYSUKUJEAJBTOSÖNBUHBSIJYPORUJYVPEJKUUVYPSUPÖKJUVBPYPORUKUIILÖKJYJJÖHÖHIOKUYPPYPSIUPHOUKUOKJÖÖNÖLURÖQQÖKJÖVÖRIÖUKUPNEKJEJJBBQEEPJUNAEZBPSLUKJÖRRUYKUPYURRYNOUSÖKÖPOUSÖINNUÖÖRRYKYPHOUKUNÖPPÖIRSONIORYRRYPUUPYJJBKYVOISIJJYRUKUJBPPYHBSYBSISSIRÖPTIILYRJÖQUPIRRÖYUORYORRIJSOKSÖÖPKYRRÖUKJÖNAEJBBSÖINNUÖKHÖKJÖKUUVQUKYJJALQBBHBJKUUVYPTÖKBLSYHBJSLUKJÖRRUJSIPSIRTUPRÖUJIQYRRÖRÖQNÖUJJYPUSÖPKKÖHÖÖLÖPÖORUÖUPÖYJJBPUUZYPJUYRRYOKIUKUSBBLQYTÖYJJBPYSIORUKUHÖJQIJJÖKYRRÖUKJÖOPRÖQNÖUZYPTÖNÖUQYPYPYRBQBSÖINNUÖKSBBPJEUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖVÖRIKUSORQYSLUKJÖRRURÖKUÖVBPQEUPESEBBPNÖLYQQUPSIUPSOKSÖÖPVBPYKJBJIPJIUSIUPVBPORUKUNÖRÖPPIJÖUSÖÖPTORROUPSÖJIORUORRIJJÖPWYLUPKIOKUJIUQNUÖOKJOKNÖUSSOTÖSÖINÖPSBEPJUOPJOZYRRÖHURSÖKJIPIJQYRSOUKYKJUQUYKKÖPOUNOTÖRRYÖKUÖSSÖÖPNOUKJIJJIÖQUPIRRÖQYPYYNÖRTOPNÖLYQQUPTÖKUPBHOUJOKJÖÖSOVJÖRÖQNÖÖKUQUSKUNEEJBUKUJYRBQBRJBYPYQQBPKUSKUYJJBTOSÖUKYPOPKYILÖJJÖHÖYPPIKQYLSSYTBNOUSÖKÖPOUJÖVJOQÖJJÖÖPTÖSÖJIUVYJUKÖPOTÖÖPKURRBSÖINNUÖKYUORRIJJÖHÖPPIJSOKSÖÖPSIPUPWÖKJÖKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUSOKSÖYRBQBVÖRIÖÖYJJBTOSÖUPYPKYILÖÖOQÖÖJUYJBBPHÖPVÖSIPUPWÖKORUKÖPOPIJSÖINNUÖKEQQBLKUSIUJYPSUPQUKJBNOUSÖNIVIUNOTÖPNYRSSBRBKPBOROORUORRIJVEHBYPPYTÖSIPÖUSÖSIRIUTÖLÖVÖÖÖRSOUHULLÖJÖSÖKKÖÖPVBPYRRBYUORRIJQUJBBPKEEJBSÖJIÖYJJBORUOJJÖPIJYKNÖPTÖRÖUKYPNÖRHYRISKYYPKÖNOUSÖÖPKÖUJKUYVSBYPYQQBPSIUPORUKUSIIRIPIJQIJJÖSOKSÖVBPYUORRIJIKSOPIJQEEPPUPKYPSIQQYQQUPSÖKHÖHÖPVBPORUJÖLTOPPIJNOTÖRRYNÖLYQQÖPQEEPJUNÖRSSUOPVBPORUÖTÖJYRRIJYJJBNOUSÖNÖRÖUKUNUÖPRÖQNÖUJJYPKÖRIOQUSKUVÖRIKUJNBBKJBNELÖQUZYURRYVBPSEKEUKUULJBBSKYYPSYKSIKJYRIPYKUJJYRENAEZUKJBKUSKUYJJBORYPSIIRRIJPUUKJBUSBPUNOUSÖHÖKJÖKUSYLJOQÖJJÖIPYKJÖÖPÖÖLLYORUPEJNYRSSBJIKSÖRRUPYPQIUKJOYUSBVBPVÖRIPPIJÖTÖJYRRÖSOSOÖKUÖÖYPJIPPYSYJBBPTOSÖVÖRIÖUKUSIRSYÖÖÖHUSOPNOUSSUNELÖQUZUYPHIOSKUSÖINNUÖKKÖPOUPYVBPOHÖJNYRSSBSÖKÖSUHUBHOUKUJNEKJEJJBBKYRRÖUKYPOQÖRRYJÖSÖNUVÖRRYKUJYYJJYORYVÖÖHYURRIJSOKSÖÖPNBBKYHBPPYQÖÖURQÖRRYNOUSÖHÖKJÖKUTÖRBVJUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖORUÖKJIPIJRUUSSYYKYYPSÖSKUNBUHBBQEAVYQQUPSÖINNUÖKJIRUNIVIQÖÖPNOTÖRRYQEEPJUNAEZBKJBYPNUZBQIIJOSKUKJÖVBPKÖPOUKUPBTÖQUPBYQQYORYSIUPVÖKKÖPLUSÖKSÖINNUÖKVBPJBYUVBJSBVZEJBNÖRTOÖSÖÖPHÖUSSÖJYSUKUHBBLBPKUTOUJISKYPQIJJÖQYUZBPSÖVZYPOPQÖSKYJJÖHÖHULVYUKJBQQYKYÖUPÖSUPNUJBBNÖUSSÖPKÖNOUSÖÖTÖJJYRUQUPSBHIOSKUVÖRIÖJNEKJEJJBBNAEZBPSÖINNUÖKSEKEUVÖRIÖPNBBKJBNUÖPRÖQNÖUJJYPURIOQYUZBPOPJOUQUJJÖHÖPEJSIPOPPUOPNIORYRRÖQQYTÖÖIJYJJÖHÖKUJBEVJBNÖRTOPSIUPKYÖIJJÖÖQYUJBKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUHÖPVÖSÖINNUÖKORUVYJSYPBBPYJUTÖKÖPOUHUUQYUPNLOXYYJJÖÖPJOUQYURRYSOLÖÖPUPTÖTBJJUHUUKUOVTYPIOLÖÖTOUJÖPOIZÖJJÖÖYRBQBQQYÖUSÖPÖJBLSYUPOPKYYJJBOPIKSOJJÖHÖEVJYYPÖUPOÖÖPTIQÖRÖÖPKYPRUKBSKUQYUZBPOPLISOURJÖHÖHUUKUSYLJÖÖNBUHBKKBNÖÖKJOJJÖHÖLÖQÖZÖPSIIPÖUSÖPÖTÖÖPPYJJÖHÖÖRQITÖSAEVURRYVBPHÖUSYPUVBPYPKURQBPKBJBEJJEUHBJSEEPYRUKJBVBPYPNIVIYKKÖÖPNLOXYYJÖKJÖVBPORUVILKSÖKQUYKTOSÖELUJJUSUUHÖÖKJÖRIOPJYYKJÖÖPVIORUQÖJJÖYRBBUKRÖQUPONNUYPQISÖÖPQUSBKYHUUZYKOVTYPIOLÖOPNOUSÖSEKEUKÖPOUJNÖLUNBUHBBKUJJYPYJJYPORYIPYRQOUPIJSOKSÖÖPQÖJSIKJÖQUKYKJÖSÖINNUÖKHÖKJÖKUTOSÖUKYPQIKRUQUPHUUZYKHYRHORRUKIIKOPNEVUUPHÖYRRIKQÖJSÖQYUZBPOPSBEJBHBÖUPÖSUPSYLLÖPYRBQBQQYÖUSÖPÖQYSÖKKÖNEVBKKBSÖINIPWUKKÖQYSSÖOPNÖRTOPSÖIYQNÖPÖSIUPNELÖQUZUJPIOLYPÖNBBJUPSBEJJBBHBVBJLÖVÖPUSÖINNÖPUNYLIKJÖQUKYYPÖTÖJJYRUPORYHÖPUTOPÖUPNBUHBPBPUUPLUSÖKYJJBHOUKUPRBVJYBQYSSÖÖPÖROUPHÖILÖKJIÖQIJJYPHOUPIJTBJJBBJBJBSÖUSSYÖSYPYPSBBPHÖKJIIRRYKURRBSLUKJÖRRUJOHÖJVÖILÖUJÖYKUPYUJBKÖQÖÖPÖUSÖÖPSÖJKYRUPSIUPSÖUVQUKYJHÖYRKUHÖJSÖINNÖPUOVUSOVJUQYSSÖÖQIIJÖQÖJNEVUUPHÖYRJÖTÖJORUHÖJPUUPLUSSÖUJÖYJJBVYURRBORUOQÖNÖRHYRUTOUZYPTÖSÖQYRUYPKÖÖJJIYQIJJÖIKYUQQÖJVYUKJBORUHÖJSAEVYQNUBSIUPQUPBSÖUSSURBVJUHBJNÖRÖKUHÖJJEEJEHBUKUPBTÖLUNIKJUHÖJNEVUUPHÖYRRIKQÖJSÖPKEQÄORUJNOLJJUPKÖNUYRYYPYLBKKIIJÖLUSYLJOUSIRSYPYYPKÖQYRSYUPHIOZYPÖÖHUSOPNOUSSUQIJJÖKÖPOUHBKEHBPKBNÖRTOPYPYQQBPSIPVBPYPORURBVZYJJBHBJÖPWYLUKKÖNÖLUPSOLJJYRUPNBBVBPOKJÖQÖÖPPÖVSÖÖQUSKYJJYRBVZYQYSSÖÖPPEJNOUSÖSEKEUKUSKUYJJBÖTÖJIKQYSÖKJÖNUJBBQUPIJYROKKÖKYKÖÖQUPIJSYKJBQBBPESKUJOUSSOUKYJNBUHBJPBUZYPVERRETYPQESBJSLUKJÖRRUJTÖJIOPSÖVHURÖPVULHUJJBHBJLIOÖJNYRSBBPJOJYIJJÖÖIPYRQÖÖPUSOKSÖKYPTBRSYYPQUPIRRÖYUORUKUQUJBBPKEEJBYRBBKUPBIPYRQOUJRÖQNÖUKJÖTÖNELÖQUZYUKJÖKUPBORYJYLURÖUPYPSIUPQUPBKURRBKUPBVÖRIÖJJOJYIJJÖÖIPYRQÖKUQUPBVÖRIÖPHÖUPVÖÖHYURRÖQYSÖKJÖORYPSIHUJYRRIJJIVÖPKUÖSYLJOTÖSIUPSÖSIRTYPÖÖHUSOPNOUSSUKÖÖHIPÖISUORRYTÖSUYLLBPNÖSORRUKYJKYUJKYQBPSYLJÖÖNEVBPSUHYPYPPYPSIUPSOKSYJÖPKUJBSIHUJJYRYPSYUJBOPHUYLYRRBPUTÖYZYKKBPUQUKJBSYKSIKJYRYQQYTÖQUJSBLISOISKYJLISOURYQQYEVZYKKBQIJJÖNYRSBBPNYJJEHBPUTÖJEEZEPKYPHIOSKUIPYRQOUQÖÖPKUPBNBUHBPBSÖINNUÖKÖPJOUNOTÖRRYRIHÖPNEKJEJJBBQEEPJUNAEZBPSÖUSSUYUHBJHOUJOJYIJJÖÖIPYRQUÖÖPKÖQÖRRÖJÖHÖRRÖRBVZYNÖIROÅOYRVOÖRSYQUKJUÖRSINYLBUKJYOKOPTIRSÖUKJI"

def freq_testi_b():
    return "ÄIIÖZÅCZYZBJVHCRAZBVBDCÖZZHZÄÄCÅVBDIYVVBJICFCZGGRRÄRHÄVÖARVUIGÄIBBRBÖPYVHVÄVGÄIGHVÖIGHRHRIGHRRRZBVZGHCBRCBÄRHÄVÖARVUIGÄIBBRGGRDZUVHMBHPMGZGHIBBCBDQMHPÄZFÅRGHRHPMGZGHIBBCGGRÄPMHZZBÖPYVHVÄVGÄIGHVÖIÄRBGRÖRZGRÖCZHHVVGHRRÖCZHHVVBRÖÖVÄZFÅCZHHRBVVHÄRBGRÖRZGVHVGZHHZJPHVHHPJRÖHZCBAVHGZVBÄPMHHQQBÖZZHHMJPPÖRZBGPPUPBHQPAIIHVHRRBGZHVBVHHPJRÖHZCBCAZGHRAZÖÖRRÖIVZÖÖRVZGRZGZDPPGPPBHQZGVGHZHVYUPAVHGPÖRZGGRHRFÄCZHVHHIÅRIIUZGHIGYRÄÄIZHRÄPMHPBBQGGPAIIHCGHRFÄCZHHRZGZGZZFHMAZGHPRJCYRÄÄIZGHRÅRJCZARDVFPZGZGHPÄRGJRHIGYRÄÄIZGHRÅRHÄIJRDVZHHVZGVBAVHGPBÄRGJRHIÄGVBAVBVHVÖAZZBRZBVZGHCÄCCGHIIÖPYVHVÄVGÄIGHVÖIBÄRYUVGHRÄVGÄIGHVÖIBRÖCZHHRBVVGHRDIYVVBJICFCGHRVBGZAAPZGVBBZZGHPÄPMHHZJRGVAAZGHCÖZZHCBÄRBGRBVUIGHRÅRARZÄZJVÖPÅRHCZGVBGCGZRRÖZUVACÄFRRHHZVBÄRBGRBVUIGHRÅRDZFZHHRFRBHRBVBDIYVHHRÅCYHZDIYVAZVGARHHZJRBYRBVBDQMHPÄZFÅRBRGZRÄCYHRDHÄJDHPMGZGHIBHCHCFGHRZÄÖCÖRÄZRÖCZHVRJCYRÄÄIZUVBÖCDVHHRAZGVÄGZJRÖHZCBARZÖÖRÄRBGRÖRZGRÖCZHVÄRRJDÖPYVHVÄVGÄIGHVÖIDIYVAZVGARHHZJRBYRBVBÖPYVHVÄVGÄIGHVÖIRJRFHVBVGZHVÖÖPPBDPZJPÅPFÅVGHMÄGVBRGZRDIYVAZVGBVIJCGHCVYUCHHRRVHHPRGZRÖPYVHVHPPBARRÅRAVHGPHRÖCIGJRÖZCÄIBHRRBÖPYVHVÄVGÄIGHVÖIIBJRFRHRRBVBZBHPPBHIBHZRRGZRBÄPGZHHVÖMGGPBCIURHVHRRBRZÄRHRIÖIHVHHIÅVBRGZCZUVBCGRÖHRGCJZHHIÅRAVBVHHVÖMHRDCÅRARZÄZJVÖPJRGRFJCZGRDIYVAZVGAVHGPHCJRHAVZÖÖVHCUVÖÖRHPFÄVZHPBZZBZYAZGHVBÄIZBAIZUVBÄZBÖRÅZVBBPÄQÄIÖARGHRAVHGPHVZJPHCÖVJRZBDIIDVÖHCÅRHVCÖÖZGIIUVBFRRÄRRZBVVÄGZJRRBAVHGZÖÖPCBJRÖHRJRAVFÄZHMGCGRBRZÖARGHCDCÖZHZZÄÄRRÅRÖICBBCBACBZAICHCZGIIUVBMÖÖPDZHCRZÖARGHCBAIIHCÄGVBHCFÅIBBRGGRBVCJRHÄCFJRRARHHCARBHPFÄVPYZZÖZBZVÖIÅRYZZÖZJRFRGHCÖICBBCBACBZAICHCZGIIUVBBPÄQÄIÖARGHRBVCJRHÄCHZJRÖHRJRÖÖVAPPFPÖÖVÖRÅVÅRÅRGICAVBIYRBRÖRZGZGHRÖRÅVZGHRGIIFZBCGRRGIIÄZBAVHGZGGPMADPFZGHQRFJCÅVBÖZGPÄGZAVHGZÖÖPCBRFJCRBZZBJZFÄZGHMÄGVBARHÄRZÖIBÄIZBYRFFRGHIGHCZAZBBRBÄZBBPÄQÄIÖARGHRÖCDIÖHRÄMGVCBAMQGGZZHPVHHPAVHGZÖÖPCGRBRÖICBHCRCBZHGVZGRFJCBPAPAVHGZVBACBZBRZGVHRFJCHÄVFHCJRHGZZHPÄIZBÄRAVHGPHCJRHAVZÖÖVVÖZBVYHCYVBÄZFVZÄPÅRAMQGMÖDVMUVBRZYVAVZUPBDZHPZGZÄZBÖQMHPPMYPDRFVAAZBHRDCÅRAZHRHRAVHGZVBAIZHRÄZBRFJCÅRÄIZBDIIBHICHRBBCÖÖZGHRRFJCRBPZGHPVUVÖÖPARZBZHIZGHRGMZGHPCBHPFÄVPPVHHPAVHGZPAAVYCZUVHRRBYMJZBÅRJZZGRRGHZBMHAVCÖVAAVGRRBVVHHPBBVVUIGÄIBBRBÄPGZHHVÖMMBÄRBGRÖRZGRÖCZHHVVBÅCBÄRHRJCZHHVVBRCBGZZFHMPRJCYRÄÄIZGHRÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAPPBJRÖHZCBAVHGZGGPHPAPÄRBGRÖRZGRÖCZHVCBAZVÖVGHPBZHPFÄVPÅRYRÖIRBÄZZHHPPRÖCZHHVVBÖRRHZÅCZHRÅRÄRZÄÄZRRÖÖVÄZFÅCZHHRBVZHRJRÖHZCCBGICAVBGIIFZBAVHGPBCAZGHRÅRÅRJRÖHZCBARRHÄRHHRJRHBCZBBVÖÅPGCGRBGICAVBHICHHRJRGHRAVHGPARRGHRRJCYRÄÄIIGGRYRÄÄIIÄMDGPAVHGPÄRRUVHRRBAZÖHVZÄCÄCBRRBÅPÖÅVÖÖVÅPHVHPPBHRJRÖÖZGVGHZAIIHRARDIIACBZAICHCZGIIHHRHIFJRRARRBÅRAIZUVBHZÖRÖÖVZGHIHVHRRBHRZÄMÖJVHPPBIIGZHRZAZÄÄCÅRHÄIJRGGRÄRGJRHIÄGVGGRAVHGPPVZIIUZGHVHRÅRÄRGJRHVHRMYHVBPHRGRZÄPZGVBPDIIGIÄIDCÖJVBRJRRBAVHGZÄQZGGPCBACBVBZÄPZGZPDIZHRÅCZGHRDCZGHVHRRBCGRÄVFFRÖÖRRBRJCYRÄÄIIHRVZHVYUPJRRBAVHGPGPZÖMMRZBRVBVAAPBHRZJPYVAAPBDVZHHVZGVBPIIGZRHRZAZRVZÖPYHQÄCYHRZGVGHZZGHIHVHRJRRBAVHGPIIUZGHIIÖICBHRZGVGHZÅRHÄIJRGGRAVHGPBÄRGJRHIÄGVGGRYCZHCAVBVHVÖAPHÅCIGHRJRHAMQGHZÖRBHVVBÅRHRJCZHHVVBAIÄRRBAZÄGZÅRHÄIJRÄRGJRHIGGZHHVBCBYMJPRGZRVBGZBBPÄZBGVBRJIÖÖRJCZURRBHIFJRHRAVHGPÖICBBCBACBZAICHCZGIIHHRGVBRJIÖÖRJCZURRBVUZGHPPAVHGZVBJZFÄZGHMGÄPMHHQPDRFVAAZBÅRGVBRJIÖÖRJCZURRBAMQGHCFÅIRZÖARGHCBAIIHCGHRÅRHÄIJRÄRGJRHIGAMQGHIÄVVAVHGPHVCÖÖZGIIUVBÅRÖCGHIGRGHVVBBCGHRAZGHRGZÖÖPGVBRJIÖÖRARYUCÖÖZGZAARBACBZAVHGPBDIIGRRURRBÄRGJRHVHHIRRFJCÄÄRRÄGZHIÄÄZDIIÄGZJRGVAAZGHCÖZZHHCÄRBBRHHRRÅRHÄIJRRBÄRGJRHIÄGVVBGZZFHMAZGHPBZZGGPJRÖHZCBAVHGZGGPÅCZGGRGVCBARYUCÖÖZGHRÖPYHQÄCYHRZGVGHZAVZUPBHIÖZGZGZZFHMPÅRHÄIJRRBÄRGJRHIÄGVVBÅRVHVBÄZBBZZBHIÖZGZHVYUPHIFJVARRAVHGZGGPGICAVHGZGGPÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAPÖÖPJCZURRBÖZGPHPVÄCÖCXZGHRÄVGHPJMMHHPJCZURRBGICÅVÖÖRHIFJVARRBYZZÖZJRFRGHCRÅRJPYVBHPPGZZHPÖPYHVJZPYZZÖZUZCÄGZUZÅRHMDDZCÄGZUIIÖZDPPGHQÅPGRARBRZÄRZGVGHZÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAZPHIÖVVHIÄVRAMQGMÄGZHMZGAVHGZGGPAMQGYRÖÖZHIGCBGZHCIHIBIHAVHGZVBYCZUCBDRFRBHRAZGVVBGRZBZHGVYRÖÖZHIGBVIJCHHVÖIZGGRZGHIRGZZBPDQMUPGGPÅCGGRGCJZHHZZBIGVZGHRAVHGZVBÄPMHHQQBÖZZHHMJZGHPHCZAVBDZHVZGHPYRÖÖZHIGRZÄCCBMHDPZJZHHPPAVHGPYRÖÖZHIÄGVBCAZGHRÅRDCÖZZHHZGVHÖZBÅRIÄGVHGZHVBVHHPMYHVVBGCJZHVHRRBDRFVAAZBÄVGHPJPAVHGPHRÖCIGDIIBGRRHRJIIGÖICBBCBACBZAICHCZGIIGJZFÄZGHMGÄPMHHQZÖARGHCDCÖZHZZÄRBHRJCZHHVVHÅRARRBÄPMHQBVFZAICUCHYRÖÖZHIGCBÖZBÅRBBIHVHHPAVHGPYRÖÖZHIÄGVBJICHIZGVGGRHIÖCIHIGHRJCZHHVVGGRCHVHRRBBMÄMZGHPDRFVAAZBYICAZCCBJRZÄIHIÄGVHYZZÖZBZVÖIIBÅRÖICBBCBACBZAICHCZGIIHVVBAVHGPHRÖCIUVBÅRHVCÖÖZGIIUVBDIIBHRFDVVBFZBBRÖÖRAVHGPYRÖÖZHIÄGVÖÖVRGVHVHRRBBZVÖIHRJCZHVAMQGHRÖCIGAVHGZVBÖICBBCBYCZHCRVUZGHVHPPBÅRYRÖÖZHIGCBCYÅVÖARGGRRBGZHCIHIBIHGZZYVBVHHPAVHGPYRÖÖZHIÄGVBARZÖÖRVUZGHVHPPBÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAZPRFJCZGRDIYVAZVGGICARÖRZGVHÖRRÅRGHZVZJPHÄRBBRHRRJCYRÄÄIZHRAMQGAZBPCÖVBÄCÄVBIHGVBÄIZBÄRÖRDGIIUVBAQÄÄZARZGVARBZHIHHIAVHGPCBÄZBMYHPÄÄZPAIIHHIBIHRJCYRÄÄIIRIÄVRÄGZCÖVBBPYBMHGICAVGGRBZZBRJCYRÄÄIIRIÄVZHRÄIZBÅRHÄIJRBÄRGJRHIÄGVBYRÄÄIIÄCYHVZHRRJCYRÄÄIZGHRÖICDIAZBVBVZHZVHVBÄPPBHRFÄCZHRAVHGPHRÖCIUVBÖCDVHHRAZGHRÅRHPÖÖRZGHRVZÄIÄRRBCÖVVGZHHPBMHHPAPRÖCZHVÄIZHVBÄZBCGRÖHRRBÄVFHCCGZZHPVHHPZYAZGVHVZJPHCÖVHMMHMJPZGZPBMÄMZGVVBAVHGZVBYCZHCCBVZÖVBÅIÖÄRZGHIBMÖVBIIHZGVBAIÄRRBÖICBBCBJRFRÄVGÄIÄGVBÖRGÄVÖARHCGCZHHRJRHGICAVBAVHGZVBYZZÖZBZVÖIÅVBCÖVJRBJICBBRYICARHHRJRGHZRZÄRZGVAAZBCUCHVHHIRDZVBVADZPHPAPVBHZGVGHPPBÄCFCGHRRZÖARGHCJZZGRRBAVHGPDCÖZHZZÄRBHPFÄVMHHPJRÖHZCBAVHGPHCJRHAVZUPBÄRZÄÄZVBMYHVZGHPCARZGIIHHRCBHPFÄVPPVHHPHPHPÄRBGRÖÖZGCARZGIIHHRÄPMHVHPPBÄVGHPJPGHZAVHGZVBACBZBRZGVHMADPFZGHQÅRJZFÄZGHMGRFJCHYICAZCZUVBDIYVAZVGARHHZJRBYRBVBVUIGHRÅRFRBHRBVBAVZÖÖPCBHPYPBÄVGÄIGHVÖIIBDMMUVHHMVHIÄPHVVBCÖZÄCGVÄIIGZJRZGVZHGVAPBDIYVVBJICFCRBVÄPMHVHPPBVBBVBÄIZBUVSRHHZRÖCZHVHRRBDZFZHHRFRBHRBVBGURFJCZGRDIYVAZVGYMJPHÄIIÖZÅRHGRRAAVHPBPPBÄPGZHVÖHPJPÄGZRÖCZHHVVBÅCÖÖRHCUVÖÖRCBJRZÄIHIGHRHIÖVJRZGIIUVBAVHGPBYCZUCÖÖVÅRHVCÖÖZGIIHVAAVHIÖVJRZGIIUVBBPÄMAZÖÖVAVZUPBCBCÖHRJRYICÖZGGRAAVARRZÖARBÖRRÅIZGVGHRAVHGPÄRUCGHRÅRAVHGZVBHZÖRBYVZÄÄVBVAZGVGHPAVZUPBCBCÖHRJRYICÖZGGRAAVGZZHPÄIZBÄRAVHGZVBÄVGHPJPPBYCZHCCBÅRÄPMHHQQBÅRAVHGZVBGICÅVÖIIBÄZZBBZHVHPPBYICAZCHRBZZBGICAVGGRÄIZBARRZÖARBÖRRÅIZGVGHZGRACZBÖICBBCBACBZAICHCZGIIUVBHIFJRRAZGVBCBCÖHRJRÄVGÄZQGGPDPPHQÄGZPHVYUVGGPAAVGRARRBRZÄRRBAVZUPBCBCÖHRJRYICÖZGGRAAVAMQGAVHGPHVCÖÖZGIIHVAAVÄZÖDRZÖIÄMJMGHPÅRGVBMÖÖPDZHPAZGVGHPÅRDRFRBHRAZGVGHRRJCYRÄÄIZUVBÄZVÖHPAZBVBGICAVGGRVZÄIZHVBÄRRBCÖVFRHÄRZGIARRZÖARBÖRRÅIZGVVBAVHGPÄRHCCBÅRGICAVGGRAVZÖÖPVZCÖVGVÖÖRZGHRHZÖRBBVHHRVHHPRJCYRÄÄIZUVBÄZVÖHPAZBVBHPGGPRÖCZHHVVGGRVGZHVHMGGPAICUCGGRCÖZGZHRFDVVBAVZUPBAVHGPAAVÄRGJRJRHVBVAAPBÄIZBBZZHPÄPMHVHPPBCBAMQGYMJPMAAPFHPPHPGGPZÖARGHCÄVGÄIGHVÖIBZÖARDZZFZGGPVHHPJRZBÄRGJRJRHAVHGPHGZHCJRHZÖARÄVYPGHPYZZÖZUZCÄGZUZRYZZÖVBÄVFFMHHPAZBVBAVHGZZBCBBZGHIIJRZBYCZHRARÖÖRAVHGZPÅRYMJPGGPAVHGPHRÖCIUVGGRHIÖZGZGRÖÖZRGVÄPRJCYRÄÄIIHVHHPÅRHÄIJRÄRGJRHIGBZZBÄIZBBMHÄZBVFZÖRZGVHHRJRHAVHGZVBÄRGJRHIÄGVVBVFZDRZÄCZÖÖRDRZBCHHRJRHAVHGPHRÖCIUVBACBZAICHCZGIIHHRVIGGRAVHGPDZBHRRÖRCBÄRGJRBIHJZZAVJICGZÄMAAVBHVBRZÄRBRAIHHRAVHGPÄRHCÅRHÄIIARRZÖARÖÖRVFZHHPZBYICÖVGHIHHRJRRJRIYHZRGMZHPHPYPBAVHGPÄRHCCBARRZÖARÖÖRCJRHAIIBAIRGGRJPVGHQBÄRGJIÅRGZHPÄRIHHRFIIRBFVYIBDIIBÅRAIZUVBYMQUMÄÄVZUVBHRFJVAVHGPÄRHCRÖZGPPJZPGVZÄÄCÅRCJRHAMQGHZVUCBDIIHVYVZÄÄCYRÖÖZBHCÖRZHCBHCZAZBHRÅRARRHRÖCIHVVBÄPMHVHHPJZVBRÖIVZUVBÖRRÅVBVAZBVBÅRAVHGPDRÖCHARRZÖARÖÖRRFJCZGRDIYVAZVGAVHGPÄRUCBHCFÅIAZGVÄGZÅRÖICBBCBACBZAICHCZGIIUVBMÖÖPDZHPAZGVÄGZHRFJZHGVAAVÄIÖÖVÄZBARRÖÖVÅRARZUVBGZGPÖÖPVFZRÖIVZÖÖRMÄGZÖQÖÖZGZPHCZAZRÅRFRHÄRZGIÅRHRFJZHGVAAVÄIÖIHHRÅZVBHZVHCZGIIUVBÖZGPPAZGHPGZZHPAZGHPÄRIDRGGRCÖVJRHHICHHVVHCJRHHIÖÖVVHÄIZBÄRVVHHZGVGHZÅRVÄCÖCXZGVGHZBVCBHICHVHHIÅRAZBÄPÖRZBVBARRBÄPMHHQQBÄCYUZGHIJRÄIÖIHIGÅPÖÄZHICHHVZÖÖRCBVGZAVFÄZÄGZDRÖAIQÖÅMÖZYRGCZÅRÄRRÄRCÅRARZGGZCJRHGVÖÖRZGZRYMQUMÄÄVZHPÅCHÄRARRZÖARBÖRRÅIZGVGHZRZYVIHHRJRHAVHGPÄRHCRÄRBBIGHVHRRBZYAZGZPHVÄVAPPBJRÖZBHCÅRÅCHÄRVZJPHRZYVIHRAVHGPÄRHCRÅRÖICBBCBACBZAICHCZGIIUVBYVZÄÄVBVAZGHPAVHGPHJCZJRHÖICURAZÖÅCCBZRÄVGHPJZPÅRGCGZRRÖZGHRRGVARRDRFRBHRJZRHMQDRZÄÄCÅRMADPFZARRZÖARRHVYUPPBHPPÖÖPGICAVGGRGVÖÖRZGHRDCÖZHZZÄÄRRÅCÄRCBVBBRÄCZHRJRRÅRDZHÄPÅPBHVZGHPRÖCZHHVVGGRRJCYRÄÄIIÄZVÖHCÄCGÄZGZJRÖHZCBCAZGHRAZRARZHRHPGGPCBMAAPFFVHHPJPAZBÄPÖRZGZRRÖIVVÖÖZGZRJRZÄIHIÄGZRRÖCZHHVVBJCZARRBHIÖCRZYVIHHRZGZJRÖHZCBCAZGHRAZGHRAVHGPARZGHRGIIFZBCGRGZÅRZHGVVDCYÅCZGÅRZHPGICAVGGRDPPHQGRZYVIHHRZGZGIIFHRRÖIVVÖÖZGHRVDPCZÄVIUVBAIÄRZGIIHHRÅRRJCYRÄÄIIÄZVÖÖCÖÖRCÖZGZAVFÄZHHPJZPDRZÄRÖÖZGZRJRZÄIHIÄGZRRGZRRÄCÄCBRZGIIHVBRHRFÄRGHVÖHRVGGRCBAMQGYICARHHRJRVHHPJICGZHHRZBVBDPPHVYRÄÄIIÅRIIUZGHRAZGRÖRCBMYUVBDFCGVBHZBAVHGPDZBHRRÖRGHRAAVGZZGMÄGZDFCGVBHHZÄCÄCARRAAVAVHGPDZBHRRÖRGHRGRARRBRZÄRRBDFCGVBHHZRAVHGZGHPAAVCBHPMGZBGICÅVÖHIHRZFRÅCZHVHIGGRÄPMHQGGPHPGHPZGCCGIIGCBHZIÄRGHZGICÅVÖHIRÅRBPZUVBGICAVGGRHZIÄRGHZGICÅVÖHIÅVBAVHGZVBCGIIGÄCÄCVIBGICÅVÖÖIZGHRAVHGZGHPCBDICÖVHGZZGDICÖVHÄCÄCVIBRÖIVVÖÖRGICÅVÖÖIZGHRAVHGZGHPGZÅRZHGVVGICAVGGRMÖDVPBPJCZAAVAMQGÄVFHCRVHHPMÖZDFCGVBHHZRHRÖCIGAVHGZGHPAAVCBGVFHZWZCZHIÅRMÖDVPBPJCZAAVAMQGHCUVHRVHHPAVZÖÖPCBYMJPÅRHCZAZJRAVHGPÖRÄZBMHHZVUPBVHHPAVHGPGVÄHCFZBHCZAZÅRHCHHRJRHJRÄRJRGHZYICAZCCBÖICBBCBACBZAICHCZGIIUVBÅRZÖARGHCCBÖZZHHMJPHÄMGMAMÄGVHÅRCJRHRZUCGHZCÖÖVVHAIÄRBRHPGGPHMQGGPÅCJICGZRÖICBBCBACBZAICHCZGIIUVGHRYICÖVYHZAZBVBÅRÖRRÅRDCYÅRZBVBMYHVZGHMQCBVFZHHPZBHPFÄVPPAVZUPBÄRZÄÄZVBHRJCZHHVVBRHIÖVVCÖÖRAVHGPÖRÅZVBIYRBRÖRZGIIGÄVYZHMÄGVBDMGPMHHPAZBVBÅRÄCFÅRRAZBVBÅRGZHPHMQHPCBHVYHPJPÖRRÅRGHZMYHVZGHMQGGPVFZHCZAZÅCZUVBÄRBGGRAVZUPBHVÄVAZVBDPPHQGHVBCBDVFIGHIHHRJRHIHÄZHHIIBHZVHCCBVZHIBHVVGVVBGZZHPGMMGHPCÖVBÄZBZÖCZBVBVHHPAVHGPYRÖÖZHIGCBHPBPGMÄGMBPZÖACZHHRBIHDVFIGHRJRBGRÅRHÄIJRBÄRGJRHIÄGVBRÖIVZHRVFZDICÖZÖÖVGICAVRÅCHHRGRRAAVHIHÄZHHIIBHZVHCCBDVFIGHIJRRÖICHVHHRJRRÅRÄPMHPBBQGGPHVGHRHHIRHZVHCRÅCHRÄPMHVHPPBAIIBAIRGGRHIÖVJRZGIIUVBFRHÄRZGIÅRHVYUVGGPAAVÅRRBBVHRRBAVHGPBÄRGJRHIÄGVÖÖVÄZBHRJCZHHVZHRVZFRÅRRJZRÄVZBCÅRÅCHÄRJCZJRHCÖÖRJRYZBXCÖÖZGZRÖPYUVVUIGÄIBBRBHPMGZGHIBBCBDQMHPÄZFÅRYHHDGKKKVUIGÄIBHRWZWZJRGÄZDCMHRÄZFÅRRGZRÄCYHRGZJIHDHÄRGDLJZZHRHHIAICÄÄRIGMHÖÄIIÖZÅCZYZBJVHCRAZBVBDCÖZZHZÄÄCÅVBDIYVVBJICFCZGGRRÄRHÄVÖARVUIGÄIBBRBÖPYVHVÄVGÄIGHVÖIGHRHRIGHRRRZBVZGHCBRCBÄRHÄVÖARVUIGÄIBBRGGRDZUVHMBHPMGZGHIBBCBDQMHPÄZFÅRGHRHPMGZGHIBBCGGRÄPMHZZBÖPYVHVÄVGÄIGHVÖIÄRBGRÖRZGRÖCZHHVVGHRRÖCZHHVVBRÖÖVÄZFÅCZHHRBVVHÄRBGRÖRZGVHVGZHHZJPHVHHPJRÖHZCBAVHGZVBÄPMHHQQBÖZZHHMJPPÖRZBGPPUPBHQPAIIHVHRRBGZHVBVHHPJRÖHZCBCAZGHRAZÖÖRRÖIVZÖÖRVZGRZGZDPPGPPBHQZGVGHZHVYUPAVHGPÖRZGGRHRFÄCZHVHHIÅRIIUZGHIGYRÄÄIZHRÄPMHPBBQGGPAIIHCGHRFÄCZHHRZGZGZZFHMAZGHPRJCYRÄÄIZGHRÅRJCZARDVFPZGZGHPÄRGJRHIGYRÄÄIZGHRÅRHÄIJRDVZHHVZGVBAVHGPBÄRGJRHIÄGVBAVBVHVÖAZZBRZBVZGHCÄCCGHIIÖPYVHVÄVGÄIGHVÖIBÄRYUVGHRÄVGÄ"

def freq_testi_c():
    return "ASJMYRÖPEHAXFHAUSPIQFKQÄÖQLJWQÄXINQYQAITUCLÄLHTKZKPCBÄUVVÅSCHÄJZÄASGRBPTAKUCHCBVWÅKCLÄKPSDGÅPQXÅÄJTTDVÄIGKÄXPVYJLTEEDLPZRRYMTENPZRÅÄÖÖKZWRUDAFÄHTKÖLHCYMTIDUÅMDÄÖWYHDQGFÖQDCDBOYZÄYIYYTVKOWÄAPQYZKQXGXSZCLZÖYZYÄKIZUKTEPHHTGLUNRWTZPÄESLRMOMRIPMFPÄEHZRRBÅXQOMLWYÅFVPUYQTZZULIBCJPQVÖQTZLAZZXLVTÄBRIÄILUÖCBJVSGXMMZOOMDWXQRTKRAIQZJTDIHDCÅÖCWTKDBQDPINCYRVÖWIÅPAZRXKRUERDÅGCSGDPXJZNÖVBDJXWÅZVRIBHQSWITWLVFEJQÖÄRGÅMRXYQNCHJUZKPAÄKHASVTXLZMMHMWRBQHJLXPFHPGWÖZIÅMDIDGVÄPCÅISRAÄZVIIRWCBTNUJMWDPYÅFOCFÖIXENPNCHJUZKPAÄKHASVTXLZPQYZKQXGNUVÅCFYÄFOMZJLJZXOBVYGDÖIQJTSZRTRHTZGBMXIVIHJSPUHKVÖSGDÅTVGXPRZÖRVWSJDSVRTJVYLRAJKJLTEYHÄFTCULVNXÖZDEDBGSÄXPVMTÖIFXXPRZCBÅTGJAQVPBÄWPLÖJVJTÖMKXLPIÅMFPNZXÖÅGQBGGÅÄBÅFKLPVZQTLXHTGLUNRWTZPÄESLRMOMRIPÅLÖHTZSIRTLXEBÄKILCBLKRYOYEXÅCEIWBHQDINXÄLÄNOTLRSCFPVRÄRÄDEZCBVKHPTKLTÅASDQCJFFLLOEDMJOIÄAOCHPVHTÖÄÖIHPRYLRQQTDAQYEZNOKCBWQYJLVNMBIVÅZFQHXQWLJEJPVKÄBOFLSÖWJHDGBNCBCÄLEÖUVHXQOYICYÅZTBMJEWCÅFKGBGRBOPZXIMAISUAUGDYMFEJRAPLZAÄKHTMJRTFRYCBASBBOQÄLXRRÅRWÖGSÖLRTQIRPSJUSMZENPVXJQÄCJUTONXBMFFEPULRRAQHXLSLEDBVTÅÅWQMÅPÄZRTRHÅÄAPLSEBÅNEHÄBKCULUSRAÄZVIIRWNOWQYJLVYMIIIÅCFLLKIXMFEHÖVÅQXÖÖVFPVCSCBOMPRXÄOBWILXXLUHQHSMXHXGKXXPGRÄDPVÄRNSZVJGÖSPPNSRÄRÄKXEPHPLHÖMYIPNUVTRHWJRBÅGFITAWJÄBKCBXIXITFJJOJÖLPWKZUHOVARZCBEPIYLKHOMSVXLYHPHDAGDZZFERLUYÄHAZGWTSVPJMTOBRXQJHZÄLIDQGÅZÖWVODRGJIDÄBUÄBJVÄTOLZRLÄFKYWKZUHOVARZCBÅPPOLKÄVZVJJDCÅÖCWTYLXNUVWÄALPWKZXTAWEQTPVUTRÖMTXYWJQJGHÅÄFAÖIVJAZREKWPLÖLVJIOIEPTLUZJRRÄBLJZJMDRVRTRWQLÄNMJEWCGPEHTTRWPVLYHLVYGBRMTYTVDEDBGKÄAWITWATVKÅÄFFLUISÄTWQÅMVCFHRGTOZHPOSRZCFÅGUTOGHPWXLAMATCFQHXÅZXHRÄLXZTZAÅTTÖÄÄDHÄULRZRMTZJTDEDBVKÄAWMPEYMFMÄQYVAÄPDYFPTVHXJRNCHZUMKWLZXÄQVUÄGBMOISWXOXWJTMTSAGHOMLJSPGÅÄÖLVJIWIÄIJSHHLWKZQTYIYEEAYÄQRAWSBGKCEWCGIPMBIJXYVGVWÄALPZVITIVIYSCGBHLGPVODZUECIRVYQÄLXKJUIÄCHQPRCFÅFGJBLVQBCÅVLVYSUCXMJJQCBUWTSITILÄLWFCÖHMARÖRWPÄGGÅBOFPUPÄÄÄVÄAKJÄHÅQRXÄRÄRIÅMDJPUBRÖMUVVÅSLTPAGHÖTONXBILXICAHRTSMTBTSKSCÅJYGXLUGJNPZVÄLCTKPAÄKHASVTXLCJFGZURTYLKPTEVUQDPTGHLAYIDÄBSCUYQTZPVWSHBVMÅFZZJDTVÄIDQBHPRAÄÅFÅLVXXPRZRZWTGJBRTQIRPSJROISENPÖIHPZKPCBÄYQLÄLEBJRMGBWGTWLZZLTPGHKALUFÖWQÄLXRRÅRWKTPTMFYIWÄAVAYSMXHTLJSJRZKCGBWXTXGKXXPGRÄDPVQBJUEIWFPUTZAVODRÄAPBGFPIGOIMXYÅVVUCHZMFOVODRÅLCBJVYHRRNFBUIFHXQDGPGXFRJTTDHXLAPLZAÄKHAWEWTIVUEPWTKHKAZVLZXLPFPOKHTVÄIDÄHÅSDÅLGJPZVJSPCYBBTVMXYÅSEJRÖHEVYWSJPTZZÄQZVLGZKNHLLASLCFRQRXPKJZKCWQERYÄBBMXTÖÅVQCÄAGHÖTONXBILXYÅÖQÄULUOWÖWLXEAYMGBWITWALVQBÄBKQÖLOOWPÅLSHÄAFQHPZYALXZRFYGHKALÅEJBÅGQÄBRNPVOITZLZVRJCFHQWKZNXÖZVVDÄGTMHAAGHTOÖIJFVSQZYOLEÖÅEEJQÖGDGBZFCAAKOHGWÅJZRÄYFKZKQQJGZPUASXÄQÄDMZRGWÅFAUDBZUVXJBRTGUÖWZJZKCWQZFHTGLUNRWTZPÄESLRMOMRIPUVXIJQMQHÖHSIDÄAPBPZRQULOKDAÄVPCÄBUZGBITXYWXLXLYHJJXQRÖZVKBZBRTJVUWTXYÅNQYGBHJDIÄÄÄLXJMBZBKYFJSTTANARIIUHKZAPUVVMQTQTAUGJIQTJPÅGQINCYRRDÅGCSGDPXJZNÖVBDJXWÅZIDJZNRGBIZIÖFYIJQWGPCÖLTÄYOGQJCÖLTZAMXÄYOVZXTVUCALVMTDÅVQÅZÖSCÖTOHXBDYIBQVZÄAXIYTVOTPBCFMMHMWRBPVLMBJGWMFBMXENPZZXLVTÄBRIÄILUÖCBJVSGXMMZOOMDWXPPRLRAJRTYLVRDÄHZJIBÅVXWMFMLZFSBGXGYJPZKOTNVUGWZÄHEWTÅDHFVYPRÖÅRKBÅHIBCBPCIÖWVTXGKXXPGRÄDPVOYZÄWSBJWGPYPZXTÖWXLLZFSBGXGYJPZKOTNVUGZAPUVVMQJSPYLPFLZJXBÄVFXRMKCFTXXTVÄAOXLRÅRAJÅZXÖÅCEFDQYBRXMXALVHPTAVYÄGMIQEXÄNOTLRSCFYIYUPÄVPCSFHPAPLGDSMJVBÄBKQÖLOKDRIJEDRVYÄGPVVBLÄKMTJÖHDZYTEDOIJIIRJYSHZZKYBMJWEKÖPQHLVVQPAZRXKRUERDÅGCSGDPXJZNÖVBDJXWÅZWJWFÖGÖVIOWÖWLXICJLLVXITZAWEWAÄGCLRAXDYÖQVXLIRUÄÖPZKDWQÄXBÄXLLCXÄKBPAAWÄMBZMTSZGWTWNIHIGHKYPÄKDMIJXÅCFYÄFYILÄYVKMWÄXWYUPVRÄAÄVRLGÖRCHJZLSÖFDHHÄHYCULVJQQHJSHBBPLXPVÅJQWJQTBVZYFVWTIBILIHÄULHPXÅZRWTYLXRGVKSCLYCLVFIDÄHÅKZYQYJPZAIHLROÄFPVYAGTYMZFVÅÄHBNXRXRVNRKGÅZÖWLNXBWXLTRHZIMWLOZSMLIDÖCYBVBIYÄMMVOJÄBKCAKRRÄRPZXXLRÅRHLUKWXWLWLÄFHLUPLGCXGKXXPGRÄDÅFRÄAÄVRWGGRSHPZGWPÅEIDÄFICHAOXKÅXZRAMAKYWÖISJTTDEJRVUBRAÄNXÖZECIRVYQÄLXKDDGXOXPHPJÖÖGIAWQÄXIRCYRZYÄXXAÅZJSPRÅRDWIZILXSPÄQHHLUPVSTÖÅABHDMSJVÖNFHZZYRÄLXLLOÖÖTWPZYIQPVUFRÖÄÄLLVGVDÄPUBFLÄYHLLAOTJHVAYOISÄOZGXJCBZQHJTRDTVÄCHCBHLBLVEDDIYHXLJHPUINFHZZYRÄLXLLHÖGJWPQCVTDHMMHMWRBAAEJSPUHKVÖNFHÖIKSCKRYCBDIXXYMFSHKHPRHLZYKNKTZXLCTDZYTGDOÅYECJRUBGWIMJGATVHGBÅCÄDIRÄQQXIHÄULQZRÄOBWLZRJSFUCFTVMXYNARBÄBKQULURTYLKPTEYHPPYLDADIDMYGTLPRBÅOZBZZKQLXLPHTLOZLZZSVFÄVKAPZLSÖPGTFLZUEGDQYIYIJXZÅFHBVBQMXYOTPBÄBKCULURXUWFIDGZZFCNSKOAXZPTBVSÄXPÄUCRÖDHXRZZCBLÅZXTÅÖSVIVCTAZKNLLZYIJDQYQHLTGDOÅDEZCHÄRRYNFHVIFEWÄCJFIAIYEXTQGAÄULQSÖDZTOMFREPUHKVÖQQTYÅCEWMAPLRYÅKDTVGQCZGÅCFASGFPÄBEZZFZZÄPZVQLÄLHTKÖLHCYMTAZUEIHDOLLBGKNTYÅVXJQDLJRZUMKWLZXEAYKYPÖLKJDQCXÄEHHRHAISJWQÄEYGBSZBOIXXZKCWQFRYKQUTOZSMLEJRGLKRBKNXYTAOIMAGTFTOGCLÄXLXPZUMAXGYJPZKOTNVUMTSÅUCWIFHIJRNCBAXKBLZVZWCBHLÖPLTÄYOZRUMFKCWKZUHOVARZCBZLRÖIYJCXHHTRVYÄGBQRBLÄLNRKGÅZÖWIJTXWXLÅCFYGUÖWZJAFVXJÄÖSÄWTVRRYLVVXFRYQRXUGCKRDMZFVÅÄHBNFBUIWBWCUHKCNPNXÖZAHHMHÅGUPÅZEÖIECIRVYQÄLXKDVTTQCCUOZBDQYDTVÄXÄJÖPPZVÅJTRMFWTPSLRGZZJDTVÄWJZÖSCFUIMYKTBEDBVZNQÖÅSQWÄAPBBVUKZYQYJPZKSCQRRCBRGRBPZUZXPJFEVÖZKZPZARZCBHRHCXVWLÄZVTDQYMFOVODRMFWQÄHÅJRRMTEXÄZPXTZZGCYÅUVSZVHÄMJLPÄAISÅPÄGGAQONÄFLVZXÖIJWTKAHKQUTOZSMLEJRWGJÅLLGCTLJSJRCJFWTVRTYLKHTKÖHLUATGZTLZWJMFHKPAÄKHASVTXLDEQRXUGIJÄLWEKZKÄXÖMJTYOVVTLHLPRANFHSMJVTPBHQAZÄYLLZAKÅCHOCÖAQTZQWJWCÄHZJQQÅZHKUKZIIFPDHWQMJAXUVIKOSQGÖLYAÖQÅXBGXÅQDKZYCITGQTRHKÄATLXEBÄGGAQOFPRDÅGCSGDPXJZNÖVBDJXWÅZQTRGSÅWAÄXSXÅNXÄJÖYGÄALGZPVKXTJAHLBJÅZTYMFSVFVUFRWASÄWRGRIYXKÄAWMPEYMFWLKWPLRWXDJDQVTHGÖFLUIZEAYIKJÄLGRBRXQYÅZKCIONOÖKBTADÄYÄZWEKGWMFBIÄILUÖCBJVSGXMMZOOMDWXCBSGXBÅZTBÅJBWCHZDQÖWXWYQFKEKHLJVDQYXÖQFKTTVÖCBPUGDRINWTKYFJÖPTOZMMLÖWCÖZCGLUSTAICKRJÖLPWZÄHEWTZRJGÖSQDZZZXÖWXLXTVUCALVMTDÅVQÅZÖSCÖTOHXBDYIBQVYZÄYIYUWIFHTLBHRGWÖZIÅMDIDGJFPÖOÅSRAÄZVIIRWCBTNUJMWDPYÅFOCFÖIXIWÖLWFCÖLLZPÖXEÅIECIRVYQÄLXKDTNGXUMÖSDQÖPKHÖIJSVFJFPÖOÅSRAÄZVIIRWCBTQYÅZKCIODQYFVÖZGHOMLXTÖVÅWUPZOFÖICXÄIVUÄHBUEIBMJWAÄDMÅFOISXÖSVRFJRJCFLÅHTVWEXLIRUÄÖPZTTAJZXTJAÄPRÖUKWLVÖIHPÖHLUATGZPVÄEHÄBÅCFLÅKDÅTVXIGRSJRQQTBJVYEHCGÅTFCÄUHPNLIHQCTJZAÄGDÅFZZXLVTÄBRIÄILUÖCBJVSGXMMZOOMDWXQHCPJTTQTTLJSJRGLTVYMSTYOKSCQÄHQMYIYFINJMTRJRÄBLTKHPVDMZRÖHEVYWSJPTZZÄQZVLGZKNHLLASLCFRQRXPKJPVWEHRYLPFLZTTQQFRIGUHEDILKDWQKXTLJPJÄPÄEHQHJBBBFHRFPLGDOFÅDHMFKLZYOKDCÄÅSHKRKCGIZQEYÅLEJCFHBVUGSIBGDPWFVÅQCXJÅWAUVRDCBHRHXQTÄAÄZVÄCFUÄYLZKDASQPWGXOCHLÄZYÖGENTHPTQHJTRWSMLSVFRÅRGVDRWTOÖIJCBIMFOMZTAQWITIHHLUPUFÖWQÄLXRVUÄHBÄGCPLESJQJHPRYLKWLUECIRVYQÄLXVQWQKXTLUPQÄCÄKHLLZWCCBHPSPÄYZÖÖHTXLÄVKUINXTXÄAPBÄHÅCBOIYJSMJVCZGÅCFASGFPVNCVIVYRZWTXRNSDMZRGÅMFBQTJÖMKWXDQYÄHBXRTBÅVTQJZZRRYLKDXIJWÄYFMWÖWMXYKZGVWLZUEVYFXKYLZVWCOYCBSIXJDAVREPBHZBOZGJAZVHÄIRSRCNPJTXQYVERHLLGAÄEBWVARZZFLLRYVGDJVNEWBVUTRÖLDYKZGVWLZUEVYÄXROLZMAPRMRWZÄHEWTKZCDQYBRXMXYKZJEIMATÄFPVÄTÖMFIDMFTRZBÄGHAÖXGRTVUMAQQTBLVYWWÄASÄBOÅRTRÄQZRPFPLHPSÄTWQÅMVCFHBVAQMJTTDHXLHÄPBPZODRMFJÄLÖHLUALGCWIFHIJRNFRÖGTWISNEBGWPAVÖIZITOLVXEOUEVÖÄOWTOVVXMTOICXUKHQHJLENDUGBRÅÄÄAÅFEHRXGPROMZÄRMFKRJÖHLUPLGCWMBSDCBPGGSWIAPDKTXJRKCÖLOKJZUÄYBBVÅGGPVGIBMAWÅMTRCMDUUVSAVVWCHMÅFAÄGBLVYWBÄXLRIBITYKZCEDÄUHMTSÖYTAWEPOAÄHBVAJXOBIYIDLCYBRXMXÄVIFWAÄUVKZYITIPVAREKAFQHPZYALXZXÖÄXFPGJSKHÅFVXJBRTJVUWTXYSGQCCFMYVYVBVSIFWTRHZNVWIUCRÖDHXRCJFUIGXWPÄNMARZNRRBÄYTXÄDMZÄWPLÖJVJTÖMGGAQOOÄFXHPBTOÖIJÄHÅQVXIZVSMFPÄIGVKQDZOZLUVXVFVYGBZUSRAÄZVIIRWCBZKNIZUDEDBGSÄXPVYFPTVVTTULLRYTKWYQFKXLSVPUPNFHZZYRÄLXLLGYIXTAÄMTFBRÅCFLÅZÄWTVXJHPTQHJTRTOIESVFYLPFTLXEBÄKBTRHHJÖLNODWGFHTPVOÄFAISCLUUNBGXOCHLÄZYKTBEUYULBRXWIÅSMJVÄBFVRHTLKIBWJECZGÅCFASGFPVCPRKALBYJVÄÄAVARZRZSJZÖQQIOIÄIDQRYÖVBÅUHOVARZQHFJÖPZPTRNUPÖÄBKCGÅHXIXFDXÄJÖKCBXQTÄAÄZVIMAZÄÄPVMRWTZVSTVYTPRMXHPOZVÄLXLLRBÄÅFÅLVXXPRMÅFZZJDTVÄIDQOHRHWIMXYWEXXJVÖGGTWTIZKÖVTBZVTVÖSYTXPZXEAÄZYXLZGDBMJEHQRTKRXHPBTOÖIJÄHÅDQWRGWLUAHHMHÅMTSNODWIFHIBRTJRYLYBLOAHXQHVPRXGYJPZKOTNVUNOAISCLÅTXJQCTGULOXXOIFKTPRURVÖIYYKZÖIHPRYLRAUUJAAVVÄEYLRYPTYÄYOÅSHQAHRGWHLIBZUQITGRPZQÄRÄRÄKTSPGTYÖAÅXWASJMYRÖPEHAXFHAUSPEKRÅRULUOWÖWLXEAÄZYPÖIÄILUÖCBJVSGXMMZOOMDWXKRÅQÖKNYJÖHEWLRZSJFTSYWLOZRIRRSKRYVEIBIFIDMTOCBSIRLXQDNELGEEULURXUWFIDQJTDZYIRFIÄNMTNFPJPYLDHJSFEIDZUQÄOISÄAPGGACMWYJXVOLIQFXXQCTQDZZZTDÅVQÅZÖSCÖTOHXBDYIBQVLLÖTOZIBILWHYULRGQHXEÖLFMDECTRVWMÄÄAMJMDERÖCJPVKCLVÄELQRTFPWTKBTOWIJWULJGPÅGCXIKEAEPSJVÖNUJMWDPXLHPJÖAXUHBMJSVFVÖCBPUGDRINWTKYFJÖPTOZMMLÖWCÖZCFJSTTAJDEDBRULRBÅRKBÅHIBCBPTPÖTJIXGKXXPGRÄDPVOYZÄWSBJWGPYPZXTÖÅDYJQDLJVYQKKÖWHECZGÅCFASGFPVAJERSVJÖQHXÅPZJEHMTOTPÖTJIXGKXXPGRÄDPVOÄAPGGACMMÅFSMXHLZYIJRRICHGLKHTXJEARZRCBLÄZCJÅLIHQÄHNWKZJTXMJOTLDSÄTPZGIMICSCRJRÄBLTKHYIKFXRRSKIÖIXCPLVRÅCFYJRYLYBLOZRZÄFHLHPZGIPVHPTRGPÄÖWILÄYTTRWÄFLQHDZÅJZZZJJCFZMAWQYJLVHBXTVUCALVMTDÅVQÅZÖSCÖTOHXBDYIBQVZRMÖAOBVIAHHMHÅQVDMTXXIFKIMAZIRADTTAXSJHGRÅTÄLVGBPZZRBGXÅJRRMTEXÄZPXTZZGCYÅUVSZVHÄMJLPÄAISÅPÄZRUÄFÅFVÖZGHYIÅMDLGPBRRXDWPVDMIRRUTZWSKJJZÅDHYÖKPRBZKWLVYBYÅFVPUYQTZPVMXYMFTÄUPÅDHVWFWJÄHLPROMPRXÅLCBJUOCHAWSUCLKQTLBLLRBÄSÄYQKXXPZLPBLPGHPVKOOJUPEYPÄGJBNJCCHRQZAAÄEBWLÖIJMTOÄHBÅQOWLAKÅCHLLSZZJXBIKMUCRRRRYLKCKRDMZFVÅCBLÄZJLUZHCMHZTRÖITWPLVQCZGÅCFASGFÅFDMIRRUBZASÅJPZVHXQALLRÖJKJAOJYFNVUICXLDYÖIEXÄJÖHRHPVJTAÄÖIHPAFQHPZYALXZRLZTRCFBQRBÖGXOBGXÅQHZZZÄYÄJIIQVMÅFLÄZFWILWTNOSGGBITWPVEEHQZEPWGTRXÖNUVEPUUGBRMTQÖÖFHXPULYFPVNTÖÄNZTLCYLRJVJHLÄKVTBZRÄÖBWIÅOIEMWPCÅRVYÅYJJTDRÄLXFPVYITDLVTRLÄUKCBDIXWINUVEPUUGBRMTJÖGYHXGÄYÄWBNUJMWDPITAMÅFOISXÖNUVHÄGVKALZKDDIJIDCBVPABQZJLZKYVAPÖCBZULÄYTVRWQUHKÖLVJIWIÄXOTPYPZYÄKADIDMYGTLPROMYÄRÄAPBBVURIÖVKHTVÄIDDZUJRYLYWLUDEDBGSÄXSIXRYLSOLÄÖPDZNMXTBÅAKJPVNYBRMXJTLAKTPVVAYVWSCPZÅDHFCWNBTVMIDQKWDÄFÅEQÖIJXBQÄIDEPSJRYLKWLUDIÖMBLLZTÅNENSZÖINVSÄUPTGZPÄGQZSÖKCHTÅKDLÅLIÄQYVAÄPDÄCZKÖZTPULRWKZYJLTVRWQÖHEVBÖZTYNUVAÄBHBRZKNKAIKSCJMJIROMYUÖDLEWCBUMFOISXÖQCEDQÄHBCXQTTYÅZRÄLCTKPAÄKHASVTXRÅHEPÖÅEAPZHBTRHKÄAWMPEYMFOEKALPWIMTDGKÖEDQRÅRGÅMRTZUÄYBBVÅMTSLDRÖLZXLGÄÅGXBIZJAIEXBGXHDZYTEDOIJIEAÄZYYLZSSUTAKÅCHHRHAMSTBKÖIDJZRQCXHÄHTOVQTRTOCFTVUCXGKXXPGRÄDPVUVSÅGQBÄBKQÖLOKDAXZPTPRÖBVYITBPLFMDEVUÖCÖLKYKZGVWLZUEVYÅTTÖIKXKNDKÄHPZGIBQDPTRHQZAAÄEBWIYECMTOFVÖZOWÖWLXIYRÅRRWTGYTVDCDBRYCYLZYTXUVQSHÖPEYPÄGJBNUPÖÄSEBVOISENPÖIHPZKPCBÄOWPÅLSHÄAFQHPZYALXZRAJPTKVOPEDDQKRÄLXÅGÖWQXÄVÅYEZCBZÄFMMZIZZYRÄLXZRPWTKHUIÄJSJÅHLUPÅVSÖÅEBBRZSJUPVSÄYQKXXPGVKGLSKDRGDPXPQÖCFDGMXÖZZKXPZUEVYIZJCXHHTRVYÄWKZUHOVARZCBZYRBÄRTRMFSCRVSCJTÅOEYÅGGÅPRKGCDMXAAIELXRCJIGIOGHLVLIHÄFZÄAXISSUTAKÅCHHRHQHRÖLLVQÄBFVRHZKNYTVDEDBGKÄAWITWATVKÄBVZRCÖISRAÄZVIIRWCBÅFYTXUVWRRHZMATLGZÖMYEDERYÄBBMXTANUVÅCFYÄFYIYCZÄKZTPZNFVBPKBAQFKYMFZKRBÅRSQÅLVSKGÖQÄÖQLJWQÄXINQYQAITYIÖLKOHGWÅJZRÄYFKZKQQJCTÄHBLGCTLJSJRCJIGIGXTDÅVQÅZÖSCÖTOHXBDYIBQVTÄHATFYAÄJDCQJÅGÖWZOAALVKXLGÅÄÖXITDJÅLEDCBVAYPVNTWAEMBHCUQORLGCWMBSDCBZTAQQTTWXSXLGRWPZWGTWIZTODÄGMGBASJTXQKLEAÄLWDIASDTASMDRVZMAAXUHBINWTKYFJÖPTOZMMLÖWCÖZCVYTOZBÅLEJQFEBVBÅLSÖWJHDGBNMABMRXDQKIHGBNÄJPAKDPUVRZÄJZÄASGRBPTAKUCHCBVWÅKILUEEIÄÄNZÖWMXYZÄWSBJVURZWTYFZZLIHMTOCJPVKCLVÄE"
