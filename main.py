import argparse

from player import play
from constructor import construct

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument("file", nargs="?", help="Path to input MIDI (.mid) file")
	parser.add_argument("--mode", choices=["ignore", "closest"], default="closest", help="Handler for notes not present in mapping table")
	parser.add_argument("--table", help="Path to note mapping table file")
	parser.add_argument("--seq", help="Use a pre-generated sequence")
	parser.add_argument("--seqfile", help="Path to output sequence (.seq) file")
	parser.add_argument("--silent", action="store_true", help="Disable genereated sequence print")

	args = parser.parse_args()

	if args.seq:
		seq = args.seq
	else:
		if not args.file or not args.table:
			parser.error("file and --table are required when --seq is not provided")
		seq = construct(args.file, args.table, args.mode)

	if not args.silent:
		print(f"generated sequence: {seq}")

	if args.seqfile:
		with open(args.seqfile, "w") as f:
			f.write(seq)
			f.close()
		
	play(seq)

if __name__ == "__main__":
	main()
