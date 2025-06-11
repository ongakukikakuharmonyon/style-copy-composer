# analyzer.py (楽曲の構造を丸ごと分析する最終形態)

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
        for ch in chordified_score.flat.getElementsByClass('Chord'):
            song_profile["chord_progression"].append(ch.pitchedCommonName)
        # 連続する同じコードをまとめる
        if song_profile["chord_progression"]:
            prog = [song_profile["chord_progression"][0]]
            for i in range(1, len(song_profile["chord_progression"])):
                if song_profile["chord_progression"][i] != song_profile["chord_progression"][i-1]:
                    prog.append(song_profile["chord_progression"][i])
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
        
        # 楽器情報を取得
        inst = part_elem.getElementsByClass(instrument.Instrument).first()
        if inst:
            part_info["instrument"] = inst.instrumentName
            
        # 音部記号を取得
        cl = part_elem.getElementsByClass(clef.Clef).first()
        if cl:
            part_info["clef"] = cl.name
        
        # このパートの音符シーケンスを抽出
        for elem in part_elem.recurse():
            if isinstance(elem, note.Note):
                part_info["note_sequence"].append(('Note', elem.pitch.nameWithOctave, float(elem.quarterLength)))
            elif isinstance(elem, chord.Chord):
                 # 和音は最高音を代表として追加
                part_info["note_sequence"].append(('Chord', elem.pitches[-1].nameWithOctave, float(elem.quarterLength)))
            elif isinstance(elem, note.Rest):
                part_info["note_sequence"].append(('Rest', 'Rest', float(elem.quarterLength)))

        song_profile["parts"].append(part_info)
        
    return song_profile

# テスト用のコード (app.pyからは直接使わない)
if __name__ == '__main__':
    # このファイルにサンプルXMLへのパスを記述して、python analyzer.py で実行すると結果が見れる
    import json
    path = "sample_input/example.xml" # あなたのPCのファイルパス
    profile = analyze_song_structure(path)
    print(json.dumps(profile, indent=2))
