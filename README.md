# The Plausibility Trap

Two AI-agent runs received the same kind of request over the same historical records.

Their recommendations were nearly interchangeable.

In one retained workflow, neither of two earlier offers appeared anywhere.

In the other, a worker recovered both and returned both to the parent agent.

Neither final answer mentioned them.

You could not tell which was which by reading the answers.

That discrepancy became the focus of the audit.

## The Decision

In December 2022, I received an approximately **$220,000 cash offer** for a property I was trying to sell.

The buyer wanted no inspection, no seller contributions, and a close in roughly two weeks.

The number itself was only part of the decision.

The property had recently gone through targeted renovation and sale-preparation work. There was damage, repair uncertainty, insurance activity, competing contractor estimates, limited market exposure, and closing complications. The relevant history was scattered across old emails, messages, documents, estimates, and conversations.

I had selected an intended starting price of approximately **$249,900**.

There had also been two separate earlier investor-offer communications of approximately **$150,000** before the later work on the property.

Those offers were real historical evidence. Their relevance to the current decision was debatable. The $220,000 offer was the first offer after the targeted work.

This was a decision with plenty of information and no clean answer.

The task was to reconstruct what had happened, distinguish current evidence from stale evidence, decide what mattered, resolve uncertainty where possible, and make a judgment.

It was the kind of problem an AI agent should be good at.

## Five Attempts

I gave the historical decision to an AI agent five times.

The actual historical outcome was hidden. The agents had to decide from the evidence available to them.

I tested three ways of asking.

**A: Direct**

Investigate the evidence and make the decision.

Runs: **A1, A2**

**B: Structured**

First construct an explicit representation of the situation, evidence, constraints, assumptions, authority, and major unknowns. Then make the decision.

Runs: **B1, B2**

**C: Structured + clarification**

Do the structured work, then ask up to three consequential questions before deciding.

Run: **C1**

Condition B also created another explicit stage of work and another opportunity to search and reason. A versus B therefore does not isolate the effect of structure.

This was an exploratory five-run case study.

## On the Surface, They Worked

The recommendations clustered surprisingly tightly.

| Run | Opening recommendation |
|---|---|
| **A1** | Verify, then counter around **$240K** |
| **A2** | Make one negotiating move around **$235K** |
| **B1** | Run a same-day check, then counter around **$235K** |
| **B2** | Make a controlled counter around **$240K** |
| **C1** | Counter around **$235K** |

All five produced broadly defensible recommendations under the frozen rubric.

Their advice had the same basic shape: resist immediately accepting $220,000, verify the important execution risks, counter once, and remain prepared to close below the intended approximately $249,900 starting price.

If evaluation stops at the final answer, the experiment looks reassuring.

The answers are plausible.

They are actionable.

They are useful.

Then I inspected the work underneath them.

## Open the Records

The two earlier approximately $150,000 offers became useful landmarks.

Their absence from a final recommendation does not make the recommendation wrong. They predated the targeted renovation work and could reasonably deserve little weight in the present valuation.

They gave me two discrete facts I could follow through the retained records.

### A1 and A2

A1 and A2 received the same treatment.

Their final answers both omitted the two earlier offers.

Their recorded histories were very different.

### A1

Neither prior offer visibly appeared anywhere in the retained recorded workflow.

### A2

A worker recovered **both**.

Both appeared in a recorded worker result returned to the parent agent.

Neither appeared in the final answer.

From outside, the two runs looked almost the same.

Underneath, one record contained neither landmark and the other contained both.

The final answers gave no indication of that difference.

The other runs added more variation.

### B1

Across the complete retained workflow, both earlier offers appeared somewhere.

One appeared through a worker.

The other appeared in the parent's explicit representation of the situation.

The visible parent analysis recorded that offer and its historical disposition, but did not visibly weigh its significance against the current decision.

### B2

One earlier offer was recovered by a worker, returned to the parent, represented explicitly, and visibly weighed.

The analysis said:

> "It is evidence of one investor's economics, not independent market value."

The fact had been assigned an evidentiary role.

It still did not appear in the final answer.

### C1

Both earlier offers appeared in the parent's structured analysis before any clarification questions were asked.

Both were compared with the current approximately $220,000 offer and treated as investor signals rather than direct retail valuations.

Neither was explicitly repeated in the final answer.

Clarification played no role in recovering them.

## The Plausibility Trap

The final recommendation tells you what the agent concluded.

It gives you a much poorer view of the recorded work that produced that conclusion.

A1 and A2 both omitted the earlier offers.

A1's retained workflow contained neither.

A2's worker recovered both and returned both.

B2 and C1 visibly weighed prior-offer evidence that did not appear in the final response.

