# git-tidy

Have you ever come back to a git repo after a while, started developing, and
then realised you weren't on the main branch, or your branch was missing the
latest changes, so you ended up with merge conflicts?

Or have you ever finished working on a feature, completed a pull-request online,
and wanted an easy way to clean up your local repo from all the unused
references that have accumulated themselves?

Then `git-tidy` is for you!

This is a simple Python script which you can install by copying (or symlinking)
anywhere on your path (I recommend ~/bin/, but something like /usr/local/bin/
would also work).

Entering
```bash
git tidy
```
at the terminal will:
- Check out the default branch, usually `main`
  -  if this is not configured, it will try to figure out what it should be,
- Pull to make sure that you're up-to-date with the default branch,
- Delete all branches that have already been merged into the default, and,
- Delete all references which have been removed from the remote as well,

leaving you with a pristine, tidy repository in order to continue your
development.
