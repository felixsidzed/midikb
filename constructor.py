import json
from pretty_midi import PrettyMIDI, note_number_to_name, note_name_to_number

def construct(midiFile, tableFile, mode):
	with open(tableFile, "r") as f:
		table = json.load(f)
		f.close()

	seq = []
	midi = PrettyMIDI(midiFile)

	allNotes = []
	for instrument in midi.instruments: allNotes.extend(instrument.notes)
	allNotes.sort(key=lambda n: n.start)

	pitch2note = {note_name_to_number(k): v for k, v in table.items()}

	i = 0
	while i < len(allNotes):
		curTime = allNotes[i].start
		simulNotes = list()

		while i < len(allNotes) and abs(allNotes[i].start - curTime) < 1e-5:
			if mode == "closest":
				name = note_number_to_name(allNotes[i].pitch)
				pitch = allNotes[i].pitch
				simulNotes.append(str(pitch2note[min(pitch2note.keys(), key=lambda x: abs(x - pitch))]))
			elif mode == "ignore":
				name = note_number_to_name(allNotes[i].pitch)
				if name in table:
					simulNotes.append(str(table[name]))

			i += 1
			
		if len(simulNotes) > 1:
			seq.append(f"[{''.join(list(set(simulNotes)))}]")
		elif len(simulNotes) == 1:
			seq.append(simulNotes[0])

		if i < len(allNotes):
			waitTIme = allNotes[i].start - curTime
			if waitTIme > 0:
				seq.append(f"({waitTIme:.4f})")

	return " ".join(seq)
