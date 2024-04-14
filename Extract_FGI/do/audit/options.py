#!/usr/bin/env python
import argparse
from audit import __version__

class  Options():
	__args = None

	def args(self):
		return self.__args

	def __init__(self, argv):
		parser = argparse.ArgumentParser(prog=f'SSCParser {__version__}',
						usage='main [options] args',
						description='flags malicious/risky open-source packages')
		subparsers = parser.add_subparsers(title='actions', dest='cmd', help='Command (e.g.audit-online, audit-offline)')

		parser.add_argument('-v', '--version', help='Dump tool version', dest="ver", action='store_true')

		#############################
		# Audit-online sub-command
		#############################
		parser_audit_online = subparsers.add_parser('audit-online', help='Audit packages for malware/risky attributes')

		# Audit-online optional args
		parser_audit_online.add_argument("-t", "--trace", dest="trace", \
				help="Install package(s) and collect dynamic/runtime traces", action="store_true")

		# Audit-online positional args
		parser_audit_online_group = parser_audit_online.add_argument_group(title='required arguments', description='--packages must be chosen.')
		parser_audit_online_arg = parser_audit_online_group.add_mutually_exclusive_group(required=True)
		parser_audit_online_arg.add_argument('-p', '--packages', nargs='+', help='Audit-online packages (e.g., npm:react, pypi:torch), optionally version (e.g., rubygems:overcommit:1.0)', action='store', default=[])

		#############################
		# Audit-offline sub-command
		#############################
		parser_audit_offline = subparsers.add_parser('audit-offline', help='Audit packages for malware/risky attributes')

		# Audit-offline optional args
		parser_audit_offline.add_argument("-t", "--trace", dest="trace", \
				help="Install package(s) and collect dynamic/runtime traces", action="store_true")

		# Audit-offline positional args
		parser_audit_offline_group = parser_audit_offline.add_argument_group(title='required arguments', description='--packages must be chosen.')
		parser_audit_offline_arg = parser_audit_offline_group.add_mutually_exclusive_group(required=True)
		parser_audit_offline_arg.add_argument('-p', '--packages', nargs='+', help='Audit-offline packages (e.g., npm:C:\desktop\ABC), optionally version ', action='store', default=[])

		# parse args now
		self.__args = parser.parse_args(argv)

