#!/usr/bin/env python3
"""Parse skip flags from commit messages.

Tags can be stacked — any combination works:
  [backend-skip]      -> skip all backend Rust jobs
  [simulation-skip]   -> skip backend-simulation job
  [matchgames-skip]   -> skip backend-matchgames job
  [matchmaking-skip]  -> skip backend-matchmaking job
  [admin-grpc-skip]   -> skip backend-admin-grpc job
  [general-skip]      -> skip backend-general job
  [godot-skip]        -> skip all Godot export jobs
"""

import os
import sys

commits = (sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()).lower()

skip_backend = "[backend-skip]" in commits
skip_general = "[general-skip]" in commits
skip_simulation = "[simulation-skip]" in commits
skip_admin_grpc = "[admin-grpc-skip]" in commits
skip_matchmaking = "[matchmaking-skip]" in commits
skip_matchgames = "[matchgames-skip]" in commits
skip_godot = "[godot-skip]" in commits

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"skip_backend={str(skip_backend).lower()}\n")
    f.write(f"skip_general={str(skip_general).lower()}\n")
    f.write(f"skip_simulation={str(skip_simulation).lower()}\n")
    f.write(f"skip_admin_grpc={str(skip_admin_grpc).lower()}\n")
    f.write(f"skip_matchmaking={str(skip_matchmaking).lower()}\n")
    f.write(f"skip_matchgames={str(skip_matchgames).lower()}\n")
    f.write(f"skip_godot={str(skip_godot).lower()}\n")
