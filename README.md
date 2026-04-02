# 📄 Paper Reader Skill

A Claude Code skill that transforms one or more academic papers into a **single self-contained interactive HTML file** — ready to open in any browser, no server required.

## ✨ Features

| Feature | Description |
|---|---|
| 📚 **Paper Library** | Browse all loaded papers with key metadata at a glance |
| 🔍 **Critical Analysis** | Structured breakdown: methodology, findings, strengths, weaknesses |
| 🧩 **Thematic Synthesis Lab** | Cross-paper concept explorer powered by a merged glossary |
| 📝 **Interactive Quiz** | Auto-generated comprehension and critical-thinking questions |
| 📖 **Glossary** | Unified term definitions with links to related papers |
| 🤖 **AI Chat** | Research assistant tab (requires Anthropic API key) |

## 🚀 Quick Start

1. Install the skill in your Claude Code environment
2. Upload one or more academic PDFs (or paste text / provide URLs)
3. Say: `help me read this paper` or `analyze this paper`
4. Claude outputs a single `paper-reader.html` file
5. Double-click to open in your browser — everything is ready

## 💬 Trigger Phrases

- `help me read this paper`
- `analyze this paper`
- `create a reader for these papers`
- `extract this paper`
- Upload any academic PDF

## 📋 What Gets Extracted

For each paper, the skill extracts:

- **Elevator Pitch** — 50-word summary of the core contribution
- **Abstract** — verbatim or closely paraphrased
- **Methodology** — research design, sample, instruments, and analysis approach
- **Key Findings** — specific, citable claims with statistics where available
- **Future Work** — authors' own acknowledged limitations and next steps
- **Strengths & Weaknesses** — critical assessments, not summaries
- **Key Quotes** — memorable sentences that crystallise the paper's argument
- **Pedagogical Implications** — practical implications for teaching and learning
- **AI-EdTech Implications** — actionable insights for AI education product designers
- **Quiz Questions** — methodology, findings, and critical-thinking question types

## 🗂 Multi-Paper Support

When multiple papers are provided:
- All papers are processed before any output is generated
- Glossary terms are **merged across papers** — no duplicates
- Each glossary entry includes `relatedPapers` linking all papers that share the concept
- The **Thematic Synthesis Lab** uses `relatedPapers` to surface cross-paper connections

## 📁 File Structure

```
paper-reader/
├── SKILL.md                      # Skill instructions for Claude
├── README.md                     # This file
└── references/                   # Reference materials
```

## ⚙️ Requirements

- Claude Code with skill support
- `paper-reader-template.html` available at:
  - `/mnt/skills/user/paper-reader/paper-reader-template.html` (preferred), or
  - uploaded manually to the conversation
- For **AI Chat** tab: an [Anthropic API key](https://console.anthropic.com/)

## 📊 Output Quality Standards

The skill enforces strict quality on every extraction:

- **Findings** must be specific and citable — no generic statements like "AI can be helpful"
- **AI-EdTech Implications** must name concrete design decisions, tradeoffs, or risks
- **Elevator Pitch** answers "so what?" not "what is this paper about"
- **Weaknesses** explain what the limitation *prevents us from concluding*
- **Quiz** always includes at least one methodology, one findings, and one critical-thinking question

## 🧠 Designed For

- Researchers processing large paper corpora
- Students preparing for seminars or literature reviews
- AI-EdTech product designers extracting design insights
- Anyone who wants to go beyond passive reading

## 📄 License

MIT
