"""Claim a batch from data/batches.csv so parallel Claude sessions never work on the same one.

Run from the repo root:  python3 -I data/claim_batch.py        (next free batch)
                         python3 -I data/claim_batch.py 7      (batch 7 only)

A batch is free when origin has no productlist-N branch and its review folders aren't on origin/main yet.
Claiming pushes productlist-N as one empty "Start batch N" commit on top of origin/main (unique per session), with a
lease that only succeeds if the branch doesn't exist yet, so if two sessions race for the same batch exactly one wins;
the loser moves on to the next one.
Release an abandoned claim that has no commits with:  git push origin --delete productlist-N
"""
import csv
import subprocess
import sys
import uuid


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r


git("fetch", "origin", "--prune", "--quiet")
main_sha = git("rev-parse", "origin/main").stdout.strip()
taken = {line.split("refs/heads/")[1] for line in
         git("ls-remote", "--heads", "origin", "productlist-*").stdout.splitlines()}
on_main = set(git("ls-tree", "--name-only", "origin/main").stdout.split())

batches = list(csv.DictReader(open("data/batches.csv", encoding="utf-8-sig")))
slugs = {b["branch"]: [b[f"slug_{i}"] for i in (1, 2, 3) if b[f"slug_{i}"]] for b in batches}
wanted = sys.argv[1] if len(sys.argv) > 1 else None
if wanted:
    batches = [b for b in batches if b["batch"] == wanted]
    if not batches:
        sys.exit(f"No batch {wanted} in data/batches.csv")

for b in batches:
    branch = b["branch"]
    done = all(s in on_main for s in slugs[branch])
    if branch in taken or done:
        if wanted:
            sys.exit(f"Batch {wanted} is not free ({'already on main' if done else 'branch exists on origin'}).")
        continue
    names = ", ".join(b[f"product_{i}"] for i in (1, 2, 3) if b[f"product_{i}"])
    msg = f"Start batch {b['batch']}: {names}\n\nClaim {uuid.uuid4().hex[:12]}"
    claim = git("commit-tree", f"{main_sha}^{{tree}}", "-p", main_sha, "-m", msg).stdout.strip()
    r = git("push", "--quiet", f"--force-with-lease=refs/heads/{branch}:", "origin",
            f"{claim}:refs/heads/{branch}", check=False)
    if r.returncode:  # another session claimed it a moment ago
        if wanted:
            sys.exit(f"Batch {wanted} was just claimed by another session.")
        continue
    print(f"CLAIMED batch {b['batch']}: {branch} (from origin/main {main_sha[:7]})")
    for i in (1, 2, 3):
        if b[f"product_{i}"]:
            print(f"  {i}. {b[f'product_{i}']}  ->  {b[f'slug_{i}']}/")
    if b["notes"]:
        print(f"  notes: {b['notes']}")
    print(f"\nNext: git worktree add ../truepicks-worktrees/{branch} {branch}   (if this checkout is shared)")
    print(f"      or: git switch {branch}   (after git fetch, if this session has its own worktree)")
    sys.exit(0)

sys.exit("No free batch left.")
