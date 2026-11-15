# Recent-object discovery by metadata and content

Use this workflow when the researcher refers to a recent, latest, or
just-created EDSL object without a UUID or reliable description. The aim is to
identify the object, not to import every recent object into the study.

## 1. Prefer exact current-session evidence

If the current conversation already produced or selected one matching local
path, UUID, or Expected Parrot URL, use that evidence. Do not infer a match only
because a `chat_summary.md` file exists, and do not search the filesystem before
loading this owner skill. If several current-session objects fit, ask which one
the researcher means.

## 2. List a bounded remote candidate set

First inspect the command contract with `ep search --help` if it has not been
used in this session. Search the likely lowercase object type without a query so
the API returns newest-first metadata:

```bash
ep search --type survey --page_size 5
ep search --type results --page_size 5
```

For an ambiguous phrase such as "recent survey," check both `survey` and
`results`; researchers may mean the instrument or its responses. For "recent
results," check only `results`. Read candidates from `data.objects`, including
`uuid`, `object_type`, `alias`, `description`, `visibility`, `url`,
`last_updated_ts`, and `created_ts`.

Do not add `--visibility private`: omitting the filter includes the researcher's
private, unlisted, and public objects. Keep `--community` off unless they asked
for other users' public objects. Merge the returned metadata by
the timestamp that matches the user's wording and shortlist at most the three
newest plausible candidates:

| User wording | Order by |
|---|---|
| "latest," "newest," "just created," or "just ran" | `created_ts` |
| "recently edited," "last updated," or "latest revision" | `last_updated_ts` |
| ambiguous "recent" | `created_ts` by default; show both timestamps when an older object has a newer update |

Do not let an old object with a recent edit displace a newly created object for
a creation-oriented request. If the user clearly cares about the latest saved
revision instead, use update time.

Use the current runtime date required by the system prompt when "recent" names
a real time window. Never infer the year from model memory.

## 3. Inspect content only when metadata is insufficient

If alias and description identify a clear candidate, confirm it without pulling
several objects. Otherwise inspect no more than the three-item shortlist. Use a
temporary directory, not the study tree, so discovery does not create durable
study artifacts before the user selects an object.

For a survey, save the candidate temporarily and inspect its actual question
names, texts, types, and options:

```bash
candidate_dir=$(mktemp -d /tmp/ep-object-search.XXXXXX)
cleanup_candidate_dir() {
  case "$candidate_dir" in
    /tmp/ep-object-search.*) rm -rf -- "$candidate_dir" ;;
    *) return 1 ;;
  esac
}
trap cleanup_candidate_dir EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
ep inspect <uuid> --type survey --save "$candidate_dir/candidate.ep"
ep surveys questions "$candidate_dir/candidate.ep"
```

Run the temporary save and its inspection in the same shell invocation so the
validated EXIT trap removes the package on success, error, or interruption.
The signal handlers exit through that cleanup path. Never
remove an unvalidated path and never leave candidate copies in the study tree.

For Results, inspect summary metadata first:

```bash
ep inspect <uuid> --type results --sample 1
```

If the returned column names are insufficient, save that shortlisted Results
object temporarily and use `ep results head --rows 1` with explicit repeated
`--column` arguments selected from only these namespaces:

- `question_text.*`
- `scenario.*`
- `agent.*`

Never include `answer.*`, `prompt.*`, `raw_model_response.*`, or other response
content merely to identify an object. A single sampled row can supply positive
matching evidence, but it cannot prove that a value never occurs in later rows.
Do not claim that `.head(1)` avoids downloading a remote Results object: keep
the shortlist small because inspection still retrieves the object.

## 4. Confirm, then retrieve

Present up to three candidates with type, description or alias, updated time,
and URL. If one match is unambiguous, name the evidence and confirm or proceed
as the request permits. If several remain plausible, ask the researcher to
choose before saving anything into the study.

After selection, return to the main skill's Retrieve step. If the bounded search
finds no plausible match, offer one controlled expansion (a keyword query or
the next metadata page), then ask whether the researcher has a local file. Do
not repeatedly pull broader candidate sets.
