# git-tidy

I wrote this utility to save myself some repetitive typing, because I often come
back to a repo after a while of not using it, and in the meanwhile a remote may
have moved on or I'm not sure what state it's in.

So this gets it cleaned up relatively quickly.

It's more or less the equivalent of

```bash
git checkout main
git fetch --all --purge  # purge is to delete unnecessary remote refs
git merge origin/main main --ff-only
git branch --merged | grep -v main | xargs git branch -d
```

with some extra convenience and (I hope) safety features.
