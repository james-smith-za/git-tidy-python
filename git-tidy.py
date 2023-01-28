#!/usr/bin/env python

# git-tidy is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# git-tidy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

# You should have received a copy of the GNU General Public License along with git-tidy. If not, see
# <https://www.gnu.org/licenses/>.
"""git-tidy module."""

import subprocess
import sys
from typing import List, Tuple, Union

common_default_branches = [
    "main",
    "master",
    "devel",
    "dev",
]


def run(command: Union[List[str], str]) -> Tuple[int, str]:
    """Run a subprocess.

    The subprocess is checked for whether it returns successfully, and its
    stdout or stderr is captured for the caller to make use of.

    Parameters
    ----------
    command
        The command to run as a subprocess.

    Returns
    -------
    returncode
        The (integer) return code from the completed subprocess.
    stdout / stderr
        In the case of a zero return code, the stdout from the subprocess is
        returned. In all other cases, the stderr is returned. In both cases,
        the bytes are converted to str and stripped of whitespace on either
        side.
    """
    try:
        process = subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as exception:
        return exception.returncode, exception.stderr.decode().strip()

    return process.returncode, process.stdout.decode().strip()


def get_default_branch() -> str:
    """Return the name of the repo's default branch."""
    returncode, configured_default_branch = run(["git", "config", "--get", "--local", "tidy.defaultbranch"])
    if returncode == 128:
        # The --local flag caused this to fail because we're not in a git repository.
        print(configured_default_branch, file=sys.stderr)
        sys.exit(returncode)

    # If we're in a repository, we need a list of branches, either as a
    # sanity check that the configured branch is there, or to choose one
    # if it's not configured.
    _, branch_list_raw = run(["git", "branch", "--list"])
    branch_list = [
        branch.strip("*").strip()  # Remove the indicator of current branch.
        for branch in branch_list_raw.split("\n")
        if len(branch)  # Ignore empty lines.
    ]

    if returncode == 0:  # The config entry was successfully returned.
        # But it's worth checking that the branch exists nonetheless.
        if configured_default_branch in branch_list:
            return configured_default_branch

        print(
            f"{configured_default_branch} configured as defauly branch for tidying purposes, but it doesn't exist!",
            file=sys.stderr,
        )
        # TODO: There is probably a clean way to fix this.
        sys.exit(-1)

    print("No default branch for git-tidy configured, will try to figure out which to use...")

    candidates = []

    # Check whether any branches match our list of common defaults.
    for branch in branch_list:
        if branch in common_default_branches:
            candidates.append(branch)

    if len(candidates) == 1:
        # Only one branch name matches, so we'll go with that one.
        run(["git", "config", "--add", "tidy.defaultbranch", candidates[0]])
        return candidates[0]

    if len(candidates) == 0:
        print("No candidate branches!", file=sys.stderr)
        sys.exit(-1)

    # If we don't have one or zero, which do we have?
    selection = -1
    while (selection < 0) or (selection >= len(candidates)):
        print(
            f"{'Several' if len(candidates) > 1 else 'No'}  potential default branch candidates found. "
            "Please select one:"
        )
        for n, candidate in enumerate(candidates):
            print(f"{n}: {candidate}")

        # TODO: This breaks if the user is stupid and doesn't input an int.
        selection = int(input("Which to choose?"))

    return candidates[selection]


if __name__ == "__main__":

    default_branch = get_default_branch()
    print(f"Switching to {default_branch}")
    run(["git", "checkout", default_branch])

    # Check which remote it's configured with.
    _, remote = run(["git", "config", "--get", f"branch.{default_branch}.remote"])

    print(f"{default_branch} is configured for remote {remote}")

    # Get latest changes from remote, clear up unnecessary stuff.
    run(["git", "fetch", "--all", "--prune"])
    run(
        ["git", "merge", "--ff-only", f"{remote}/{default_branch}", default_branch]
    )  # TODO: Handle what happens if the ff fails.

    # Check which branches are `--merged` and clean them up.
    _, merged_branches_raw = run(["git", "branch", "--merged"])
    merged_branches = [
        branch for branch in merged_branches_raw.split("\n") if len(branch)  # Remove zero-length elements.
    ]
    for branch in merged_branches:
        if branch[0] != "*":  # This time we want to explicitly exclude the checked-out branch.
            subprocess.run(["git", "branch", "-d", branch.strip()], check=True)
