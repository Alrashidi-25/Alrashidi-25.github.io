# مسار · Masar — Academic GPA Planner

A free, Arabic-first web app that helps Saudi university students calculate, understand and
**plan** their GPA. No account, no server, no internet required — everything runs in the browser
and is stored on the student's own device.

**[Live demo](https://alrashidi-25.github.io/masar/)** · Built by [Abdulrahman Alrashidi](https://www.linkedin.com/in/abdulrahman-alrashidi-9b9543249/)

---

## The problem

Students guess at their GPA, lose track of it across semesters, and have no straightforward way
to answer the one question that actually matters when planning a term:

> "What average do I need **this semester** to reach the cumulative GPA I want?"

Most calculators online stop at "here is your semester GPA". Masar works backwards from the goal.

## What it does

| Feature | Detail |
|---|---|
| **Dual-scale engine** | Full 5.00 and 4.00 Saudi grade scales (A+ → F) with official grade bands |
| **Semester GPA** | Live calculation as courses are entered, with the standing (ممتاز / جيد جداً / …) |
| **Cumulative GPA** | Combines the current term with prior credits, or with saved semesters automatically |
| **Target solver** | Enter a target cumulative GPA → get the exact term average required, plus a feasibility verdict |
| **Semester tracking** | Save each term; cumulative GPA and the trend chart roll up automatically |
| **Grade distribution** | Visual breakdown of how many courses landed on each grade |
| **CSV export** | Exports with a UTF-8 BOM so Arabic opens correctly in Excel |
| **Privacy** | `localStorage` only — nothing is transmitted anywhere |

## The math

Grade points are credit-weighted:

```
termGPA = Σ(credits × gradePoints) / Σ(credits)

cumulativeGPA = (priorPoints + termPoints) / (priorCredits + termCredits)
```

The target solver rearranges the cumulative formula to isolate the unknown term GPA:

```
required = (targetGPA × (priorCredits + termCredits) − priorPoints) / termCredits
```

If `required` exceeds the scale maximum the goal isn't reachable in a single term, and the app
says so instead of printing an impossible number.

## Grade scales

| Grade | Score | 5.00 scale | 4.00 scale |
|---|---|---|---|
| A+ | 95–100 | 5.00 | 4.00 |
| A  | 90–94  | 4.75 | 3.75 |
| B+ | 85–89  | 4.50 | 3.50 |
| B  | 80–84  | 4.00 | 3.00 |
| C+ | 75–79  | 3.50 | 2.50 |
| C  | 70–74  | 3.00 | 2.00 |
| D+ | 65–69  | 2.50 | 1.50 |
| D  | 60–64  | 2.00 | 1.00 |
| F  | < 60   | 1.00 | 0.00 |

## Tech

Plain HTML, CSS and JavaScript — no framework, no build step, no dependencies.

```
masar/
├── index.html   # RTL Arabic markup
├── style.css    # dark theme, responsive down to 320px
└── app.js       # grade scales, GPA engine, target solver, persistence
```

## Running it

Open `index.html` in any browser, or serve the folder:

```bash
python3 -m http.server 8000
```

## License

MIT — free to use, fork and adapt.
