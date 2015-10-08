from gi.repository import Gtk
from opengridview.window import Window
from gi.repository import GObject
import sys

windows = []

def window_closed(window):
    global windows
    windows.remove(window)
    if not windows:
        Gtk.main_quit()

def main():
    """Main entry point"""

    # Quit when interrupted
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Arguments:
    # --separator STRING/REGEX - how to split a row into cells (only relevant for CSV parser)
    # --flatten - flatten item hashes. {'a':{'b':'c'}} --> {'a_b':'c'}
    import argparse
    parser = argparse.ArgumentParser(description='View tabulated data via GUI')
    parser.add_argument('-p','--parser',type=str, default='autosplit',help='Type of parser to use') #TODO add possible parsers
    parser.add_argument('--headers',type=str, help='Headers are this comma-delimited names instead of ones supplied in file')
    parser.add_argument('--filter',type=str, help='Pre-populate filter box')
    parser.add_argument('-s', '--separator', help='How to seperate columns. Applies only to some parsers')
    parser.add_argument('files', nargs='*', help='Files to show. Each file opens a new window')
    args = parser.parse_args()

    GObject.threads_init()

    default_config = {'format': args.parser}
    if args.filter:
        default_config['filter']=args.filter
    if args.separator:
        default_config['separator']=args.separator
    if args.headers:
        default_config['headers']=map(lambda s: s.strip(),args.headers.split(','))
    inputs = [ (open(f,'r'),default_config) for f in args.files ]
    # Add stdin as input, if it's not a tty
    if not sys.stdin.isatty():
        inputs.append((sys.stdin, default_config))

    global windows
    windows = [Window(i[0],i[1]) for i in inputs]
    for win in windows:
      win.start_read()
      win.connect("destroy",window_closed)
    if windows:
        Gtk.main()
    else:
        print 'No input supplied so no windows are created'
