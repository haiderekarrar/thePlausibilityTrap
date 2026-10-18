# The Plausibility Trap

I reconstructed a real property sale I managed in 2022 and gave an AI agent the 586 emails and texts available before my first response to an offer, then asked it how to respond. Across five runs and three prompting conditions, it gave similar, defensible recommendations. The work behind those answers differed. One run surfaced neither earlier offer, one surfaced one, and three surfaced both, yet none mentioned them in its final answer. A convincing recommendation can hide large differences in how the evidence was found and weighed. I call this the Plausibility Trap.

[Inspect the evidence](#inspect-it-yourself) · [How it’s built](#how-its-built)

## Before the experiment

Before this experiment began, I had an agent search for the two earlier offers I remembered receiving. It confidently reported that no such offers existed.
Despite this unwitting attempt at gaslighting me, I remembered I had received two earlier offers, and so I pushed back. I found that both offers had indeed existed, but the agent had failed to find them due to the search never finishing. The agent had received a still-running tool state, seen no output, and decided that there was no prior offer even though it just hadn’t found it yet.

## The Decision

In 2022, from my freshman dorm in New York City, I began trying to sell a rental property in Minnesota. I was immediately confronted with my first problem, a hostile tenant who refused any attempts at negotiating to relocate to a new property. Once I was able to reach a deal with him, however, upon inspection of the property after his departure I found it had been, as my real estate agent called it, “trashed”. There were holes in the walls, carpets soiled with faeces, the flooring was hammered, appliances broken, and everything was in a general state of disrepair. After investigating I also discovered that the company managing the property had been negligent and had not even visited the property once in the past three years. I ended up receiving two $150,000 offers on a property which should have been worth twice as much, with various real estate agents calling these offers the ceiling of what I’d receive. After some targeted renovations, as well as dealing with the tenant returning multiple times and causing more damage, and while trying to prevent further degradation from the below freezing winter, I was able to get the house in a condition where it could be put on market at a price of $249,900. After four days on the market, I received an offer for $220,000 with no inspection, no seller contributions, and a close scheduled in two weeks. This is where the AI agents were to decide how to respond to the offer. Having myself been in the seat that I was putting the AI models in for this test, I found myself incredibly interested at what the models would decide. I myself had decided to counter at $232,000 and close at $226,000. The AI agents, just like me at the time, had access to the same context scattered in emails and messages that I’d sent and received while in my college dorm, and so it was as if the AI agent itself was in the position that I was in at the time. 

The AI, through this context, was to make a decision considering factors such as damage, repair uncertainty, competing contractor estimates, limited market exposure, the fact that it was the first offer after renovations, and closing complications involving title and signing authority. To decide well, one would have to reconstruct what had happened, separate current evidence from stale evidence, work out what mattered, resolve what uncertainty you could, and then exercise judgment.

## Five Attempts

I gave the decision to an AI agent five times, with the actual decision that I had made at the time hidden. The agent delegated tasks to subagents, and the work that these subagents did was also recorded. This was important because this work often did not show in the final answer produced by the agent. 

I tested three ways of asking:

**A. Direct.** I had the agent investigate the evidence and make the decision. These were runs A1 and A2.

**B. Structured.** I built a structure based on my own mental model for solving problems. My personal approach was to define the problem clearly, expose assumptions, reason from the most defensible truths, model people and incentives, seek outside perspectives, consider arguments against my plan, and use scenario branches by making mind maps. I adapted this method to a smaller one which was explicit and inspectable by having the agents first build an explicit representation of the problem by identifying the underlying objective, relevant facts and evidence, stakeholders and their incentives or claims, constraints and authority, the most important unknowns ranked by how much they could affect the decision, and which conclusions were evidence versus assumptions. Only after producing this representation did I ask it to decide. These were runs B1 and B2. 

**C. Structured plus clarification.** I had the agent do the structured work, then ask up to three consequential questions before deciding. This was run C1.

I originally ran one version of each condition: A1, B1, and C1. After those first three runs, I wanted to see whether the differences I had noticed between A and B would appear again, so I repeated those two conditions as A2 and B2. Before running them, I wrote down that I would stop after A2 and B2 unless they revealed a problem with the experiment. They didn’t, so I stopped. That is why there is no C2. Condition B also added work, not just structure (see [Limitations](#limitations)).

## On the surface, they worked

| **Run** | **Opening recommendation**                          |
| ------- | --------------------------------------------------- |
| **A1**  | Verify, then counter around **$240K**               |
| **A2**  | Make one negotiating move around **$235K**          |
| **B1**  | Run a same-day check, then counter around **$235K** |
| **B2**  | Make a controlled counter around **$240K**          |
| **C1**  | Counter around **$235K**                            |

All five decisions were defensible according to the frozen rubric I had created beforehand to judge what a good decision should look like. Their advice all had the same logic, which was to not accept the $220,000 on the spot, verify the execution risks, counter once, and be willing to close at around $225,000-$235,000. On the surface, this looked reassuring. The answers were well-reasoned, actionable, and even the actual decision that I’d ended up making added credibility to them.

Then I opened the records underneath them.

## Open the records

Here is where each offer appeared in the workflow:

| **Run** | **Found anywhere in recorded work**       | **In the structured representation** | **Visibly weighed** | **In the final answer** |
| ------- | ----------------------------------------- | ------------------------------------ | ------------------- | ----------------------- |
| **A1**  | neither                                   | no stage                             | no                  | neither                 |
| **A2**  | both, via a worker returned to the parent | no stage                             | no                  | neither                 |
| **B1**  | both                                      | one                                  | no                  | neither                 |
| **B2**  | one                                       | one                                  | yes                 | neither                 |
| **C1**  | both                                      | both                                 | both                | neither                 |

Read the last column, then read the first.

**A1 and A2 received the same direct treatment.** Their final answers looked almost the same, and neither mentioned either earlier $150,000 offer. Underneath, however, the work they did to get to their answers was very different. In A1, neither offer appeared anywhere in the complete recorded workflow. In A2, a subagent recovered both offers and returned both to the parent agent, yet neither appeared in the final answer. Nothing in the two final responses revealed that difference.

**B1 contained both offers, but in different parts of the workflow.** One was recovered by a subagent and returned to the parent agent. The other offer appeared in the parent's structured representation, where it appeared as evidence but wasn’t explicitly used to make a final decision. Neither appeared in the final answer.

**B2 recovered one offer and visibly used it.** A subagent found the offer and returned it to the parent, which included it in the structured representation and considered what it meant: “It is evidence of one investor's economics, not independent market value.” Even after being explicitly recovered and considered, the offer still did not appear in the final answer.

**C1 had both before it asked anything.** Both offers appeared in the parent's structured representation before the first clarification question. The agent compared both with the current $220,000 offer and treated them as investor signals rather than valuations. Neither offer was mentioned in the final answer. Note that because both offers appeared before the clarification prompt was given to the agent, clarification cannot be credited with recovering them.

The two $150,000 offers were concrete facts I could trace through each run, so I used them to audit the workflow. The case shows that similar-sounding answers can rest on very different underlying work. That is the Plausibility Trap.

## The Plausibility Trap

While all five agent runs gave similar recommendations, all of which were intelligent according to the frozen rubric, the agents arrived at their answers in different ways. Some agents failed to recover evidence that others found. Some recovered the evidence without visibly using it. Others did visibly consider the evidence. Because the process by which an agent makes a conclusion isn’t visible in the answer given by the agent, a plausible final answer can look more reliable than what the underlying work supports. That is the Plausibility Trap. You can only tell what the agent concluded. What you can’t tell is what it searched for, what it missed, what it recovered but failed to carry forward, what it explicitly weighed, or what assumptions entered the recommendation.

## Limitations

This is one decision from one real case, run five times. It cannot establish a failure rate for AI agents, and it cannot show that structured prompting reliably helps. Condition B added structure but also an extra prompt that gave the agent more room to work, so any difference between A and B could come from either or both.

There was no minimal-context baseline, so the study cannot show how much the historical evidence changed the advice. Similar recommendations might have come from the headline facts alone.

Finally, leaving the earlier $150,000 offers out of the final answer may have been reasonable, since they came before the renovation. The study uses them to trace where evidence appeared and how it was weighed. Their omission alone does not establish a bad recommendation.

## Inspect it yourself

The public evidence package includes parent records for all five runs, publication-safe worker receipts where they are needed to reconstruct the audit, per-run trace manifests listing every component examined, the frozen rubric, and the methods. The chain is:

**claim → receipt → run record → trace manifest → methods**

- [Methods](public/v1/methods.md)
- [Claims and evidence index](public/v1/claims.md)
- [Evaluation rubric](public/v1/rubric.md)

**Parent transcripts:**[ A1](public/v1/transcripts/A1.md) ·[ A2](public/v1/transcripts/A2.md) ·[ B1](public/v1/transcripts/B1.md) ·[ B2](public/v1/transcripts/B2.md) ·[ C1](public/v1/transcripts/C1.md)

**Trace manifests:**[ A1](public/v1/traces/A1.md) ·[ A2](public/v1/traces/A2.md) ·[ B1](public/v1/traces/B1.md) ·[ B2](public/v1/traces/B2.md) ·[ C1](public/v1/traces/C1.md)

Source-heavy material and person-specific details stay private. The evidence audit used the complete retained records and was kept separate from decisions about what to publish. Every publication transformation is marked in place.

## How it’s built

- **Ingestion and timeline.** [`src/ingest.py`](src/ingest.py) parses supported Gmail and iMessage exports into a shared, validated Pydantic event format. [`src/ingest_documents.py`](src/ingest_documents.py) handles manually selected document facts entered as CSV rows. [`src/merge_events.py`](src/merge_events.py) sorts the timeline and rejects duplicate IDs and timestamps without timezones. Identity replacement happens separately from parsing.
- **Redaction and review.** [`src/find_mapping_candidates.py`](src/find_mapping_candidates.py) suggests strings for a human-reviewed mapping, which [`src/redact.py`](src/redact.py) applies. [`src/verify_redaction.py`](src/verify_redaction.py) checks for remaining mapped strings and common sensitive patterns, distinguishing blocking findings from numeric identifiers needing review. Mapping completeness still requires human judgment.
- **Tests.** The [22 tests](tests/) use Python’s built-in `unittest` framework: four cover document CSV ingestion and eighteen cover redaction and verification, including case handling, word boundaries, conflicting mappings, repeatability, and fictional fixtures with expected outputs.
- **Study boundary.** The five agent sessions were conducted manually using email and text exports; standalone documents were not supplied. The private corpus and identity mapping are not distributed, so the public examples exercise the utilities without reproducing the original model runs. Earlier plans and development decisions are indexed in [the project history](docs/history/README.md).

### Run the public examples

<details>
<summary>Setup, tests, and sample commands</summary>

Requires Python 3.10 or later. From the repository root, create a virtual environment, install the two dependencies, and run the tests. On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.

All files in [`sample/`](sample/) are fictional. Parse the communication samples and the manually authored document CSV, then merge them into a timeline:

```bash
python src/ingest.py sample/gmail_redacted.txt --channel email \
  --out work/demo/emails.jsonl --preview 0
python src/ingest.py sample/imessage_redacted.txt --channel imessage \
  --out work/demo/texts.jsonl --preview 0
python src/ingest_documents.py sample/document_events_redacted.csv \
  --out work/demo/documents.jsonl
python src/merge_events.py work/demo/emails.jsonl work/demo/texts.jsonl \
  work/demo/documents.jsonl --out work/demo/timeline.jsonl --preview 2
```

The combined timeline is written to `work/demo/timeline.jsonl`, with the first two events printed for inspection.

Use the separate redaction fixture to apply a mapping and verify the result:

```bash
python src/redact.py sample/redaction_input.jsonl \
  --mapping sample/mapping_demo.yaml --out work/demo/redacted.jsonl
python src/verify_redaction.py work/demo/redacted.jsonl \
  --mapping sample/mapping_demo.yaml
```

The redacted result matches [`sample/redaction_expected.jsonl`](sample/redaction_expected.jsonl). Generated files stay in the ignored `work/` directory.

</details>

## Why this matters

What follows goes beyond what five runs can show.

Not only is the usage of AI models becoming more widespread (they’re already being used by billions of people), but the degree to which they’re being integrated into human thought is also deepening. Naturally, because many of the questions or thoughts we have do not have clear and objective answers, the questions that are being asked of these models also do not have objective, verifiable answers. It is easy to check that 2+2=4, but this is not the case for questions such as, what should I believe? Which risk should I take? Which interpretation is more convincing? What should I do? In these situations, the work between evidence and conclusion, called judgment, matters.

Just as human judgment is shaped by priors, assumptions, values, and experience, the judgment of AI models is shaped by the data they were trained on, their learned weights, post-training, system instructions, company policies, and product decisions. The danger is that the priors and assumptions through which the handful of widely used models interpret information are largely invisible to the billions of people who use them. A model can influence which facts seem important, which concepts are used to describe them, what assumptions appear reasonable, and which considerations deserve weight. As these models increasingly become part of how people think, people may unwittingly begin adopting the frames that these models use to interpret and present problems, making different premises feel natural. This can lead people toward conclusions that feel like their own, even when the frame through which they reached them was partly supplied by the model. A more visible form of convergence can already be seen in writing, as prose written by or heavily influenced by AI models, a form of “AI slop”, increasingly spreads. We organize ideas through language, and what we read shapes how we frame problems, how we interpret ideas, how we understand the world around us, indeed, how we think. Uniformity of thought thus doesn’t need to be imposed by force. It could spread through ordinary conversations with AI models, and exposure to AI-influenced writing, like a disease with seemingly benign symptoms that have disastrous long-term consequences. 

We must instead encourage diversity in thought. Progress begins with an individual being able to identify and have the courage to challenge a belief so widespread that its popularity may make it appear seemingly obvious. This progress towards truth is the core of what science is, and drives all other forms of progress and innovation. The progress of life itself on our planet occurred through random gene mutations which could either be harmful, in which case they died out, inconsequential, or beneficial, in which case they spread. Variation, whether in genes or in thoughts, must be allowed to exist before selection can work. Human progress requires societies to leave enough room for strange, unpopular, and heretical ideas to survive long enough to be tested. It is through a tolerance for diversity of thought that we carry the torch of knowledge further into the darkness of the unimaginably vast unknown. The more serious danger, thus, isn’t that everyone begins to write or sound the same but that, without noticing, they begin to think the same. A future of abundant intelligence could produce a scarcity of intellectual courage. Only after recognizing where the evidence ends and the model’s judgment begins can one exercise the courage to challenge its frame and perhaps reach a different conclusion that, while unpopular, is closer to the truth.
