#!/usr/bin/python3


import argparse
import json
import requests

def



def main(args):
	pass


if __name__ == '__main__':
	PARSER = argparse.ArgumentParser(description='what the fuck??')
	PARSER.add_argument('source', help='system leaving from')
	PARSER.add_argument('destination', help='where you are going', default='trade')
	ARGS = vars(PARSER.parse_args())
	main(ARGS)
