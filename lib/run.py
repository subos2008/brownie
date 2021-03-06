#!/usr/bin/python3

from docopt import docopt
import importlib
import os
import sys

from lib.components.network import Network
from lib.services import color, config
CONFIG = config.CONFIG


__doc__ = """Usage: brownie run <filename> [<function>] [options]

Arguments:
  <filename>         The name of the script to run
  [<function>]       The function to call (default is main)

Options:
  --help             Display this message
  --network [name]   Use a specific network (default {})
  --verbose          Enable verbose reporting
  --tb               Show entire python traceback on exceptions

Use run to execute scripts that deploy or interact with contracts on the network.
""".format(CONFIG['network_defaults']['name'])

def main():
    args = docopt(__doc__)
    name = args['<filename>'].replace(".py", "")
    fn = args['<function>'] or "main"
    if not os.path.exists("scripts/{}.py".format(name)):
        sys.exit("{0[error]}ERROR{0}: Cannot find {0[module]}scripts/{1}.py{0}".format(color, name))
    Network(setup = True)
    module = importlib.import_module("scripts."+name)
    if not hasattr(module, fn):
        sys.exit("{0[error]}ERROR{0}: {0[module]}scripts/{1}.py{0} has no '{0[callable]}{2}{0}' function.".format(color, name, fn))
    print("Running '{0[module]}{1}{0}.{0[callable]}{2}{0}'...".format(color, name, fn))
    try:
        getattr(module, fn)()
        print("\n{0[success]}SUCCESS{0}: script '{0[module]}{1}{0}' completed.".format(color, name))      
    except Exception as e:
        if CONFIG['logging']['exc']>=2:
            print("\n"+color.format_tb(sys.exc_info()))
        print("\n{0[error]}ERROR{0}: Script '{0[module]}{1}{0}' failed from unhandled {2}: {3}".format(
            color, name, type(e).__name__, e
        ))