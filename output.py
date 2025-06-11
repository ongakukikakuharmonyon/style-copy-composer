# output.py (修正版)

from typing import List, Tuple
from music21 import stream, note, metadata, meter, instrument, clef # clef をインポート
import os

NoteState = Tuple[str, float]

def note_states_to_musicxml(note_states: List[NoteState], output_path: str,
                             title: str = "Generated Score",
                             time_signature_str: str = "4/4") -> None:
    
    s = stream.Stream()

    # メタ情報
    s.metadata = metadata.Metadata()
    s.metadata.title = title
    s.metadata.composer = "Style-Copy Composer"

    # ストリームの先頭に、音部記号、楽器情報、拍子記号を追加
    s.insert(0, clef.TrebleClef()) # ト音記号を明示的に指定
    s.insert(0, instrument.Piano())
    s.insert(0, meter.TimeSignature(time_signature_str))

    for pitch_str, duration in note_states:
        if pitch_str == 'Rest':
            n = note.Rest()
        else:
            n = note.Note(pitch_str)
        n.quarterLength = duration
        s.append(n)

    # 【最重要】この一行がすべてを解決します！
    # ストリーム内の音符を、拍子記号に基づいて自動で小節に分割する
    s.makeMeasures(inPlace=True)

    try:
        s.write('musicxml', fp=output_path)
    except Exception as e:
        print(f"Error writing MusicXML file: {e}")
