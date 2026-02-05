# vault-insight

**vault-insight** is a command-line tool that analyzes an Obsidian vault to help you understand and improve how your notes are structured.

Instead of pulling information from the internet or suggesting new content, it looks only at your own notes and highlights structural issues such as:

- notes that should probably be linked
- notes that overlap and may need consolidation
- notes worth revisiting based on recent study activity (planned)

The goal is to help you keep a clean, intentional knowledge base as it grows.

---

## Why this exists

As a note collection grows, structure naturally starts to break down:

- related ideas stay unlinked
- drafts and final notes drift apart
- similar explanations get rewritten instead of reused

Most tools rely on manual tags or explicit backlinks. **vault-insight** looks for hidden relationships by analyzing how ideas appear across your notes.

It is meant to support decisions, not automate them.

---

## What it does (currently)

### Detect missing links

Finds pairs of notes that talk about similar ideas but are not explicitly connected.

```bash
vault-insight links
```

**Example output:**

```
FROM : SQL.md
TO   : Databases.md
SCORE: 0.87

--- Evidence from SQL.md ---
Data is stored in tables (rows and columns)
Uses SQL (Structured Query Language)

--- Evidence from Databases.md ---
Structured (SQL, relational)
Uses SQL to interact with data
```

This suggests that these notes are closely related and may benefit from a link.

No content is modified and no links are created automatically.

### Detect merge or consolidation candidates

Identifies notes that share a large amount of similar content and may represent drafts, duplicates, or accidental splits.

```bash
vault-insight merge
```

**Example output:**

```
NOTE A : (DRAFT) Writing Critique.md
NOTE B : Writing Critique.md
SCORE  : 0.98
SHARED SEGMENTS : 12
```

The tool shows overlapping sections so you can quickly decide whether the notes should be merged or kept separate.

---

## Planned feature

### Temporal recall (today)

Highlights notes that may be worth revisiting based on what you studied recently.

```bash
vault-insight today
```

**Planned example:**

```
You studied ENSF 337

Revisit:
  • Heap vs Stack (last seen 3 weeks ago)
  • Memory leaks (never summarized)
```

This feature is intended to be lightweight and helpful, not a full study or flashcard system.

---

## How it works (high level)

```
Obsidian Vault
       ↓
Notes are ingested and parsed
       ↓
Notes are split into smaller segments
       ↓
Each segment is converted into a semantic embedding
       ↓
Similar segments are compared
       ↓
Results are grouped at the note level
       ↓
Signals are generated:
  • missing links
  • merge or consolidation candidates
```

**Key design choices:**

- segments are analyzed instead of entire notes
- embeddings are computed locally
- links are treated as structure, not discovery
- results always include readable evidence

---

## What this tool does not do

- does not fetch information from the internet
- does not edit notes automatically
- does not force merges or restructuring
- does not replace intentional note design

It simply asks:

> Does the structure of this vault still reflect how these ideas relate to each other?

---

## Usage

After installation:

```bash
vault-insight build
vault-insight links
vault-insight merge
```

The tool is installed as a native command, so it can be run directly from the terminal without invoking Python scripts.

---

## Why this project is interesting

This project focuses on **structure** rather than **content**.

It explores how embeddings and similarity can be used to understand a personal knowledge base and surface issues that are easy to miss as notes accumulate.

The emphasis is on clarity, boundaries, and intentional organization.
