#!/usr/bin/env python3
"""Parse skip flags from commit messages.

Tags can be stacked — any combination works:
  [!backend]        skip all backend Rust jobs
  [!simulation]     skip backend-simulation
  [!matchgames]     skip backend-matchgames
  [!matchmaking]    skip backend-matchmaking
  [!admin-grpc]     skip backend-admin-grpc
  [!general]        skip backend-general
  [!godot]          skip all Godot export jobs
  [!roblox]         skip Game-Roblox tests + lint
  [!all]            skip everything
"""

import os
import sys

commits = (sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()).lower()

# Individual job flags
general      = "[!general]"      in commits
simulation   = "[!simulation]"   in commits
admin_grpc   = "[!admin-grpc]"   in commits
matchmaking  = "[!matchmaking]"  in commits
matchgames   = "[!matchgames]"   in commits
godot        = "[!godot]"        in commits
roblox       = "[!roblox]"       in commits

# Group flags (expanded below)
backend      = "[!backend]"      in commits
all_skip     = "[!all]"          in commits

# Expand group flags
if all_skip:
    general = simulation = admin_grpc = matchmaking = matchgames = godot = roblox = True
elif backend:
    general = simulation = admin_grpc = matchmaking = matchgames = True

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"skip_general={str(general).lower()}\n")
    f.write(f"skip_simulation={str(simulation).lower()}\n")
    f.write(f"skip_admin_grpc={str(admin_grpc).lower()}\n")
    f.write(f"skip_matchmaking={str(matchmaking).lower()}\n")
    f.write(f"skip_matchgames={str(matchgames).lower()}\n")
    f.write(f"skip_godot={str(godot).lower()}\n")
    f.write(f"skip_roblox={str(roblox).lower()}\n")
