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
  "aiedImplications": [
    "What this paper means for AI-EdTech product designers — specific, actionable, not generic.",
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

## Step 4 — Assemble and output the HTML file

Locate the template file. Try these paths in order, use the first one that exists:
1. `/mnt/skills/user/paper-reader/paper-reader-template.html` — skill installed in user skills
2. `/mnt/user-data/uploads/paper-reader-template.html` — user uploaded it manually

If neither path exists, tell the user:
> "I can't find the Paper Reader template. Please upload `paper-reader-template.html` to the conversation and I'll assemble your reader."
Then wait — do not proceed without the template.

Once you have the template, find the data injection block:

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
  "glossaryTerms": [ /* merged glossary from Step 3 */ ]
}
```

**Critical — do not move or remove the `<script>init();</script>` line that follows the data block.** This call must appear after the `paper-data` closing tag so the DOM element exists when `init()` runs. If `init()` is placed inside or before the data block, the app will load with an empty library.

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

**keyQuotes**: 1–2 sentences that crystallise the paper's argument or coin a concept. No methodological boilerplate.

**glossaryTerms explanation**: Substantial enough to stand alone as a mini explainer. Not a restatement of the definition.

**aiedImplications**: 2–3 implications specifically for AI-EdTech product designers — people building tutoring systems, adaptive learning tools, or AI feedback engines. Not generic pedagogy restatements. Each implication should name a concrete design decision, risk, or opportunity the paper surfaces. Bad: "This paper suggests engagement matters." Good: "An AI tutor that defaults to effort praise in group-accountability contexts (e.g. class leaderboards) may increase anxiety rather than motivation — consider making praise mode context-sensitive."

**quiz**: 3–5 questions per paper. Must include all three of the following types — no exceptions:
- **1 methodology question**: For empirical papers, ask about research design, sample, or analytical approach. For review articles or book chapters, ask about the scope, selection criteria, or synthesis method (e.g. "Which best describes the evidential basis of this chapter?").
- **1 findings question**: Test a specific claim from the paper, ideally with a statistic, effect size, or named phenomenon. Generic comprehension does not qualify.
- **1 critical thinking question**: Ask the reader to evaluate a limitation, apply a finding to a new context, or identify a tension between this paper and another. The correct answer must not be guessable without reading the paper.

All distractors must be plausible — wrong answers should reflect common misconceptions, not obvious nonsense.

---

## Common failure modes to avoid

- **Generic findings**: "AI can be helpful in education" is not a finding.
- **Generic aiedImplications**: "This paper has implications for EdTech" is not an implication. Name the specific design decision, tradeoff, or risk.
- **elevatorPitch that reads like an abstract**: Answer "so what?", not "what is this paper about."
- **Forcing original-research methodology onto review articles**: If the paper synthesises other work, say so — don't invent a sample size or research design that doesn't exist.
- **futureWork mixed with weaknesses**: futureWork = authors' own words; weaknesses = your external critique.
- **Duplicate glossary entries**: One entry per concept across all papers. Use `relatedPapers` to link multiple papers.
- **Sparse `relatedPapers`**: Every concept shared across 2+ papers must have all paper IDs listed. An empty or single-entry `relatedPapers` on a shared concept breaks the Synthesis Lab.
- **Circular glossary definitions**: Don't define "self-regulated learning" as "learning that is self-regulated."
- **keyQuotes from the methods section**: Pick sentences that make someone want to read the paper.
- **Shallow weaknesses**: "Small sample size" with no explanation of what it invalidates is a placeholder.
- **Quiz questions with obvious answers**: If guessable without reading, rewrite.
- **Missing quiz question types**: Every paper needs at least one methodology, one findings, and one critical-thinking question. Do not fill the quota with three comprehension questions.
- **Proceeding without the template**: Never attempt to reconstruct the HTML from memory. If the template file is missing, stop and ask the user to provide it.
- **Moving `init()` before the data block**: `init()` must run after `paper-data` is in the DOM. Never place it inside the main `<script>` block or before the data injection block.
