# Working on the product catalog

This repository is a Django take-home assignment. Start with the user's ticket, check the current branch and open PRs, and use the [README](README.md) for local setup. The [implementation plan](docs/implementation-plan.md) records the assignment requirements. The [handoff](docs/handoff.md) identifies work in flight.

## Scope and ownership

- Implement the explicit requirements and confirmed decisions. If a material choice is open, explain the proposed change and its tradeoffs and wait for the user's decision. Read-only investigation can continue. Carry out an approved change without seeking the same approval again.
- Apply that rule to behavior, architecture, dependencies, configuration, infrastructure, permissions, monitoring, and unrelated refactoring. A request for production quality does not grant blanket approval for these changes.
- Respect the applicant's ownership of the assignment. The applicant enters the sample records through Django admin and owns the filtering queryset. Keep the README attribution accurate about who designed, wrote, and verified each AI-assisted feature.

## Coordinate concurrent work

1. Name the owner, affected files, acceptance criteria, and dependencies for each task. Agree on shared interfaces before two agents build against them. For the search form, the view and template must agree on parameter names and how selected tags are interpreted.
2. Give concurrent writers separate feature branches and worktrees or clones. Check `git status --short --branch` and `git worktree list` before editing. Preserve another contributor's uncommitted work. Coordinate overlapping changes to models, migrations, or shared tests with the owner. [Git worktree guide](https://git-scm.com/docs/git-worktree)
3. Branch independent work from current `main`. When work requires an unmerged change, record the prerequisite PR and commit in the handoff. Before integration, check what actually merged and rerun the affected tests on the combined changes.
4. When ownership changes, record the last verified commit, what passed or failed, and the next action. Keep the details for a single feature in its PR and link to them from the handoff.

## Verify and review

With the virtual environment active and `DJANGO_SECRET_KEY` set as documented in the README, run the checks relevant to the change from the project root.

```sh
python manage.py check
python manage.py test catalog
python manage.py makemigrations --check --dry-run
```

For schema changes, include the generated migration, apply it to a disposable SQLite database, and exercise the affected admin or application path. Preserve the applicant's local sample database. For documentation changes, check paths, commands, and referenced PRs. Keep credentials and local databases out of commits and handoffs.

Open one focused PR per feature. Describe the user-visible change, why it was made, how it was tested, and any unresolved decision. The reviewer compares the diff with the ticket, checks edge cases, and reports findings against the reviewed commit. Resolve findings before merge. If the request is to open a PR for review, leave it open.
