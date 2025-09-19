#!/usr/bin/env python3

from argparse import ArgumentParser
from sys import exit
from os import linesep
from datetime import datetime

parser = ArgumentParser(
                    prog='pfs-adjustments',
                    description='Sets PFS counters from CSV file',
                    epilog='Author: Alexey Bychko <abychko@gmail.com>')

parser.add_argument('--infile', required=True, help='CSV file to process')
parser.add_argument('--format', choices=['sql', 'cnf'], required=True,
						help="Output format. SQL or my.cnf snippet")
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()
#
lines = []
#
def create_cnf_file(infile=None, outfile=None):
	for line in infile:
		if not '/' in line:
			continue

		name, enabled, _ = line.rstrip().split(',')

		if enabled == "YES":
			cnf_line = f"performance_schema_instrument = '{name}=ON'"
			lines.append(cnf_line)
#
def create_sql_file(infile=None, outFile=None):
	for line in infile:
		if not '/' in line:
			continue
		name, enabled, timed = line.rstrip().split(',')
		sql_line = (f"UPDATE performance_schema.setup_instruments "
				f"SET ENABLED = '{enabled}', TIMED = '{timed}' "
				f"WHERE NAME = '{name}';")
		lines.append(sql_line)
#
def create_outfile():
	now = datetime.now()
	date_time = now.strftime("%Y-%m-%d %H:%M:%S")

	o_filename = "perfschema." + args.format
	print(f"=> Creating outfile: {o_filename}")
# open file
	try:
		infile = open(args.infile, 'r')
	except Exception as err:
		print(f"==>> Wrong file or file path: {args.infile}!")
		print(f"{err}")
		exit(1)
#
	try:
		outfile = open(o_filename, 'w')
	except Exception as err:
		print(f"==>> Unable to open outfile: {o_filename}!")
		print(f"{err}")
#
	if args.verbose:
		print(f"=> CSV filename: {args.infile}")
		print(f"=> Output format is {args.format.upper()}")
		print(f"=> Outfile is {o_filename}")
#
	if args.format == 'sql':
		lines.append("--" + linesep + "-- PFS Adjuster " +
			date_time + linesep + "--")
		create_sql_file(infile, outfile)
#
	if args.format == 'cnf':
		lines.append("#" + linesep + "## PFS Adjuster " + date_time +
			linesep + "#" + linesep + "[mysqld]")
		lines.append("performance_schema_instrument = '%=OFF'")
		create_cnf_file(infile, outfile)
#
	for line in sorted(lines):
		if(args.verbose):
			print(line)
		outfile.write(line + linesep)
#
#
create_outfile()
















