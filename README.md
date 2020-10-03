# Satria Data
Memprediksi Hoax dari gambar dan text.

### Konten
| Konten              | Laman Kontent |
|   -------------     |:-------------:| 
| Website sumber data | [turnbackhoax.id](http://turnbackhoax.id/)                  |
| Kaggle Data         | [dsini](https://www.kaggle.com/wahyusetianto/data-bdc)      |
| Model               | [disini](https://www.kaggle.com/pencarikebahagiaan/modelku) |

## Preprocess Data
### Gambar
1. Checking Missing Data
1. Karena ukuran gambar yang berbeda - beda maka diambil sample tengah - tengah tiap gambar.<br>
    <img src = "Sample Images/1.jpg" alt = "prep 1" style="display: block; margin-left: auto; margin-right: auto; width: 50%;" />
1. Resize gambar ke ukuran 512 x 512<br>
1. Upsampling dengan Augmentasi data.<br>
Up Sampling data gambar kelas 0 sebesar : 50%, 100%, dan 200%, dengan menggunakan `augmentasi`. Augmentasi yang akan digunakan pada data gambar yaitu:<br>
`Rotasi secara acak pada rentang -70 sd. 70 derajad`<br>
    <img src = "Sample Images/download (3).png" alt = "prep 1" style="display: block; margin-left: auto; margin-right: auto; width: 80%;" />

### Text
1. Drop Duplicate Value pada data text
1. Masking Content sebelum di normalize [Encode]<br>
Melakukan masking untuk kata kata yang mengandung `URL, Hashtag, Tag, Emoji`
    ```
    # Contoh
    Website Statistika UNJ adalah http://fmipa.unj.ac.id/statistika/
    BEM Statistika UNJ #AltairBergerakMengukir
    @jokowi adalah presiden RI
    Lucu 😂

    # Encode
    Website Statistika UNJ adalah MASKURLS1MASK
    BEM Statistika UNJ MASKHASHTAGS1MASK
    MASKTAGS1MASK adalah presiden RI
    Lucu MASKEMOJIS1MASK
    ```
1. Normalize text
1. Decode mask content [Decode]
1. Clear String Punctuation
1. De-emojized
1. Fixxing misstype / typo [Manual 😂]

## Modelling
### Images
<table style="text-align: center;margin-left: auto;margin-right: auto;">
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
<table style="text-align: center;margin-left: auto;margin-right: auto;">
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
1. Model CNN pada Fasttext sangat simple, jadi mungkin akurasinya bisa bertamabah lagi jika dioptimalisasi atau menggunakan RNN.
1. Masih ada banyak kata yang misspel sehingga cukup banya katak yang tidak mendapatkan vector dari `Fastext`.
1. Model `Bert` yang di gunakan adalah [cahya/bert-base-indonesian-522M](https://huggingface.co/cahya/bert-base-indonesian-522M).
1. Dari model model yang ada bert dapat mengklasifikasikan hoax lebih baik dari model - model lainnya namun tetap memiliki kesulitan dalam mengenali kelas 0.

 © Catatan Cakrawala 2020