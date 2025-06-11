# analyzer.py

from typing import List, Tuple
from music21 import converter, note, stream, chord

NoteState = Tuple[str, float]  # 例: ('C4', 0.25)

def extract_note_states_from_xml(xml_path: str) -> List[NoteState]:
    """
    MusicXMLファイルから (音高, 音価) のリストを抽出する。
    和音は最高音を採用し、休符は 'Rest' として扱う。
    """
    try:
        score = converter.parse(xml_path)
        notes_to_parse = score.flat.notesAndRests
    except Exception as e:
        print(f"Error parsing MusicXML file: {e}")
        return []

    note_states: List[NoteState] = []
    for elem in notes_to_parse:
        if isinstance(elem, note.Note):
            pitch_str = elem.pitch.nameWithOctave
            duration = float(elem.quarterLength)
            note_states.append((pitch_str, duration))
        elif isinstance(elem, chord.Chord):
            pitch_str = elem.pitches[-1].nameWithOctave
            duration = float(elem.quarterLength)
            note_states.append((pitch_str, duration))
        elif isinstance(elem, note.Rest):
            duration = float(elem.quarterLength)
            note_states.append(('Rest', duration))

    return note_states
