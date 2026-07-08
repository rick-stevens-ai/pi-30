#!/usr/bin/env python3
# Minimal `setsid` for macOS: fork, become session leader (os.setsid), exec argv.
# This detaches the child into its OWN session + process group, so a SIGTERM to the
# launcher's group does NOT cascade to it. Usage: setsid_shim.py <cmd> [args...]
import os, sys
if len(sys.argv) < 2:
    sys.stderr.write("usage: setsid_shim.py <cmd> [args...]\n"); sys.exit(2)
pid = os.fork()
if pid > 0:
    os._exit(0)          # parent returns immediately
os.setsid()             # child becomes session leader (new SID + PGID)
try:
    os.execvp(sys.argv[1], sys.argv[1:])
except FileNotFoundError:
    sys.stderr.write("setsid_shim: command not found: %s\n" % sys.argv[1]); os._exit(127)
