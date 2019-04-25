# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# Built from https://github.com/Goom11/vscode-python and https://github.com/Goom11/ptvsd

import os
import os.path
import sys
import traceback

# TODO(goom): Instead of calling vspd.debug directly, call either ptvsd_launcher.py or ptvsd/__main__.py
def load(main_module):
    try:
        ptvs_lib_path = os.path.join(os.path.dirname(__file__), 'ptvsd')
        sys.path.append(ptvs_lib_path)
        try:
            import ptvsd
            import ptvsd.debugger as vspd
            from ptvsd.__main__ import main
            ptvsd_loaded = True
        except ImportError:
            ptvsd_loaded = False
            raise
        vspd.DONT_DEBUG.append(os.path.normcase(__file__))
    except:
        traceback.print_exc()
        print('''
    Internal error detected. Please copy the above traceback and report it.

    Press Enter to close. . .''')
        try:
            raw_input()
        except NameError:
            input()
        sys.exit(1)
    finally:
        if ptvs_lib_path:
            sys.path.remove(ptvs_lib_path)

    # For some reason, sys.path gets modified and we need to preserve sys.path[0]
    sys.path.insert(0, sys.path[0])

    # Fetch port_num from sys.argv
    port_num = sys.argv[6]
    run_as = "module"
    # Clear not run arguments
    sys.argv[1:8] = []
    # return [launcher, ...additionalPtvsdArgs, '--client', '--host', 'localhost', '--port', debugPort.toString()];
    # Reinsert args in the order expected by main
    sys.argv[1:1] = ['--client', '--host', 'localhost', '--port', port_num, '-m', main_module]

    main(sys.argv)
