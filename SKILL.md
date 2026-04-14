---
name: paper-reader
description: |
  Turns one or more academic papers into a single self-contained interactive HTML file the user can open directly in their browser. Use this skill whenever a user uploads research papers (PDF, text, or URL) and wants to study them, take quizzes, explore key concepts, or chat with an AI about the content. Trigger when the user says "help me read this paper", "analyze this paper", "create a reader for these papers", "extract this paper", or uploads any academic PDF. The skill reads all papers, extracts structured data, merges glossary terms across papers, and outputs one ready-to-use HTML file — no further steps needed from the user.
---

# Paper Reader Skill

Reads one or more academic papers and outputs a single self-contained HTML file. The user opens it in their browser and gets a fully interactive reading environment — library, critical analysis, quiz, glossary, Thematic Synthesis Lab, and AI chat — with all paper data already embedded.

## What this skill does

1. Reads all papers the user provides (PDF, text, or URL)
2. Extracts structured content for each paper across 4 dimensions
3. Merges glossary terms across papers (no duplicates), with `relatedPapers` populated for every shared concept
4. Embeds all data into the HTML template using the correct injection procedure
5. Outputs one complete `.html` file — double-click to open, everything is ready

---

## Step 1 — Read all papers

**CRITICAL: Template Check Before Starting**
Before doing anything else, locate the template file. Try these paths in order:
1. `/mnt/skills/user/paper-reader/references/paper-reader-template.html` — skill installed in user skills (original)
2. `/mnt/user-data/uploads/paper-reader-template.html` — user uploaded it manually

If neither path exists, tell the user:
> "I can't find the Paper Reader template. Please upload `paper-reader-template.html` to the conversation and I'll assemble your reader."

**Wait for the template.** Do not proceed to read papers without it.

**Ask for Domain**
Ask the user what domain or field they are working in (default is AI-EdTech) so you can tailor the `practicalImplications` extraction to their specific context.

Read every paper the user has provided before extracting anything.

If the user uploads PDFs, use the pdf-reading skill (`/mnt/skills/public/pdf-reading/SKILL.md`). If they paste text or provide URLs, use those directly.

**Read each paper fully before extracting. Do not skim.**

If multiple papers are provided, process them all before moving to Step 2.

---

## Step 2 — Extract structured content for each paper

For each paper, produce a JSON object matching **exactly** this schema. Do not omit or rename fields.

```json
{
  "id": "author-year",
  "title": "Full paper title",
  "authors": "Last, F., Last, F., & Last, F.",
  "year": 2024,
  "journal": "Journal or Conference Name",
  "elevatorPitch": "50 words or fewer: what problem this paper solves and how.",
  "abstract": "The paper's actual abstract, verbatim or closely paraphrased.",
  "methodology": "1–3 sentence description of the research design, sample, instruments, and analytical approach.",
  "keyFindings": [
    "Finding 1 — specific, not vague",
    "Finding 2",
    "Finding 3"
  ],
  "futureWork": [
    "Limitation or open question the authors themselves acknowledge",
    "Future direction 2"
  ],
  "strengths": [
    "Methodological or conceptual strength 1",
    "Strength 2",
    "Strength 3"
  ],
  "weaknesses": [
    "External critique not acknowledged by the authors",
    "Weakness 2",
    "Weakness 3"
  ],
  "keyQuotes": [
    "Most memorable sentence from the paper, verbatim."
  ],
  "pedagogicalImplications": [
    "Practical implication for teaching or learning 1",
    "Implication 2"
  ],
  "keyConcepts": [
    "Concept Name 1",
    "Concept Name 2"
  ],
  "practicalImplications": [
    "What this paper means for practitioners in the target domain (default: AI-EdTech) — specific, actionable, not generic.",
    "Implication 2"
  ],
  "quiz": [
    {
      "question": "A specific comprehension or critical-thinking question",
      "options": [
        "Option A — plausible but wrong",
        "Option B — correct answer",
        "Option C — plausible but wrong",
        "Option D — plausible but wrong"
      ],
      "correctAnswer": 1,
      "explanation": "Why the correct answer is right, citing this paper's content."
    }
  ]
}
```

Note: `glossaryTerms` is built separately in Step 3 — do not include it per-paper.

---

## Step 3 — Build the merged glossary

Collect all `keyConcepts` across every paper. For each unique concept, create one glossary entry. If the same concept appears in multiple papers, list all paper IDs in `relatedPapers` — never duplicate an entry.

**`relatedPapers` is critical — do not treat it as optional.** It is the primary data source for the Thematic Synthesis Lab. If `relatedPapers` is missing or incomplete, the synthesis view will be empty. For every concept that appears in more than one paper, you must list all relevant paper IDs. When in doubt, be inclusive rather than sparse.

