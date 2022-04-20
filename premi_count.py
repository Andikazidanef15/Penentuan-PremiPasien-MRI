import pandas as pd
import matplotlib.pyplot as plt
from CleaningData import data_cleaner

import warnings
warnings.filterwarnings('ignore')

class premi_pasien:
    def __init__(self, nama, usia, layanan, biaya_pengobatan, kasus, df):

        self.nama = nama
        self.usia = usia
        self.layanan = layanan
        self.biaya_pengobatan = biaya_pengobatan
        self.kasus = kasus
        self.df = df

        # Subset data
        data = self.df[self.df['rnmjasa'] == self.layanan]

        # Group by Total Biaya
        df1 = data.groupby(['selang_umur'])['total_biaya'].agg('mean')
        dict_besar_klaim = df1.to_dict()

        data['besar_klaim_per_segmen'] = data['selang_umur'].map(dict_besar_klaim).astype('float64')

        if self.kasus == 'KASUS 1.1':
            data['jumlah_klaim'] = data['total_biaya'] // data['rfee']

            # Segmentasi jumlah klaim berdasarkan selang umur
            df2 = data.groupby(['selang_umur'])['jumlah_klaim'].agg('mean')
            dict_jumlah_klaim = df2.to_dict()
            data['jumlah_klaim_per_segmen'] = data['selang_umur'].map(dict_jumlah_klaim).astype('float64')

            data['natural_premium'] = data['besar_klaim_per_segmen'] * data['jumlah_klaim_per_segmen'] * (
                        1 + (8.17 / 100)) ** (-1 / 2)

        elif self.kasus == 'KASUS 1.2':
            # Buat fitur baru
            data['jumlah_klaim'] = 0

            # Tentukan jumlah klaim berdasarkan asumsi tersebut
            for i in range(len(df)):
                if data['biaya'][i] == data['rfee'][i]:
                    data['jumlah_klaim'][i] = 1
                else:
                    data['jumlah_klaim'][i] = 2

                    # Segmentasi jumlah klaim berdasarkan selang umur
            df2 = data.groupby(['selang_umur'])['jumlah_klaim'].agg('mean')
            dict_jumlah_klaim = df2.to_dict()
            data['jumlah_klaim_per_segmen'] = data['selang_umur'].map(dict_jumlah_klaim).astype('float64')
            data['natural_premium'] = data['besar_klaim_per_segmen'] * data['jumlah_klaim_per_segmen'] * (
                        1 + (8.17 / 100)) ** (-1 / 2)

        elif self.kasus == 'KASUS 1.3':
            data['natural_premium'] = 2 * data['total_biaya'] * (1 + (8.17 / 100)) ** (-1 / 2)

        else:
            raise TypeError("Pilih kasus berdasarkan pilihan : KASUS 1.1, KASUS 1.2, KASUS 1.3")

        data['selisih_klaim_premi'] = data['natural_premium'] - data['total_biaya']
        data['persentase_selisih'] = data['selisih_klaim_premi'] / data['total_biaya'] * 100

        # Definisikan premi level
        df3 = data.groupby(['selang_umur'])['natural_premium'].agg('mean')
        dict_premi_level = df3.to_dict()
        data['level_premium'] = data['selang_umur'].map(dict_premi_level).astype('float64')

        self.data = data
        self.df3 = df3

    def introduksi_pasien(self):
        # Perkenalan pasien
        kalimat = "Pasien bernama {0}, berusia {1} dan berobat di klinik MRI untuk pelayanan {2} dengan biaya pengobatan Rp{3}".format(
            self.nama, self.usia,
            self.layanan, self.biaya_pengobatan)
        return kalimat

    def premi_yang_dibayarkan(self):
        i = 0
        while self.usia not in self.df3.index[i]:
            i += 1

        if self.usia in self.df3.index[i]:
            premi_level = self.df3[self.df3.index[i]]

        kalimat = "Asumsi pembayaran premi mengikuti {0}, untuk biaya pengobatan Rp{1}, {2} harus membayar premi sebesar Rp{3}".format(
            self.kasus, self.biaya_pengobatan, self.nama, round(premi_level))
        return kalimat

    def dinamika_premi(self):
        # Buat plot premi terhadap total biaya pasien untuk kategori tertentu
        umur_klaim2 = self.data[
            ['umur', 'total_biaya', 'besar_klaim_per_segmen', 'natural_premium', 'level_premium']].drop_duplicates(
            subset=['umur']).sort_values(by=['umur'], ascending=True)
        plt.plot(umur_klaim2['umur'], umur_klaim2['total_biaya'], label='Jumlah Biaya')
        plt.plot(umur_klaim2['umur'], umur_klaim2['level_premium'], color='black', linestyle='--', label='Premi Level')
        plt.plot(umur_klaim2['umur'], umur_klaim2['natural_premium'], label='Premi Alami')
        plt.xlabel('usia')
        plt.ylabel('besar biaya (puluhan juta rupiah)')
        plt.legend()
        plt.show()
