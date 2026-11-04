# Automated release guard (Beta)

`Generate Config Files` continues to run on the existing daily cron and main pushes; it commits only after all checks succeed. No day-to-day manual approval is needed for normal upstream-rule refreshes.

The guard checks:

- Required Mihomo, Stash, Loon and Surge outputs are present and not empty.
- Both public Egern configurations contain **only** `https://example.invalid/REPLACE_WITH_YOUR_EGERN_SUBSCRIPTION`; exactly 29 distinct groups, 30 remote rules, final default, and correct IPv6 flags.
- All existing `Rules/Egern/*.yaml` remain present and parseable.
- Per-file Egern rule counts never fall below 50% of checked-in HEAD; the total Egern rule count never falls below 70% of HEAD. This is an anomaly tripwire, not a guarantee of rule semantics.

If a check fails, GitHub Actions stops **before** `git add` / `git push`, leaving the published configuration unchanged. Review the failure in the run log before changing a threshold. Large intentional rule removals should be reviewed as code changes in a PR.

## Limitations

- This guard does not yet prove semantics across all five clients or check every potentially sensitive value in all files.
- If upstream content changes but its size stays normal, other semantic defects may still pass. Parser and client-level tests remain important.
- If updaters produce the same regenerated files as HEAD, no new commit is needed.
- Branch protection / mandatory PR approvals are controlled in GitHub repository settings, not by this script.

## Local checks

```bash
uv run --with pyyaml python scripts/test_release_guard.py
uv run --with pyyaml python scripts/validate_release_guard.py
```

For a reproducible release rehearsal, first run the existing generator and Egern template publisher using the public placeholder, then run the guard.
