#!/usr/bin/env python3

import argparse
from sys import exit
from os import linesep

parser = argparse.ArgumentParser(
                    prog='pfs-adjustments',
                    description='Sets PFS counters from CSV file',
                    epilog='Author: Alexey Bychko <abychko@gmail.com>')

parser.add_argument('-f', '--filename', required=True, help='CSV file to process')
parser.add_argument('-e', '--export', help='Output to SQL file', action='store_true')
parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag

args = parser.parse_args()
#
infile = None
outfile = None
outfile_name = args.filename.replace('.csv', '.sql')
sql_list = []
#
#
if args.verbose:
	print(f"CSV filename: {args.filename}")

if args.verbose:
	print(f"SQL filename: {outfile_name}")

try:
	infile = open(args.filename, 'r')
except Exception as err:
	print(f"==>> Wrong file or file path: {args.filename}!")
	print(f"{err}")
	exit(1)

for line in infile:
	if not '/' in line:
		continue
	name, enabled, timed = line.rstrip().split(',')
	sql_line = (f"UPDATE performance_schema.setup_instruments "
				f"SET ENABLED = '{enabled}', TIMED = '{timed}' "
				f"WHERE NAME = '{name}';")
	sql_list.append(sql_line)

if(args.verbose):
	for sql_line in sql_list:
		print(sql_line)

if args.export:
	try:
		outfile = open(outfile_name, 'w')
	except Exception as err:
		print(f"==>> Unable to open file: {outfile_name}!")
		print(f"{err}")
	for sql_line in sql_list:
		outfile.write(sql_line + linesep)
