# Satria Data
Memprediksi Hoax dari gambar dan text.

Website sumber data [dsini](http://turnbackhoax.id/)<br>
Kaggle Data [dsini](https://www.kaggle.com/wahyusetianto/data-bdc)<br>

## Images
<ol>
    <li>Preprocess Data & EDA [Done]
    <p>Preprocess:
    <ul>
        <li>Karena ukuran gambar yang berbeda - beda maka diambil sample tengah" tiap gambar.
        <li>Meresize gambar ke ukuran 512 x 512
    </ul>
    <li>Up Sampling & Augmentasi [Done]
    <ul>
        <li>Up Sampling data gambar kelas 0 sebesar: 50%, 100%, dan 200%
        <li>Augmentasi dengan : Rotasi secara acak pada rentang -70 sd 70 derajad
    </ul>
    <li>Memiilih Transfer Learning
    <table style="text-align:center">
        <tr>
            <th>Model</th>
            <th>Best Accuracy</th>
            <th>Best F1 Score</th>
        </tr>
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
    </table>
</ol>

## Teks
<ol>
    <li>Preprocess Data & EDA
    <p>Preprocess:
    <ul>
        <li> Drop Duplicate Value pada data text
        <li> Normalize text
        <li> Clear String Punctuation
        <li> De-emojized
        <li> Fixxing misstype / typo [Manual wkwk]
    </ul>
    <li>Memiilih Transfer Learning
    <table style="text-align:center">
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
            <td>XLM - Roberta</td>
            <td> - </td>
            <td> - </td>
        </tr>
        <tr>
            <td>BERT Multilangual</td>
            <td> - </td>
            <td> - </td>
        </tr>
    </table>
</ol>

## Note:
1. EfficientNetB7 akurasinya jadi lebih stabil dengan weight `noise-student`
1. Model CNN pada Fasttext sangat simple, jadi mungkin akurasinya bisa bertamabah lagi jika dioptimaliisasi atau menggunakan RNN
1. Jika menggunakan `LSTM` gak tau kenapa hasil yang diberikan selalu lebih dari hasil yang di berikan, padahal hasilnya lebig bagus.
1. Masih ada banyak kata yang misspel sehingga cukup banya kata yang tidak mendapatkan vector dari `Fastext`.

 © Catatan Cakrawala 2020