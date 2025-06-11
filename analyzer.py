# analyzer.py (最終修正版)

from typing import List, Tuple
from music21 import converter, note, stream, chord

NoteState = Tuple[str, float]

def extract_note_states_from_xml(xml_path: str) -> List[NoteState]:
    """
    MusicXMLファイルから (音高, 音価) のリストを抽出する。
    【重要】最初のパートのみを対象とし、メロディラインとして扱う。
    """
    try:
        score = converter.parse(xml_path)
        # --- ここが最重要の修正点 ---
        # score.flat の代わりに、最初のパート (parts[0]) のみを対象にする
        instrument_part = score.parts[0].recurse()
    except Exception as e:
        print(f"Error parsing MusicXML file: {e}")
        return []

    note_states: List[NoteState] = []
    for elem in instrument_part:
        if isinstance(elem, note.Note):
            pitch_str = elem.pitch.nameWithOctave
            duration = float(elem.quarterLength)
            note_states.append((pitch_str, duration))
        elif isinstance(elem, chord.Chord):
            # 和音の場合、一番高い音をメロディとして採用
            pitch_str = elem.pitches[-1].nameWithOctave
            duration = float(elem.quarterLength)
            note_states.append((pitch_str, duration))
        elif isinstance(elem, note.Rest):
            duration = float(elem.quarterLength)
            note_states.append(('Rest', duration))

    return note_states
