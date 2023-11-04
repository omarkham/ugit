import argparse
import os
import sys

from . import base
from . import data

def main():
    args = parse_args() #parse the command-line arguments
    args.func(args) #call the corresponding function based on the subcommand
    
def parse_args(): #Define the command-line argument parser
    parser = argparse.ArgumentParser()
    
    commands = parser.add_subparsers(dest='command') #Create a subparser to handle different subcommands
    commands.required = True #Make it required to specify a subcommand

    init_parser = commands.add_parser('init') #Define a subcommand called "init"
    init_parser.set_defaults(func=init) #Set the default function to be called when the "init" subcommand is used
    
    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')
    
    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object')
    
    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)
    
    return parser.parse_args() #Parse the command-line arguments and return the result


def init(args): #Function to be called when the "init" subcommand is used
    data.init()
    print(f'Initialized empty ugit repository in {os.getcwd()}/{data.GIT_DIR}')
    
def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))
        
def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))
    
def write_tree(args):
    base.write_tree()