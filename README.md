# rasp_dht22

## 説明

このプロジェクトは、DHT22センサーから温度と湿度データを読み取り、データベースに挿入します。

## インストール

1.  必要なPythonパッケージをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

2.  `.env`ファイルでデータベース接続を設定します。

## 使い方

1.  `get_dht22.py`スクリプトを実行して、センサーデータを読み取ります。

    ```bash
    python get_dht22.py
    ```

2.  `insert_dht22.py`スクリプトを実行して、データをデータベースに挿入します。

    ```bash
    python insert_dht22.py
    ```

## ファイル

*   `.env`: データベース接続設定が含まれています。
*   `get_dht22.py`: DHT22センサーからデータを読み取ります。
*   `insert_dht22.py`: データをデータベースに挿入します。
*   `README.md`: このファイル。

## ライセンス

MITライセンス
