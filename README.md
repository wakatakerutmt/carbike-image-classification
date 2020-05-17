# carbike-image-classification
写真から車かバイクかを判定するアプリ

## url
http://34.226.247.75/carbike/

※簡易的なデモなのでssl化は省略

## 環境

- Ubuntsu
- AWS EC2

| 環境 | ソフトウェア |
| ---- | ---- |
| Application Server | Gunicorn |
| Web Server | Nginx |
| Web Application Framework | Django=3.0.6 |

その他備考
- ResNetに全結合層を加え転移学習させたモデルを利用
- FlickrAPIによって取得した車とバイクの画像を用いて転移学習を行った、テストデータに対しては95％程の正答率
- PyTorch使用
