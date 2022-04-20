import pandas as pd
import numpy as np
import re

def data_cleaner(df):
    # Drop fitur yang tidak digunakan
    df.drop(['rdisc', 'bayar', 'selisih', 'selisihx', 'bayarx'], axis=1, inplace=True)

    # Ubah bl_th menjadi tahun semua
    for i in range(len(df)):
        if df['bl_th'][i] == 'Bulan':
            df['umur'][i] = np.floor(df['umur'][i] / 12)
        else:
            continue

    # Drop fitur bl_th karena redundant
    df.drop(['bl_th'], axis=1, inplace=True)

    # Buat kolom baru berisi selang umur di mana umur pasien tersebut berada
    df['selang_umur'] = pd.qcut(df['umur'], 10)

    # Definisikan total biaya pengobatan sebagai biaya3 (biaya keseluruhan pengobatan pasien)
    df['total_biaya'] = df['biaya3']

    # Hilangkan space yang tak perlu di string
    df['rnmjasa'] = df['rnmjasa'].apply(lambda string: string.strip())

    ## Bersih-bersih string
    def layanan_cleaner(sentence):
      # Membersihkan string layanan
      sentence = sentence.upper()
      sentence = re.sub(r'\s*\(\w+(\s|-)*\w+\)*','',sentence)
      sentence = re.sub(r'(WHOLE|SINISTRA|DEXTRA|PAKET\sI{0,2}|CANGGIH|MP|ATAS|BAWAH)','',sentence)
      sentence = re.sub(r'\s*\+\s*\w+','',sentence)
      sentence = sentence.strip()
      return sentence

    # Ubah di rnmjasa, ganti KONTRAS I dan KONTRAS II dengan KONTRAS
    df['rnmjasa'] = df['rnmjasa'].apply(layanan_cleaner)
    df['rnmjasa'] = df['rnmjasa'].replace(['KONTRAS I', 'KONTRAS II'], 'KONTRAS')

    return df
