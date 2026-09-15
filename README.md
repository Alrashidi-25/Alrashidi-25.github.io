# Abdulrahman Alrashidi — Portfolio

Personal portfolio site for **Abdulrahman Manawer Alrashidi** — Computer Information Systems
senior at King Faisal University, working toward a career as a Systems & Business Analyst.

## Live preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

## Sections

- **Hero** — headline, profile snapshot, quick links
- **About** — background and how the pieces fit together
- **Focus** — Systems & Requirements → Business Analysis → Data & BI → Delivery & Security
- **Projects** — Ruaa (CSV analysis engine), Masar (GPA planner) and the senior capstone project
- **Skills** — business analysis, data & BI, project management, cybersecurity, programming, cloud & AI
- **Experience** — virtual job simulations with BCG, Siemens, stc, Microsoft, Accenture and Misk
- **Certifications** — nine verified certificates with image and PDF viewers
- **Education** — King Faisal University, CIS
- **Contact** — email, LinkedIn, GitHub

## Structure

```
.
├── index.html            # the portfolio
├── style.css
├── script.js             # nav, scroll reveals, counters, lightbox
├── masar/                # the GPA planner project (see masar/README.md)
└── assets/
    └── certs/            # certificate images (.jpg) and originals (pdf/)
```

## Things to fill in

1. **Profile photo** — drop the image in `assets/` and swap the monogram block in the About
   section (there's a comment in `index.html` marking the exact spot).
2. **Graduation project** — the second project card has a placeholder comment; add the title,
   the problem, your role, the tools and a screenshot.
3. **CV** — `assets/Abdulrahman_Alrashidi_CV.pdf` is the public copy (phone number left out on
   purpose). Replace the file to update it; the nav, hero and contact links all point to it.

## Related repos

| Project | Repo | Live |
|---|---|---|
| Ruaa — in-browser CSV analysis | [Alrashidi-25/ruaa](https://github.com/Alrashidi-25/ruaa) | [alrashidi-25.github.io/ruaa](https://alrashidi-25.github.io/ruaa/) |
| Masar — GPA planner | [Alrashidi-25/masar](https://github.com/Alrashidi-25/masar) | [alrashidi-25.github.io/masar](https://alrashidi-25.github.io/masar/) |

> `masar/` is also vendored in this repo so its "Open Live Demo" button works from the
> portfolio itself; if you change one copy, copy the files across. Ruaa is linked to its
> own Pages site rather than vendored.

## Tech

HTML5, CSS3 (custom properties, grid, flexbox) and vanilla JavaScript. No frameworks, no build
step, no dependencies.

## Contact

[Email](mailto:a.alrashiddi@gmail.com) ·
[LinkedIn](https://www.linkedin.com/in/abdulrahman-alrashidi-9b9543249/) ·
[GitHub](https://github.com/Alrashidi-25)
