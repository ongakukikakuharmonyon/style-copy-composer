# composer.py

import random
from collections import defaultdict
from typing import List, Tuple

NoteState = Tuple[str, float]  # 例: ('C4', 0.25)

class MelodyComposer:
    def __init__(self):
        self.transition_table = defaultdict(list)

    def train(self, note_sequence: List[NoteState]):
        if len(note_sequence) < 3:
            return
        for i in range(len(note_sequence) - 2):
            key = (note_sequence[i], note_sequence[i+1])
            next_state = note_sequence[i+2]
            self.transition_table[key].append(next_state)

    def generate(self, start_sequence: List[NoteState], length: int = 50,
                 pitch_range: Tuple[str, str] = ('C4', 'C6')) -> List[NoteState]:
        from music21 import pitch as m21pitch
        
        if len(start_sequence) < 2 or not self.transition_table:
            return start_sequence

        result = start_sequence.copy()
        target_length = len(result) + length
        max_tries = length * 10
        low_midi = m21pitch.Pitch(pitch_range[0]).midi
        high_midi = m21pitch.Pitch(pitch_range[1]).midi

        while len(result) < target_length and max_tries > 0:
            key = tuple(result[-2:])
            candidates = self.transition_table.get(key, [])

            if not candidates:
                # 遷移先がなければランダムなキーで再試行
                if not self.transition_table: break
                key = random.choice(list(self.transition_table.keys()))
                candidates = self.transition_table.get(key, [])
                if not candidates: break

            next_state = random.choice(candidates)
            max_tries -= 1

            if next_state[0] != 'Rest':
                current_midi = m21pitch.Pitch(next_state[0]).midi
                if not (low_midi <= current_midi <= high_midi):
                    continue
            result.append(next_state)
        return result
