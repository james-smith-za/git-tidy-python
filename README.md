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

The repo is named with `-python` on the end because I have a vague ambition to
redo this program in Go at some point, which will make it easier to distribute
for people who don't have Python installed by default (i.e. Windows users). But
I'm not sure when I'll get to that.


## TODO

I'd like to actually get a set of unit-tests in place, but I'm not sure how to
go about this really because there's a lot of subprocess calls. If anyone reads
this and has an idea, I'd be glad to hear from you.
