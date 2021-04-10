import os, sys, argparse

parser = argparse.ArgumentParser(prog='wc', add_help=False)
parser.add_argument('-w','--words',action='store_true')
parser.add_argument('-l','--lines',action='store_true')
parser.add_argument('-c','--bytes',action='store_true')
parser.add_argument('-m','--chars',action='store_true')
parser.add_argument('-L','--max-line-length',action='store_true')
parser.add_argument('-v','--version',action='version',version='%(prog)s 1.1.2')
parser.add_argument('-h','--help', action='store_true')
parser.add_argument('files',nargs='*')
parser.add_argument('--files0-from')
parser = parser.parse_known_intermixed_args()
args = vars(parser[0])
wrongs = parser[1]
def usage():
    usage = """Usage: wc [OPTION]... [FILE]...
  or:  wc [OPTION]... --files0-from=F
Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.  A word is a non-zero-length sequence of
characters delimited by white space.

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in
the following order: newline, word, character, byte, maximum line length.
  -c, --bytes            print the byte counts
  -m, --chars            print the character counts
  -l, --lines            print the newline counts
      --files0-from=F    read input from the files specified by
                           \\n separated names in file F;
                           If F is - then read names from standard input
  -w, --words            print the word counts
      --help     display this help and exit
      --version  output version information and exit"""
    print(usage)
if args['help']:
    usage()
    sys.exit()
if not wrongs:
    def wc(files):
        opts = True
        nl = '\n'
        tab = '\t'
        output = ''
        tot_lines = 0
        tot_words = 0
        tot_chars = 0
        tot_bytes = 0
        if (not args['lines'] and not args['words'] and not args['bytes'] and not args['chars']):
            opts = False
        for f in files:
            try:
                with open(f,'r') as f:
                    content = f.read()
                    output += f"{tab + str(len(content.split(nl)) -1) if not opts else ''}" # -1 for empty files
                    output += f"{tab + str(len(content.split())) if not opts else ''}"
                    output += f"{tab + str(os.path.getsize(f.name)) if not opts else ''}"
                    # if option\s used
                    output += f"{tab + str(len(content.split(nl)) -1) if args['lines'] else ''}"
                    output += f"{tab + str(len(content.split())) if args['words'] else ''}"
                    output += f"{tab + str(os.path.getsize(f.name)) if args['bytes'] else ''}"
                    output += f"{tab + str(len(content)) if args['chars'] else ''}"
                    # totals if more than one file passed
                    tot_lines += len(content.split(nl)) -1
                    tot_words += len(content.split())
                    tot_bytes += os.path.getsize(f.name)
                    tot_chars += len(content)
                output += f'\t{f.name}\n'
            except FileNotFoundError as err:
                output += f'wc.py: {err.filename}: No such file or directory\n'
            except PermissionError as err:
                output += f'wc.py: {err.filename}: Permission Denied\n'
        if len(files) > 1:
            output += f"{tab + str(tot_lines) if not opts or args['lines'] else ''}"
            output += f"{tab + str(tot_words) if not opts or args['words'] else ''}"
            output += f"{tab + str(tot_bytes) if not opts or args['bytes'] else ''}"
            output += f"{tab + str(tot_chars) if args['chars'] else ''}"
            output+= '\ttotal '
        return output[:-1]

    def files():
        files = []
        if args['files']:
            files = args['files']
        elif args['files0_from']:
            if args['files0_from'] != '-':
                with open(args['files0_from'],'r') as f:
                    files = f.read().split('\n')
            else:
                for f in sys.stdin:
                    files.append(f.replace('\n',''))
        else:
            for f in sys.stdin:
                files.append(f.replace('\n',''))
        return files
    print(wc(files()))         

else: # wrong opt\ss used
    if '-L' in wrongs:
        print('wc.py: Sorry, we don\'t support  \'-L\' yet\n')
    res = ''
    bs = '\''
    print(f"wc.py: invalid option -- {','.join(bs+x.strip('-')+bs for x in wrongs)}\nTry 'wc.py --help' for more information.")
    sys.exit()


    