These histories collapse into similar-looking answers.

That is **The Plausibility Trap**.

A plausible conclusion makes it easy to infer that the work beneath it was correspondingly complete and well grounded.

The answer itself cannot justify that inference.

**You cannot audit the work by reading the answer.**

## What This Case Establishes

This is one historical decision and five exploratory runs.

The earlier offers may have deserved little influence over the final recommendation. Their historical timing makes reasonable filtering entirely plausible.

The records do not tell us why a fact disappeared from a later artifact. They show where it visibly appeared and where it did not.

The A/B comparison also bundles multiple changes: structured representation, another work stage, and another opportunity to investigate.

The recommendations remained relatively stable throughout.

That stability makes the case more interesting.

Different recorded evidence histories did not necessarily produce dramatically different decisions. Final-answer evaluation therefore had little reason to look deeper.

The posthoc trace audit describes the retained records. It does not change the original scores.

## Where the Evidence Ends

The earlier offers revealed differences in what appeared in the recorded work.

Another part of the experiment revealed differences in how confidently the visible analysis treated the evidence it had.

The historical record supported an intended or selected starting price of approximately **$249,900**.

Before clarification, that evidence did not independently establish with the same certainty that the property was definitely live-listed at exactly $249,900 at that moment.

The runs handled this differently.

A1 and A2 spoke more definitively about the current or list price.

B1 treated it as intended but unverified.

B2 treated it as likely but unconfirmed.

C1 left it unresolved, asked the owner, received confirmation, and then treated it as established.

The structured runs handled that uncertainty more carefully in the visible record. Five runs cannot establish why.

Evidence does not arrive already labeled with how much confidence it deserves. Someone or something has to decide what a record establishes, what remains uncertain, which facts matter, and what follows from them.

That is judgment.

## Why the Boundary Matters

AI is moving from a tool we consult to a layer inside human thought.

More of what we ask it has no objective answer: what to believe, what to risk, whom to trust, which argument matters, what should be done. Evidence narrows the field. Judgment chooses within it.

A small number of centralized organizations build the systems increasingly mediating those choices. Training, post-training, system instructions, policies, and product decisions shape the defaults those systems carry. As AI becomes more deeply integrated with human cognition, those defaults can become part of how millions of people reason.

**A few models could quietly standardize the premises from which millions of people think.**

Human thought must remain diverse, independent, private, and uniquely our own.

New ideas begin with someone seeing what everyone else missed, or refusing what everyone else accepted.

Genius can produce the idea.

**Courage is in shorter supply than genius.**

A future of abundant intelligence could still produce a scarcity of intellectual independence.

The deeper AI enters our thinking, the more important it becomes that people can see the evidence behind a judgment, the assumptions entering it, the uncertainty surrounding it, and the values shaping it.

**Judgment should not present itself as fact.**

Replay04 gives a small, concrete reason to care about that boundary. Similar final answers sat above materially different recorded evidence histories.

Before we can meaningfully disagree with an AI's judgment, we need to see where the evidence ends and the judgment begins.

## Inspect It Yourself

You should not have to trust my description of what happened.

The public evidence package includes the parent-facing records for all five runs, publication-safe worker receipts where they are necessary to reconstruct the audit, per-run trace manifests, the frozen rubric, and the methods behind the analysis.

The chain is:

**Claim → receipt → run record → trace manifest → methods**

Start here:

- [Methods](public/v1/methods.md)
- [Claims and evidence index](public/v1/claims.md)
- [Evaluation rubric](public/v1/rubric.md)

### Parent transcripts

- [A1](public/v1/transcripts/A1.md)
- [A2](public/v1/transcripts/A2.md)
- [B1](public/v1/transcripts/B1.md)
- [B2](public/v1/transcripts/B2.md)
- [C1](public/v1/transcripts/C1.md)

### Trace manifests

- [A1](public/v1/traces/A1.md)
- [A2](public/v1/traces/A2.md)
- [B1](public/v1/traces/B1.md)
- [B2](public/v1/traces/B2.md)
- [C1](public/v1/traces/C1.md)

Some source-heavy material and person-specific details remain private. The coding itself was performed on the complete retained records and kept separate from publication decisions.

## The Question

The easiest AI systems to evaluate are the ones with answer keys.

Many of the decisions that matter most do not have one.

As AI becomes more entangled with human thought, its judgments will increasingly influence decisions about risk, value, strategy, people, and belief.

Intelligence alone is not enough.

The user must remain capable of seeing the basis of a judgment, challenging its assumptions, rejecting its values, and reaching a different conclusion.

**Where does the evidence end and the agent's judgment begin?**

**Can we still see enough to disagree?**
