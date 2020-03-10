import argparse

import gspnlib.parser
import gspnlib.latex

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate tikz file visualizing the given GSPN.')

    parser.add_argument('--gspn', '-i', help='The path for the gspn file in PNPRO format', required=True)
    parser.add_argument('--out', '-o', help='The path for the generated tikz file', required=True)
    args = parser.parse_args()

    # Read GSPN file
    print("Reading {}".format(args.gspn))
    gspn = gspnlib.parser.parse_gspn(args.gspn)
    print(gspn)

    # Generate tikz file
    gspnlib.latex.generate_tikz(gspn, args.out)
