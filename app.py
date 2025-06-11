# app.py (修正版)

import streamlit as st
import tempfile
import os
from analyzer import extract_note_states_from_xml
from composer import MelodyComposer
from output import note_states_to_musicxml

st.set_page_config(page_title="Style-Copy Composer", layout="centered")

st.title("🎼 Style-Copy Composer")
st.markdown("MusicXMLファイルをアップロードして、似たスタイルの新しいメロディを生成します。")

# --- Step 1: 楽譜ファイルをアップロード ---
st.header("Step 1: 楽譜ファイルをアップロード")
uploaded_file = st.file_uploader(
    "🎵 MusicXMLファイル (.xml, .musicxml)", 
    type=["xml", "musicxml"]
)

if uploaded_file is not None:
    input_tmp_path = None
    output_tmp_path = None
    try:
        # --- ここが重要な修正点 ---
        # アップロードされたファイルデータをバイナリとして安全に一時ファイルへ書き込む
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer()) # .read() の代わりに .getbuffer() を使用
            input_tmp_path = tmp_file.name

        # --- Step 2: パラメータ設定 ---
        st.header("Step 2: 生成パラメータを設定")
        length = st.slider("生成するノート数", 16, 128, 48, step=4, help="生成するメロディの長さをノート数で指定します。")
        
        pitch_options = {
            "低音域 (C3-C5)": ("C3", "C5"),
            "中音域 (C4-C6)": ("C4", "C6"),
            "高音域 (C5-C7)": ("C5", "C7"),
        }
        selected_pitch_label = st.selectbox(
            "音域の制限", 
            options=list(pitch_options.keys()), 
            index=1,
            help="生成されるメロディの音域を制限します。"
        )
        pitch_range_tuple = pitch_options[selected_pitch_label]

        # --- Step 3: 生成実行 ---
        st.header("Step 3: メロディを生成")
        if st.button("🎬 メロディを生成する", type="primary"):
            with st.spinner("楽譜を分析し、新しいメロディを生成中です..."):
                note_seq = extract_note_states_from_xml(input_tmp_path)

                if len(note_seq) < 3:
                    st.error("学習用データが不足しています。3つ以上の音符または休符を含むファイルをアップロードしてください。")
                else:
                    composer = MelodyComposer()
                    composer.train(note_seq)
                    start_seq = note_seq[:2]
                    generated_notes = composer.generate(
                        start_seq,
                        length=length,
                        pitch_range=pitch_range_tuple
                    )

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".musicxml") as out_file:
                        output_tmp_path = out_file.name
                        note_states_to_musicxml(generated_notes, output_tmp_path, title="Style-Copy Output")
                    
                    st.success("✅ 生成が完了しました！")
                    
                    with open(output_tmp_path, "rb") as f:
                        st.download_button(
                            label="📥 MusicXMLをダウンロード",
                            data=f,
                            file_name="style_copy_output.musicxml",
                            mime="application/xml"
                        )
    finally:
        if input_tmp_path and os.path.exists(input_tmp_path):
            os.remove(input_tmp_path)
        if output_tmp_path and os.path.exists(output_tmp_path):
            os.remove(output_tmp_path)
