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
def get_cf_line(name=None, enabled=None, timed=None) -> str:
	cnf_line = None

	if args.format == 'cnf':
		if enabled == "YES":
			cnf_line = f"performance_schema_instrument = '{name}=ON'"

	if args.format == 'sql':
		cnf_line = (f"UPDATE performance_schema.setup_instruments "
					f"SET ENABLED = '{enabled}', TIMED = '{timed}' "
					f"WHERE NAME = '{name}';")

	return cnf_line
#
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")

o_filename = "perfschema." + args.format
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

#
if args.format == 'cnf':
	lines.append("#" + linesep + "## PFS Adjuster " + date_time +
								linesep + "#" + linesep + "[mysqld]")
	lines.append("performance_schema_instrument = '%=OFF'")
#
for line in infile:
	name, enabled, timed = line.rstrip().split(',')
	if name == 'NAME':
		continue
	res = get_cf_line(name, enabled, timed)
	if res != None:
		lines.append(res)
#
for line in lines:
	if args.verbose:
		print(line)
	outfile.write(line + linesep)
#

