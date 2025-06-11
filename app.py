# -*- coding: utf-8 -*-
# analyzer.py (専門的解剖を行う、真の最終形態)

from typing import List, Dict, Any
from music21 import converter, stream, clef, instrument, meter, key, chord, note

def analyze_song_structure(xml_path: str) -> Dict[str, Any]:
    """
    MusicXMLファイルを構造的に解剖し、人間が理解できる「設計図」を生成する。
    """
    try:
        score = converter.parse(xml_path)
    except Exception as e:
        return {"error": f"ファイル解析に失敗しました: {e}"}

    # 1. 楽曲全体の基本情報を抽出
    song_profile: Dict[str, Any] = {
        "key": "N/A",
        "time_signature": "N/A",
        "chord_progression": [],
        "parts": []
    }

    try:
        song_profile["key"] = score.analyze('key').name
        ts = score.flat.getElementsByClass(meter.TimeSignature).first()
        if ts:
            song_profile["time_signature"] = f"{ts.numerator}/{ts.denominator}"
        else:
            song_profile["time_signature"] = "4/4" # デフォルト
    except Exception as e:
        print(f"Key/Time signature analysis failed: {e}")

    # 2.【改善】人間が読めるコード進行を抽出
    try:
        chordified_score = score.chordify()
        prog = []
        for ch in chordified_score.flat.getElementsByClass('Chord'):
            # 最も一般的でシンプルなコード名を取得する
            chord_name = ch.figure
            prog.append(chord_name)
        
        # 連続する同じコードをまとめる
        if prog:
            final_progression = [prog[0]]
            for i in range(1, len(prog)):
                if prog[i] != final_progression[-1]:
                    final_progression.append(prog[i])
            song_profile["chord_progression"] = final_progression
            
    except Exception as e:
        print(f"Chord analysis failed: {e}")

    # 3.【最重要】各パートを、音部記号を含めて精密に解剖
    for part_elem in score.parts:
        # このパートの最初の音部記号を、より確実に探し出す
        first_clef = part_elem.recurse().getElementsByClass(clef.Clef).first()
        
        part_info = {
            "part_name": part_elem.partName or f"Part {len(song_profile['parts']) + 1}",
            "instrument": (part_elem.getInstrument().instrumentName if part_elem.getInstrument() else "Unknown"),
            "clef": (first_clef.name if first_clef else "unknown"), # 確実に音部記号を記録
            "note_sequence": []
        }
        
        # パート内の音符/和音/休符を抽出
        for elem in part_elem.recurse():
            if isinstance(elem, note.Note):
                part_info["note_sequence"].append(('Note', elem.pitch.nameWithOctave, float(elem.quarterLength)))
            elif isinstance(elem, chord.Chord):
                # 和音は構成音をすべて記録する（後で使えるように）
                chord_notes = [p.nameWithOctave for p in elem.pitches]
                part_info["note_sequence"].append(('Chord', chord_notes, float(elem.quarterLength)))
            elif isinstance(elem, note.Rest):
                part_info["note_sequence"].append(('Rest', 'Rest', float(elem.quarterLength)))

        song_profile["parts"].append(part_info)
        
    return song_profile
