# 🎼 Style-Copy Composer

**Style-Copy Composer** は、MusicXML形式の楽譜からスタイルを学習し、類似したパターンの新しいメロディを生成するWebアプリケーションです。  
`Streamlit` を使用した直感的なUIと、`music21` による楽譜解析を組み合わせ、誰でも簡単に音楽生成を試せるツールを目指しています。

## 🚀 主な機能

- **簡単な操作**: MusicXMLファイルをアップロードし、ボタンを押すだけで新しいメロディを生成。
- **スタイル学習**: 2-gramマルコフ連鎖モデルにより、入力された楽譜の音の繋がりパターンを学習。
- **パラメータ調整**: 生成するメロディの長さや音域を自由に設定可能。
- **MusicXML出力**: 生成結果を標準的なMusicXML形式でダウンロードし、MuseScoreなどの楽譜作成ソフトで編集・再生可能。

## 🔧 実行方法

このアプリはStreamlit Community Cloudで公開されています。特別なセットアップは不要です。
もしローカルで実行したい場合は、以下の手順に従ってください。

1. リポジトリをクローン: `git clone https://github.com/your-username/style-copy-composer.git`
2. ディレクトリに移動: `cd style-copy-composer`
3. 依存関係をインストール: `pip install -r requirements.txt`
4. アプリを起動: `streamlit run app.py`

## 🧠 使用技術

- **UIフレームワーク**: [Streamlit](https://streamlit.io/)
- **楽譜解析ライブラリ**: [music21](https://web.mit.edu/music21/)
- **楽曲生成アルゴリズム**: マルコフ連鎖 (2-gram)
