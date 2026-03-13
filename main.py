import argparse

from player import play
from constructor import construct

def main():
	parser = argparse.ArgumentParser()

	# examples:
	# py main.py --silent --table tales/jjs_simple_piano.json --mode ignore midi/honored1.mid
	# py main.py --table tales/jjs_advanced_piano.json --mode closest midi/hide2.mid
	# py main.py --seq sequences/jjs_advanced_piano/flight_of_the_crows.seq
	parser.add_argument("file", nargs="?", help="Path to input file")
	parser.add_argument("--mode", choices=["ignore", "closest"], default="closest", help="Handler for notes not present in mapping table")
	parser.add_argument("--table", help="Path to note mapping table file")
	parser.add_argument("--seq", action="store_true", help="Use a pre-generated sequence file instead of a MIDI file")
	parser.add_argument("--seqfile", help="Path to output sequence (.seq) file")
	parser.add_argument("--silent", action="store_true", help="Disable genereated sequence print")

	args = parser.parse_args()

	if args.seq:
		with open(args.file, "r") as f:
			seq = f.read()
			f.close()
	else:
		if not args.file or not args.table:
			parser.error("file and --table are required when --seq is not provided")
		seq = construct(args.file, args.table, args.mode)

	if not args.silent or not args.seq:
		print(f"generated sequence: {seq}", flush=True)

	if args.seqfile:
		with open(args.seqfile, "w") as f:
			f.write(seq)
			f.close()
		
	play(seq)

if __name__ == "__main__":
	main()
