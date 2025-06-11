# -*- coding: utf-8 -*-
# analyzer.py (文字コード対応・最終版)

from typing import List, Dict, Any
from music21 import converter, stream, clef, instrument, meter, key, chord, note

def analyze_song_structure(xml_path: str) -> Dict[str, Any]:
    """
    MusicXMLファイルを構造的に分析し、楽曲の「設計図」を辞書として返す。
    """
    try:
        score = converter.parse(xml_path)
    except Exception as e:
        return {"error": f"File parsing failed: {e}"}

    # 1. 楽曲全体の情報を抽出
    song_profile: Dict[str, Any] = {
        "key": score.analyze('key').name,
        "time_signature": "",
        "chord_progression": [],
        "parts": []
    }

    # 拍子記号を取得 (最初のパートから)
    try:
        ts = score.parts[0].getElementsByClass(meter.TimeSignature)[0]
        song_profile["time_signature"] = f"{ts.numerator}/{ts.denominator}"
    except IndexError:
        song_profile["time_signature"] = "4/4" # 見つからない場合はデフォルト

    # 2. コード進行を抽出 (chordifyを使って全体から)
    try:
        chordified_score = score.chordify()
        chords_in_stream = chordified_score.flat.getElementsByClass('Chord')
        if chords_in_stream:
            prog = [chords_in_stream[0].pitchedCommonName]
            for i in range(1, len(chords_in_stream)):
                current_chord_name = chords_in_stream[i].pitchedCommonName
                if current_chord_name != prog[-1]:
                    prog.append(current_chord_name)
            song_profile["chord_progression"] = prog
    except Exception as e:
        print(f"Chord analysis failed: {e}")

    # 3. 各パートの情報を個別に抽出
    for part_elem in score.parts:
        part_info = {
            "part_name": part_elem.partName or f"Part {len(song_profile['parts']) + 1}",
            "instrument": "",
            "clef": "",
            "note_sequence": []
        }
        
        inst = part_elem.getElementsByClass(instrument.Instrument).first()
        if inst:
            part_info["instrument"] = inst.instrumentName
            
        cl = part_elem.getElementsByClass(clef.Clef).first()
        if cl:
            part_info["clef"] = cl.name
        
        for elem in part_elem.recurse():
            if isinstance(elem, note.Note):
                part_info["note_sequence"].append(('Note', elem.pitch.nameWithOctave, float(elem.quarterLength)))
            elif isinstance(elem, chord.Chord):
                part_info["note_sequence"].append(('Chord', elem.pitches[-1].nameWithOctave, float(elem.quarterLength)))
            elif isinstance(elem, note.Rest):
                part_info["note_sequence"].append(('Rest', 'Rest', float(elem.quarterLength)))

        song_profile["parts"].append(part_info)
        
    return song_profile
