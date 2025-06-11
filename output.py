# output.py

from typing import List, Tuple
from music21 import stream, note, metadata, meter, instrument
import os

NoteState = Tuple[str, float]  # 例: ('C4', 0.25)

def note_states_to_musicxml(note_states: List[NoteState], output_path: str,
                             title: str = "Generated Score",
                             time_signature_str: str = "4/4") -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    s = stream.Stream()
    s.metadata = metadata.Metadata()
    s.metadata.title = title
    s.metadata.composer = "Style-Copy Composer"
    s.insert(0, instrument.Piano())
    s.insert(0, meter.TimeSignature(time_signature_str))

    for pitch_str, duration in note_states:
        if pitch_str == 'Rest':
            n = note.Rest()
        else:
            n = note.Note(pitch_str)
        n.quarterLength = duration
        s.append(n)

    try:
        s.write('musicxml', fp=output_path)
    except Exception as e:
        print(f"Error writing MusicXML file: {e}")
