# Contributor handoff

## Catalog checkpoint · 2026-11-27

| Work | Last verified state | Next action |
| --- | --- | --- |
| Django starter | Published on `main` at [9a59cd7](https://github.com/notty-geek/django-product-catalog/commit/9a59cd7b0ae1745af03dd99ed7b41b7801778559). The README covers SQLite setup, the signing key, and admin login. | Use the README in the branch being tested. |
| Models, migration, and admin | [PR #1](https://github.com/notty-geek/django-product-catalog/pull/1) was open against `main` at this checkpoint. The feature branch is `codex/catalog-models`, at [b5c157c](https://github.com/notty-geek/django-product-catalog/commit/b5c157ce44329ebe5b9399ed546ae8bf2fb1328f). | The next reviewer should check the schema and deletion rules against the [implementation plan](implementation-plan.md). Check the live PR for changes or review feedback before continuing. |
| Sample data and search | The applicant owns admin data entry and the filtering queryset. Both depend on the catalog schema. | After the models are available, the applicant can populate the catalog. Before implementing search, settle the description match and whether multiple selected tags mean any or all. |

**Verification at the models commit.** The initial migration applied to SQLite, Django's system checks passed, and the migration drift check found no changes. Both relationship tests passed. Admin form submissions on a separate in-memory database accepted untagged and multi-tag products and rejected duplicate category and tag names. Those test submissions do not count toward the assignment's sample data.

## Passing work to the next contributor

Use this block in the relevant PR or task when transferring ownership. Update the checkpoint above when the project state it describes changes.

```markdown
**Task and owner** — Feature, outgoing owner, and next owner or role.
**Resume from** — Branch, commit, PR, and any prerequisite PR.
**Completed** — Observable behavior delivered and the decisions already confirmed.
**Verification** — Commands or manual checks, results, and the commit tested.
**Open issues** — Failing check, reproduction steps, or decision still needed.
**Next action** — First concrete step and how to tell when it is complete.
```
