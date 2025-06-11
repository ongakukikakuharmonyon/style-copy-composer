# analyzer.py (真・最終版)

from typing import List, Tuple
from music21 import converter, note, stream, chord

NoteState = Tuple[str, float]

def extract_note_states_from_xml(xml_path: str) -> List[NoteState]:
    """
    MusicXMLを解析し、ハーモニーを理解した上で、
    メロディライン（各瞬間の最高音）を抽出する。
    """
    try:
        score = converter.parse(xml_path)
        
        # --- ここが最後の切り札 ---
        # 1. 楽譜を解析し、同時発音をすべて和音（Chord）オブジェクトに変換する
        chordified_score = score.chordify()
        
    except Exception as e:
        print(f"Error parsing MusicXML file: {e}")
        return []

    note_states: List[NoteState] = []
    
    # 2. 和音化された楽譜から、音符・和音・休符を抽出
    for elem in chordified_score.flat.notesAndRests:
        if isinstance(elem, chord.Chord):
            # 和音の場合、一番高い音をメロディとして採用
            pitch_str = elem.pitches[-1].nameWithOctave
            duration = float(elem.quarterLength)
            note_states.append((pitch_str, duration))
        elif isinstance(elem, note.Note):
            # （単音の場合）そのまま採用
            pitch_str = elem.pitch.nameWithOctave
            duration = float(elem.quarterLength)
            note_states.append((pitch_str, duration))
        elif isinstance(elem, note.Rest):
            # 休符を採用
            duration = float(elem.quarterLength)
            note_states.append(('Rest', duration))

    return note_states
