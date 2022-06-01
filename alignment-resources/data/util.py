
import subprocess
import os
import re

FILEPATH = os.path.dirname('')
RAW_PATH = os.path.join(FILEPATH, 'alignment-resources/raw')
PROC_PATH = os.path.join(FILEPATH, 'alignment-resources/process')
MAX_NUMERO = 999999999999

UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'kuatro',
    'sinko',
    'sesh',
    'siete',
    'ocho',
    'mueve'
)

DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)

DIEZ_DIEZ = (
    'cero',
    'diez',
    'veinte',
    'trenti',
    'cuarenta',
    'sinkuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)

CIENTOS = (
    '_',
    'sien',
    'doscientos',
    'trescientos',
    'cuatroscientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)

def num_let(numero):
    numero_entero = int(numero)
    letras_decimal = ''
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    if parte_decimal > 9:
        letras_decimal = 'punto %s' % num_let(parte_decimal)
    elif parte_decimal > 0:
        letras_decimal = 'punto cero %s' % num_let(parte_decimal)
    if (numero_entero <= 99):
        resultado = leer_decenas(numero_entero)
    elif (numero_entero <= 999):
        resultado = leer_centenas(numero_entero)
    elif (numero_entero <= 999999):
        resultado = leer_miles(numero_entero)
    elif (numero_entero <= 999999999):
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)
    resultado = resultado.replace('uno mil', 'un mil')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')
    if parte_decimal > 0:
        resultado = '%s %s' % (resultado, letras_decimal)
    return resultado
    
    
def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero <= 29:
        resultado = 'veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s i %s' % (resultado, UNIDADES[unidad])
    return resultado

def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if decena == 0 and centena == 1:
        resultado = 'cien'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            resultado = '%s %s' % (resultado, leer_decenas(decena))
    return resultado

def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if (millar == 1):
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = '%s mil' % resultado
    if centena > 0:
        resultado = '%s %s' % (resultado, leer_centenas(centena))
    return resultado

def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if (millon == 1):
        resultado = ' un millon '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = '%s millones' % resultado
    if (millar > 0) and (millar <= 999):
        resultado = '%s %s' % (resultado, leer_centenas(millar))
    elif (millar >= 1000) and (millar <= 999999):
        resultado = '%s %s' % (resultado, leer_miles(millar))
    return resultado

def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))
    
    
def normalizer(text):
    text = re.sub('\ufeff| {2,}|\t', ' ', text)
    text = re.sub('\n{2,}', '\n', text)
    text = re.sub('\w\w\d\d\d.+', '', text)
    text = text.replace("...",".")
    text = text.replace("- ","")
    text = text.replace("…",".")
    text = text.replace("’","'")
    text = text.replace("”",'"')
    text = text.replace("“",'"')
    text = text.replace("[","")
    text = text.replace("]","")
    text = text.replace("\n","")
    text = text.replace("_","")
    text = text.replace("..","")
    if text.find("BL0") != -1:
        text = text[:text.find("BV0")]
    text = " ".join(text.split())
    return text
    
    
def convert_doc(doc_file, out_dir, filename):
    args = ['soffice', '--headless', '--convert-to', 'txt', doc_file,'--outdir', out_dir]
    subprocess.call(args)
    pt = os.path.join(out_dir, filename+".txt")
    with open(pt) as conv_file, open(os.path.join(out_dir, filename+"_norm.txt"), 'w') as final_file:
        lines = conv_file.readlines()
        for line in lines:
            if line.strip() != "":
                line = normalizer(line)
                numbers = [int(s.replace(".","").replace(",","")) for s in line.split() if s.replace(".","").replace(",","").isdigit()]
                for number in numbers:
                    line = line.replace(str(number),(num_let(number)))
                final_file.write(line+"\n")
    os.remove(pt)


def get_processed_dirs(top_path, query):
    paths = os.listdir(top_path)
    dirs = []
    for path in paths:
        if os.path.isfile(os.path.join(top_path, path,'wav', path+query)):
            dirs.append(path)
    return dirs
    

def process(in_dir, out_dir):
    '''Create MFA compatible dir, convert the doc files and the wav files
    '''
    rel_in_dir = os.path.join(RAW_PATH, in_dir)
    print(rel_in_dir)
    rel_out_dir = os.path.join(PROC_PATH, out_dir)
    print(rel_out_dir)
    if not os.path.isdir(rel_out_dir):
        os.makedirs(rel_out_dir)
    doc_file, wav_file = get_doc_wav(rel_in_dir)
    print(doc_file)
    convert_doc(doc_file, rel_out_dir, out_dir)
    convert_wav(wav_file, rel_out_dir, out_dir+'.wav')
    
    
def convert(string):
    return string.replace(' ','_')


def get_doc_wav(path):
    for f in os.listdir(path):
        f_low = f
        f_path = os.path.join(path, f)
        if f_low.endswith('doc') or f_low.endswith('docx'):
            doc = f_path
        elif f_low.endswith('wav') or f_low.endswith('mp3'):
            wav = f_path
    return doc, wav
    

def convert_wav(wav_file, out_dir, filename):
    out_filepath = os.path.join(out_dir, filename)
    args = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic',\
            '-i', wav_file, '-ac', '1', '-ar', '16000', out_filepath]
    subprocess.call(args)
    
    
def text_wav_normalized(PATH):
    FILEPATH = os.path.dirname(PATH)
    raw_dirs = set([convert(d) for d in os.listdir(RAW_PATH)])
    raw_dirs_dict = {convert(d):d for d in os.listdir(RAW_PATH)}
    proc_dirs = get_processed_dirs(PROC_PATH, '.wav')
    missing_dirs = list(raw_dirs.difference(proc_dirs))
    print(missing_dirs)
    for directory in missing_dirs:
        process(raw_dirs_dict[directory], directory)

    norm_dirs = get_processed_dirs(PROC_PATH, '_norm.txt')
    missing_norm_dirs = list(raw_dirs.difference(norm_dirs))
    for directory in missing_norm_dirs:
        print('normalizing text of %s'%(directory))
        text_source = os.path.join(PROC_PATH, directory, 'wav',
                                   directory+'.txt')
        text_target = text_source.replace('.txt', '_norm.txt')