```json
[
  {
    "term": "Self-Regulated Learning",
    "definition": "One-sentence plain-language definition.",
    "explanation": "2–3 paragraph in-depth explanation of the concept, its origins, and how it appears across the loaded papers.",
    "example": "A concrete real-world example of this concept in action.",
    "relatedPapers": ["darvishi-2024", "huang-2023"]
  }
]
```

---

## Step 3.5 — Build the paper network (multi-paper only)

**Skip this step if fewer than 2 papers are loaded.**

Analyse relationships across all papers and produce a `paperNetwork` object. This powers the **Paper Network** view in the HTML, which renders as two layers: (1) an auto-generated SVG relationship diagram at the top showing paper nodes and labeled directed edges, and (2) detail cards below each edge. Claude only needs to supply the correct JSON data — the SVG diagram is built entirely by the template's JavaScript and requires no additional work from Claude.

Read all papers again holistically before generating edges. Do not generate edges from memory of individual extractions — look for actual argumentative, methodological, and conceptual connections.

```json
{
  "sharedQuestions": [
    {
      "question": "One sentence describing a research question that 2+ papers address",
      "papers": ["author-year", "author-year"]
    }
  ],
  "methodologicalClusters": [
    {
      "approach": "e.g. 'Randomized Controlled Trial', 'Ethnographic Field Study', 'Systematic Review'",
      "papers": ["author-year"]
    }
  ],
  "edges": [
    {
      "from": "author-year",
      "to": "author-year",
      "type": "provides_foundation | empirically_tests | contradicts | extends | replicates | challenges_assumption | methodologically_complements",
      "evidence": "explicit_citation | textual_inference | thematic_overlap",
      "evidenceQuote": "Verbatim sentence from either paper that supports this edge, or null if none",
      "confidence": "high | medium | low",
      "description": "1–2 sentences explaining what this relationship means concretely"
    }
  ],
  "divergencePoints": [
    {
      "topic": "Name of the contested claim or construct",
      "positions": [
        { "paper": "author-year", "stance": "This paper's position in 1 sentence" }
      ]
    }
  ]
}
```

**Edge type definitions:**
- `provides_foundation` — Paper A's theory, framework, or construct is adopted as a basis by Paper B
- `empirically_tests` — Paper B provides empirical data that tests a claim made in Paper A
- `contradicts` — Paper B's findings directly oppose Paper A's on the same variable or outcome (require genuine directional conflict, not merely different results in different populations)
- `extends` — Paper B builds on Paper A's scope, population, or context without contradicting it
- `replicates` — Paper B attempts to reproduce Paper A's study design or findings
- `challenges_assumption` — Paper B questions a methodological or theoretical assumption Paper A relies on, without necessarily contradicting its findings
- `methodologically_complements` — Papers address the same question with different methods (e.g. lab vs. field, quantitative vs. qualitative) at different ecological validity levels

**Confidence rules:**
- `high` — Supported by explicit cross-citation AND direction of argument is unambiguous
- `medium` — No cross-citation but the textual evidence is clear and the inference is defensible
- `low` — Inferred from thematic overlap only; no direct textual support

**Critical constraints:**
- Never generate `contradicts` edges for papers that merely have different findings in different contexts — contradiction requires the same construct measured in comparable conditions with opposing directional results
- Never generate `provides_foundation` without being able to name the specific theory or framework being adopted
- Keep `evidenceQuote` under 50 words; null is better than a fabricated quote
- Aim for 2–6 edges total for a 3-paper set; do not force edges where none exist
- `divergencePoints` should only appear when there is a genuine interpretive or empirical disagreement, not merely different research foci

---





Find the data injection block in the template:

```html
<script id="paper-data" type="application/json">
{"papers":[],"glossaryTerms":[]}
</script>
<script>init();</script>
```

Replace **only the contents of the paper-data script tag** with the assembled data:

```json
{
  "papers": [ /* all extracted paper objects from Step 2 */ ],
  "glossaryTerms": [ /* merged glossary from Step 3 */ ],
  "paperNetwork": { /* network object from Step 3.5, or null if single paper */ }
}
```

**Critical — do not move or remove the `<script>init();</script>` line that follows the data block.** This call must appear after the `paper-data` closing tag so the DOM element exists when `init()` runs. If `init()` is placed inside or before the data block, the app will load with an empty library.

**CRITICAL: Validation Before Output**
Before calling `create_file`, you MUST validate the JSON data:
1. **JSON Validity:** Ensure the JSON is structurally sound and parses correctly.
2. **Data Completeness:** Verify that both `papers` and `glossaryTerms` arrays exist.
3. **Paper Count Match:** Count the items in the `papers` array. It MUST exactly match the number of papers you read in Step 1. If it does not, fix the extraction before proceeding.
4. **Essential Fields:** Check that every paper has an `id`, `title`, and `practicalImplications` array.

If any validation fails, do not create the HTML file silently. Fix the data or alert the user.
Output the complete HTML using `create_file` to `/mnt/user-data/outputs/paper-reader.html`, then use `present_files` to deliver it.

