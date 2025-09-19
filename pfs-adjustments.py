#!/usr/bin/env python3

import argparse
from sys import exit
from os import linesep

parser = argparse.ArgumentParser(
                    prog='pfs-adjustments',
                    description='Sets PFS counters from CSV file',
                    epilog='Author: Alexey Bychko <abychko@gmail.com>')

parser.add_argument('--filename', required=True, help='CSV file to process')
parser.add_argument('--output', help='Output to file', action='store_true')
parser.add_argument('--output-format', choices=['sql', 'cnf'], help="Output format. SQL or my.cnf snippet")
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()
#
infile = None
outfile = None
outfile_name = None
lines = []
#
def gen_sql_file(ifile=None, ofile=None):
	if args.verbose:
		print(f"SQL filename: {outfile_name}")
	for line in ifile:
		if not '/' in line:
			continue
		name, enabled, timed = line.rstrip().split(',')
		sql_line = (f"UPDATE performance_schema.setup_instruments "
				f"SET ENABLED = '{enabled}', TIMED = '{timed}' "
				f"WHERE NAME = '{name}';")
		lines.append(sql_line)
	for sql_line in lines:
		if(args.verbose):
			print(sql_line)
		ofile.write(sql_line + linesep)
#
def gen_cnf_file(ifile=None, ofile=None):
	if args.verbose:
		print(f"MySQL cnf filename: {outfile_name}")

	ofile.write("performance_schema_instrument = '%=OFF'" + linesep)

	for line in ifile:
		if not '/' in line:
			continue
		name, enabled, _ = line.rstrip().split(',')

		if enabled == "YES":
			cnf_line = f"performance_schema_instrument = '{name}=ON'"
			lines.append(cnf_line)

	for line in sorted(lines):
		if(args.verbose):
			print(line)
		ofile.write(line + linesep)
#
def open_outfile(name=None):
	try:
		f = open(outfile_name, 'w')
	except Exception as err:
		print(f"==>> Unable to open file: {outfile_name}!")
		print(f"{err}")
	return f

try:
	infile = open(args.filename, 'r')
except Exception as err:
	print(f"==>> Wrong file or file path: {args.filename}!")
	print(f"{err}")
	exit(1)

if args.verbose:
	print(f"CSV filename: {args.filename}")

if args.output_format == 'sql':
	outfile_name = args.filename.replace('.csv', '.sql')
	outfile = open_outfile(outfile_name)
	gen_sql_file(infile, outfile)

if args.output_format == 'cnf':
	outfile_name = "perfschema.cnf"
	outfile = open_outfile(outfile_name)
	gen_cnf_file(infile, outfile)















