# Gumroad listing draft — CSV Clean (draft for the captain)

Status: DRAFT — every claim below is grounded in product/csv-cleaner/README.md
and engine.js as read this run; nothing invented. Captain reviews price/copy.

## Title
**CSV Clean — fix your messy CSVs locally. One payment. Your data never leaves your machine.**

## Subtitle
Whitespace chaos, US-date mixups, duplicate rows, phantom empty columns —
cleaned in your browser in seconds. No install, no account, no upload, no
subscription.

## Body copy
Most CSV cleaners are SaaS: you upload your data to someone else's server and
pay every month ($185–$250 per user per month in this category).

CSV Clean runs **entirely in your browser**. Double-click `index.html`, drop
your file, read the report, download the clean file. Works offline. Your file
is never uploaded anywhere — it never leaves your machine.

### What it fixes
- Leading/trailing whitespace in every cell (collapses double spaces too)
- US dates `M/D/YYYY` → ISO `YYYY-MM-DD`
- Exact duplicate rows (after trimming) — keeps the first occurrence
- Entirely empty columns
- BOM characters and ragged rows (short rows padded, blank lines skipped)

### What it protects
- Leading zeros in zips/IDs — cells stay strings, nothing is coerced to a number
- Quoted fields, escaped quotes (`""`), commas and newlines inside quotes
- A report of exactly what changed: rows in/out, cells trimmed, dupes
  removed, dates fixed, empty columns dropped

### Honest limits (also in the README)
- Comma-delimited only — export semicolon/tab files as CSV first
- Date fix covers `M/D/YYYY` only; other formats pass through untouched
- Dedupe is exact-match (`"John"` vs `"john"` are different rows)

### Who this is for
Analysts, marketers, e-commerce sellers, and developers who just need their
CSVs clean and private — without a monthly bill or a data-privacy leap of faith.

### What's included
- `index.html` (the app) + `engine.js` (cleaning engine, also callable from Node)
- One-time purchase, yours forever

## Price
**$19 — one time.**
(Anchor, verifiable: WinPure Small Business $185/user/mo; ovaledge Starter
$250/user/mo — under one-tenth of one month, forever.)

## Tags / category
Software · Data tools · Productivity
