# 📄 Paper Reader Skill

A Claude Code skill that transforms one or more academic papers into a **single self-contained interactive HTML file** — ready to open in any browser, no server required.

## ✨ Features

| Feature | Description |
|---|---|
| 📚 **Paper Library** | Browse all loaded papers with key metadata at a glance |
| 🔍 **Critical Analysis** | Structured breakdown: methodology, findings, strengths, weaknesses |
| 🕸 **Paper Network** | Auto-generated relationship diagram showing how papers connect (multi-paper) |
| 🧩 **Thematic Synthesis Lab** | Cross-paper concept explorer powered by a merged glossary |
| 📝 **Interactive Quiz** | Auto-generated comprehension and critical-thinking questions |
| 📖 **Glossary** | Unified term definitions with links to related papers |
| 🤖 **AI Chat** | Research assistant tab (requires Anthropic API key) |

## 🚀 Quick Start

1. Install the skill in your Claude Code environment
2. Upload one or more academic PDFs (or paste text / provide URLs)
3. Say: `help me read this paper` or `analyze this paper`
4. Claude asks which **domain** you're working in (default: AI-EdTech) to tailor practical implications
5. Claude outputs a single `paper-reader.html` file
6. Double-click to open in your browser — everything is ready

## 💬 Trigger Phrases

- `help me read this paper`
- `analyze this paper`
- `create a reader for these papers`
- `extract this paper`
- Upload any academic PDF

## 📋 What Gets Extracted

For each paper, the skill extracts:

| Field | Description |
|---|---|
| **Elevator Pitch** | 50-word active summary — answers "so what?", not "what is this paper about" |
| **Abstract** | Verbatim or closely paraphrased |
| **Methodology** | Research design, sample, instruments, and analysis approach |
| **Key Findings** | Specific, citable claims with statistics where available |
| **Future Work** | Authors' own acknowledged limitations and next steps |
| **Strengths & Weaknesses** | Critical assessments — weaknesses name what a limitation *prevents us from concluding* |
| **Key Quotes** | 1–2 memorable sentences (≤40 words) that crystallise the paper's argument |
| **Pedagogical Implications** | Practical implications for teaching and learning |
| **Practical Implications** | Actionable insights for practitioners in your domain (default: AI-EdTech product designers) |
| **Key Concepts** | Core terms used to build the merged glossary |
| **Quiz** | 3–5 questions per paper — must include one methodology, one findings, one critical-thinking question |

## 🗂 Multi-Paper Support

When multiple papers are provided:

- All papers are processed before any output is generated
- **Paper Network** (Step 3.5): auto-generated SVG relationship diagram showing directed edges between papers (e.g. `provides_foundation`, `extends`, `contradicts`, `empirically_tests`)
- Glossary terms are **merged across papers** — no duplicates
- Each glossary entry includes `relatedPapers` linking all papers that share the concept
- The **Thematic Synthesis Lab** uses `relatedPapers` to surface cross-paper connections

## 📁 File Structure

```
paper-reader/
├── SKILL.md                              # Skill instructions for Claude
├── README.md                             # This file
└── references/
    ├── paper-reader-template.html        # HTML template (embedded at assembly time)
    └── pdf_to_txt.py                     # PDF pre-processing helper (Claude Code)
```

## ⚙️ Requirements

- Claude Code with skill support
- `paper-reader-template.html` available at:
  - `/mnt/skills/user/paper-reader/references/paper-reader-template.html` (preferred), or
  - uploaded manually to the conversation
- For **AI Chat** tab: an [Anthropic API key](https://console.anthropic.com/)

> **Note:** If the template file cannot be found, Claude will stop and ask you to upload it — it will never reconstruct the HTML from memory.

## 🖥️ Local PDF Pre-processing (Claude Code)

When running in **Claude Code** with local PDF files, large PDFs (>5MB or >30 pages) cannot be read directly — the embedded images and layout data inflate the file size beyond the tool limit. Use the included helper script to extract plain text first:

```bash
# Install dependency (once)
pip install PyPDF2

# Extract text from all PDFs in one command
python3 references/pdf_to_txt.py paper1.pdf paper2.pdf paper3.pdf
# → Creates paper1.pdf.txt, paper2.pdf.txt, paper3.pdf.txt
```

Claude will then read the `.txt` files instead of the original PDFs. This step is handled automatically when you invoke the skill — no manual action needed.

## 📊 Output Quality Standards

The skill enforces strict quality on every extraction:

- **Elevator Pitch** answers "so what?" — not a shortened abstract; max 50 words
- **Findings** must be specific and citable — no generic statements like "AI can be helpful"
- **Practical Implications** must name concrete design decisions, tradeoffs, or risks for your domain
- **Weaknesses** explain what the limitation *prevents us from concluding* — not just "small sample size"
- **Quiz** always includes at least one methodology, one findings, and one critical-thinking question; distractors must be plausible (≤15 words each)
- **Paper Network edges** require genuine directional relationships — `contradicts` is only used when the same construct is measured in comparable conditions with opposing results
- **Glossary** never has duplicate entries; every shared concept must list all relevant paper IDs in `relatedPapers`

## 🧠 Designed For

- Researchers processing large paper corpora
- Students preparing for seminars or literature reviews
- AI-EdTech product designers extracting design insights
- Anyone who wants to go beyond passive reading

## 📄 License

MIT
