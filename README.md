# Big Data Challenge - Satria Data 2020

Project team **Catatan Cakrawala** pada lomba `Big Data Challenge - Satria Data 2020`

### Task

Memprediksi Hoax dari gambar dan text (`Binary Classification`).

### [Notebooks](https://github.com/Hyuto/BDC-Satria-Data/tree/master/Notebooks)

1. `BDC - EfficientNetB7.ipynb`
2. `BDC - Main Notebook.ipynb`

### Tambahan
| Keterangan          | Laman Kontent |
|   -------------     |:-------------:| 
| Website sumber data | [turnbackhoax.id](http://turnbackhoax.id/)                  |
| Kaggle Data         | [disini](https://www.kaggle.com/wahyusetianto/data-bdc)     |
| Model               | [disini](https://www.kaggle.com/pencarikebahagiaan/modelku) |

## [Preprocess Data](https://github.com/Hyuto/BDC-Satria-Data/tree/master/Preprocess%20code)

Preprocessing data.

### Script preprocess:

```
Preprocess code/
      |------- RPU.py
      |------- Preprocess.py
```

#### Keterangan :

1. `RPU.py` => Script `Preprocess`, `Augmentasi`, dan `Up-sampling` data gambar
2. `Preprocess.py` => Script `Preprocess` pada data text

### Data Gambar

1. Checking Missing Data
2. Karena ukuran gambar yang berbeda - beda maka diambil sample tengah - tengah tiap gambar.<br>
    <img src = "Sample Images/1.jpg" alt = "prep 1" style="display: block; margin-left: auto; margin-right: auto; width: 50%;" />
3. Resize gambar ke ukuran 512 x 512<br>
4. Upsampling dengan Augmentasi data.<br>
Up Sampling data gambar kelas 0 sebesar : 50%, 100%, dan 200%, dengan menggunakan `augmentasi`. Augmentasi yang akan digunakan pada data gambar yaitu:<br>
`Rotasi secara acak pada rentang -70 sd. 70 derajad`<br>
    <img src = "Sample Images/2.png" alt = "prep 2" style="display: block; margin-left: auto; margin-right: auto; width: 50%;" />

### Data Text

1. Drop `duplicate value` pada data text
2. Masking Content sebelum di normalize [Encode]<br>
Melakukan masking untuk kata kata yang mengandung `URL, Hashtag, Tag, Emoji`
    ```
    # Contoh
    Website Google adalah http://google.com
    Jangan lupa pakai masker #StaySafe
    @jokowi adalah presiden RI
    Lucu 😂

    # Encode
    Website Google adalah MASKURLS1MASK
    Jangan lupa pakai masker MASKHASHTAGS1MASK
    MASKTAGS1MASK adalah presiden RI
    Lucu MASKEMOJIS1MASK
    ```
3. Normalize text<br>
Melakukan normalisasi text yang berkaita dengan tanda baca berdasarkan kaidah penulisan bahasa Indonesia.
    ```
    # Contoh
    Budi membayar2.000 ban yang dibelinya senilai rp.2.000.000

    # Preprocessed
    Budi membayar 2.000 ban yang dibelinya senilai rp. 2.000.000
    ```
4. Decode mask content<br>
Mengembalikan konten yang di `encode` sebelumnya.
    ```
    # Contoh
    Website Google adalah MASKURLS1MASK

    # Decode
    Website Google adalah http://google.com
    ```
5. Clear String Punctuation<br>
Menghapus tanda baca dari data text
6. De-emojized<br>
Mengubah `emoji` yang ada pada text menjadi kata-kata yang melambangkan `emoji` tersebut
    ```
    🙏 -> folded hands
    😃 -> grinning face with big eyes
    ```
7. Fixxing misstype / typo [Manual 😂]<br>
Membenarkan kata - kata yang misstype atau typo dengan cara membuat vocabulary dari data text pada `Data Latih BDC.xlsx` lalu mengexportnya ke file `.txt` untuk dilakukan pemeriksaan secara manual.

## Modelling

### Images

<table style="text-align: center; margin-left: auto; margin-right: auto;">
    <thead>
        <tr>
            <th>Model</th>
            <th>Best Accuracy</th>
            <th>Best F1 Score</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>EfficientNet B5</td>
            <td>82,6%</td>
            <td>89,5%</td>
        </tr>
        <tr>
            <td>EfficientNet B7</td>
            <td>83,5%</td>
            <td>90,5%</td>
        </tr>
    </tbody>
</table>

### Teks

<table style="text-align: center; margin-left: auto;margin-right: auto;">
    <tr>
        <th>Model</th>
        <th>Best Accuracy</th>
        <th>Best F1 Score</th>
    </tr>
    <tr>
        <td>Fasttext ID on Embedding + Simple CNN</td>
        <td> 86,2% </td>
        <td> 92,2% </td>
    </tr>
    <tr>
        <td>Bert Base Indonesian </td>
        <td> 86.6 - 87 % </td>
        <td> 92.6 - 92.8 % </td>
    </tr>
</table>

## Note:

1. EfficientNetB7 akurasinya jadi lebih stabil dengan weight `noise-student`
2. Model CNN pada Fasttext sangat simple, jadi mungkin akurasinya bisa bertamabah lagi jika dioptimalisasi atau menggunakan RNN.
3. Masih ada banyak kata yang misspel sehingga cukup banya katak yang tidak mendapatkan vector dari `Fastext`.
4. Model `Bert` yang di gunakan adalah [cahya/bert-base-indonesian-522M](https://huggingface.co/cahya/bert-base-indonesian-522M).
5. Dari model model yang ada bert dapat mengklasifikasikan hoax lebih baik dari model - model lainnya namun tetap memiliki kesulitan dalam mengenali kelas `0`.

 © Catatan Cakrawala 2020