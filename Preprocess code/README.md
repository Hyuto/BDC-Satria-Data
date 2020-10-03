# Preprocessing Code Catatan Cakrawala
Python code untuk proses `preprocessing` Catatan Cakrawala.

## 1. `RPU.py`
Script untuk `Preprocessing`, `Augmentasi`, dan `Up-Sample data` pada data gambar.

Fungsi :
1. `load_and_preprocess_image` => Load & Preprocess data gambar
2. `data_augmentation` => Augmentasi data gambar
3. `ApplyAUG` => Up-Sampling data dengan fungsi `augmentasi`

Run via `Shell`
```
python RPU.py PATH SIZE TEST_SIZE UP_SAMPLES UP_SAMPLE_CLASS
```
Data yang kami gunakan didapatkan dari
```
python RPU.py PATH-FOLDER-DATA-LATIH-GAMBAR \
                SIZE:512 TEST_SIZE:0.15 \
                UP_SAMPLES:0.5-1-2 UP_SAMPLE_CLASS:0
```

## 2. `Preprocess.py`
Script untuk `Preprocessing` pada data text.

Fungsi :
1. `FeatureExtraction` => Extract feature/konten dalam text berupa `URL`, `Hashtag`, `Tag`, `Emoji` untuk mendapatkan frekuensi kemunculannya dan MASKING untuk proses `encode` dan `decode`.
2. `SpellChecker` => Mengecek dan membenarkan kata-kata yang misstype/typo.
3. `clean_up` => Membersihkan `\n` dan mengubah menjadi `lowercased` data text
4. `normalize` => Normalisasi peletakan tanda baca
5. `remove_punc` => Menghapus tanda baca
6. `deemojized` => Mengganti `Emoji` menjadi kalimat 
7. `RUnecesarry` => Menghapus kata kata yang tidak perlu dan juga menghapus `stopwords`

## Requirements :
### `RPU.py`
   * numpy
   * pandas
   * tqdm
   * PIL
   * tensorflow >= 2.1.0
   * sklearn & skimage
### `Preprocess.py`
   * numpy
   * pandas
   * emoji
   * tqdm

 © Catatan Cakrawala 2020