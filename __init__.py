#!/usr/bin/env python3

import logging # get rid of warnings from scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import argparse	 # parse the arguments from the command line
import sys # iterate through the command line arguments
import traceManipulation # manipulator for the trace

if __name__ == "__main__":
	''' initialize the argparser '''
	parser = argparse.ArgumentParser(description='The program executes one or more of the manipulations in the order given on the command line. In addition to the outputfile a textfile is generated to trace the changes. ', epilog='written by Benedikt Ferling<benedikt.ferling@wwu.de>')
	parser.add_argument("-t", dest="trace", metavar="INNPUTFILE", required=True, help='Trace on which the operation is executed')
	parser.add_argument("-C", dest="clone", metavar="CLONE", required=False, help='Clone random packets')	
	parser.add_argument("-R", dest="remove", metavar="REMOVE", required=False, help='Remove random packets')
	parser.add_argument("-S", dest="swap", metavar="SWAP", required=False, help="Swap random packet-pairs")
	parser.add_argument("-r", dest="rules", default="rules.txt", metavar="RULES", required=False, help="file with rules for the changes")
	parser.add_argument("-o", dest="output", default="output_trace.pcap", metavar="OUTPUTFILE", required=False, help="Outputfile")

	args = parser.parse_args()
	
	if args.trace and args.output:	
		''' iterate through the args and execute them in order of declaration on the command line '''
		manipulator = traceManipulation.TraceManipulator(args.trace, args.output)
		
		for param in sys.argv:
			if param == "-R":
				manipulator.removeRandomPackets(int(args.remove))
			if param == "-C":
				manipulator.cloneRandomPackets(int(args.clone))
			if param == "-S":
				manipulator.swapRandomPackets(int(args.swap))
			if param == "-r":
				manipulator.executeRulesFromFile(args.rules)
			
		manipulator.write(args.output)
		
	else:
		parser.print_help()
		exit(1)
	
	exit(0)

exit(2)
