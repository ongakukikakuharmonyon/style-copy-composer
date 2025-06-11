# app.py (分析結果を表示する「司令室」バージョン)

import streamlit as st
import tempfile
import os
import json # JSONをきれいに表示するためにインポート

# 1. インポートする関数名を、新しい名前に変更！
from analyzer import analyze_song_structure
# MelodyComposer と note_states_to_musicxml は一旦使わない

st.set_page_config(page_title="Style-Copy Composer", layout="wide")

st.title("🎼 Style-Copy Composer (v2.0: 構造分析モード)")
st.markdown("MusicXMLファイルをアップロードして、その楽曲構造（設計図）を分析します。")

uploaded_file = st.file_uploader(
    "🎵 MusicXMLファイル (.xml, .musicxml) をアップロード", 
    type=["xml", "musicxml"]
)

if uploaded_file is not None:
    input_tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            input_tmp_path = tmp_file.name

        # 2. 楽曲分析を実行し、「設計図」を取得
        with st.spinner("楽曲の構造を解析中..."):
            song_profile = analyze_song_structure(input_tmp_path)
        
        st.success("✅ 楽曲分析が完了しました！")

        # 3. 分析結果（設計図）を画面に表示
        if "error" in song_profile:
            st.error(f"分析中にエラーが発生しました: {song_profile['error']}")
        else:
            st.header("楽曲の設計図 (Song Profile)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("調 (Key)", song_profile.get("key", "N/A"))
            with col2:
                st.metric("拍子 (Time Signature)", song_profile.get("time_signature", "N/A"))
            
            st.subheader("コード進行 (Chord Progression)")
            st.text(" -> ".join(song_profile.get("chord_progression", [])))
            
            st.subheader("パート詳細 (Parts)")
            for i, part in enumerate(song_profile.get("parts", [])):
                with st.expander(f"パート {i+1}: {part.get('part_name', 'Unnamed')} ({part.get('instrument', 'N/A')})"):
                    st.write(f"**音部記号 (Clef):** {part.get('clef', 'N/A')}")
                    st.write(f"**ノート数:** {len(part.get('note_sequence', []))}")
                    # ノートシーケンスの最初の10件だけ表示
                    st.json(part.get('note_sequence', [])[:10])

    finally:
        if input_tmp_path and os.path.exists(input_tmp_path):
            os.remove(input_tmp_path)
