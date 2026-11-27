# Catalog implementation plan

Use the acceptance criteria below to plan a feature and review its PR. Check the [handoff](handoff.md) for branch and review status before taking ownership.

| Deliverable | Decisions and dependencies | Acceptance evidence |
| --- | --- | --- |
| Models and admin | A product has a required name, description, and category. Tags are optional and shared. Category and tag names are unique within their respective tables. | Migrate a fresh SQLite database. Save products with zero and multiple tags in admin. Verify that a category in use is protected and deleting a tag preserves its products. |
| Sample catalog | Codex entered the sample records through Django admin and exported them as a fixture. The applicant reviewed this work as part of the [AI-assisted implementation](../README.md#ai-attribution). | On a fresh database, run `python manage.py migrate`, then `python manage.py loaddata sample_catalog`. Verify that the catalog contains 5 categories, 10 tags, and 20 products. |
| Search and filters | Match the trimmed search text as a case-insensitive substring of the description, combine the active filters, and require every selected tag. | Check description, category, and tags independently and together. Include an empty result and a product with multiple matching tags. Check that each matching product appears once. |
| HTML page and submission | The form and view use the same query parameters. Document the page URL, filter behavior, setup steps, and AI contributions in the README. | From a fresh checkout, follow the README, load the sample data, and submit a combined search in the browser. Verify that the review link points to the public repository. |

## Planning a feature

For work shared across agents, put these details in the ticket or PR description. For a small change, a few lines suffice.

- **Outcome and owner** — Describe what the user can do when the feature is complete and who owns the change.
- **Interfaces and dependencies** — Identify files or contracts shared with another contributor, the prerequisite branch or PR, and any decision awaiting the user.
- **Implementation** — Outline the smallest change that satisfies the confirmed behavior. For a schema change, describe its effect on existing records.
- **Verification** — Give a reproducible check and its expected result. After implementation, record the actual result and the commit tested.
