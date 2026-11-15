# Synthetic pre-work rehearsal

The installed `fielding` runtime includes EDSL for `simulate survey` and
`simulate synthesize`. Full `simulate meeting` additionally requires the separate
Conversation package, which this integration does not install. Do not claim a
full conversation rehearsal is available or substitute a fabricated transcript.

For requested pre-work simulation, use a separate Treffen project from any real
participant study. Configure JSON with an `organizer` persona and `attendees`
list containing one persona per participant (`participant_id`, `display_name`,
`traits`, optional `instructions`). Import with `simulate configure --input
<personas.json>`. Synthetic roles represent authored scenarios, not those real
people's beliefs.

Select a current model via `skill:workflow-model-selection` and establish cost
and execution authorization via `skill:edsl-surveys-cost` before calling
`simulate survey --model <selected-model>` or `simulate synthesize --model
<selected-model>`. These commands execute EDSL internally rather than exporting
Jobs for `ep run`. `--disable-remote-inference` selects EDSL's local execution
path; a model provider can still be remote and charge for calls.

The survey simulation builds its own Survey and does not apply the collection
builder's groups/skip rules. Use it only for instruments whose behavior matches
that simpler path; do not present it as a faithful branching-instrument test.
The package stores synthetic Results under `.treffen/simulation/`; retain these
and check citations in synthetic findings just as with human inputs. Review all
findings before design. `simulate synthesize` also writes into the ordinary
synthesis tree, and design files are not automatically labeled synthetic, so
label every rehearsal export and keep human and synthetic projects separate.

Simulation files use fixed names and can be overwritten on rerun. Preserve each
completed run before another execution. Synthetic agreement and simulated
outcomes do not establish actual participant agreement, attendance, or decisions.