Say:
> **Your Paper Reader is ready.** Open `paper-reader.html` in any browser — all papers are pre-loaded. To use AI chat, enter your Anthropic API key in the Research Assistant tab.

---

## Quality standards

**elevatorPitch**: Active sentence: "This paper [does X] by [method Y], finding [Z]." Hard limit: 50 words. Not a shortened abstract.

**methodology**: For original research, name the design, sample, instruments, and analysis method. For review articles, book chapters, or opinion pieces, describe the corpus being synthesised and the synthesis approach — e.g. "Narrative review synthesising 5 empirical studies spanning museum visits, large-scale assessment, classroom surveys, case study, and online workshop analysis. No original data collection." Never force a single-study methodology description onto a paper that does not have one.

**keyFindings**: Complete, citable claims. Include statistics or effect sizes where reported. No findings generic enough to apply to any paper. For review articles, findings are the conclusions the authors draw from their synthesis — not summaries of individual studies reviewed.

**futureWork**: Authors' own acknowledged limitations and next steps only. Strictly distinct from `weaknesses`.

**strengths / weaknesses**: Critical assessments, not summaries. Weaknesses should name what the limitation prevents us from concluding — not just "small sample size." For review articles, weaknesses include selection bias in study choice, lack of systematic search criteria, and overgeneralisation across heterogeneous samples.

**keyQuotes**: 1–2 sentences that crystallise the paper's argument or coin a concept. Hard limit: maximum 40 words or 2-3 lines. No methodological boilerplate.

**glossaryTerms explanation**: Substantial enough to stand alone as a mini explainer. Not a restatement of the definition.

**practicalImplications**: 2–3 implications specifically for practitioners in the user's domain (default: AI-EdTech product designers). Not generic restatements. Each implication should name a concrete design decision, risk, or opportunity the paper surfaces. Bad: "This paper suggests engagement matters." Good: "An AI tutor that defaults to effort praise in group-accountability contexts (e.g. class leaderboards) may increase anxiety rather than motivation — consider making praise mode context-sensitive."

**quiz**: 3–5 questions per paper. Must include all three of the following types — no exceptions:
- **1 methodology question**: For empirical papers, ask about research design, sample, or analytical approach. For review articles or book chapters, ask about the scope, selection criteria, or synthesis method (e.g. "Which best describes the evidential basis of this chapter?").
- **1 findings question**: Test a specific claim from the paper, ideally with a statistic, effect size, or named phenomenon. Generic comprehension does not qualify.
- **1 critical thinking question**: Ask the reader to evaluate a limitation, apply a finding to a new context, or identify a tension between this paper and another. The correct answer must not be guessable without reading the paper.

All distractors must be plausible and concise (maximum 15 words per distractor) — wrong answers should reflect common misconceptions, not obvious nonsense.

---

## Common failure modes to avoid

- **Generic findings**: "AI can be helpful in education" is not a finding.
- **Generic practicalImplications**: "This paper has implications for EdTech" is not an implication. Name the specific design decision, tradeoff, or risk.
- **elevatorPitch that reads like an abstract**: Answer "so what?", not "what is this paper about."
- **Forcing original-research methodology onto review articles**: If the paper synthesises other work, say so — don't invent a sample size or research design that doesn't exist.
- **futureWork mixed with weaknesses**: futureWork = authors' own words; weaknesses = your external critique.
- **Duplicate glossary entries**: One entry per concept across all papers. Use `relatedPapers` to link multiple papers.
- **Sparse `relatedPapers`**: Every concept shared across 2+ papers must have all paper IDs listed. An empty or single-entry `relatedPapers` on a shared concept breaks the Synthesis Lab.
- **Over-generating edges**: Do not force a `contradicts` edge because two papers have different findings. Require genuine directional conflict on the same variable.
- **Fabricating evidenceQuote**: If no direct quote supports the edge, set `evidenceQuote` to null. Never invent a quote.
- **Assigning high confidence to thematic_overlap edges**: `thematic_overlap` evidence must map to `low` confidence. High confidence requires `explicit_citation`.
- **Circular glossary definitions**: Don't define "self-regulated learning" as "learning that is self-regulated."
- **keyQuotes from the methods section**: Pick sentences that make someone want to read the paper.
- **Shallow weaknesses**: "Small sample size" with no explanation of what it invalidates is a placeholder.
- **Quiz questions with obvious answers**: If guessable without reading, rewrite.
- **Missing quiz question types**: Every paper needs at least one methodology, one findings, and one critical-thinking question. Do not fill the quota with three comprehension questions.
- **Proceeding without the template**: Never attempt to reconstruct the HTML from memory. If the template file is missing, stop and ask the user to provide it.
- **Moving `init()` before the data block**: `init()` must run after `paper-data` is in the DOM. Never place it inside the main `<script>` block or before the data injection block.
