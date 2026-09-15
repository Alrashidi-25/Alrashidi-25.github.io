# Abdulrahman Alrashidi — Portfolio

Personal portfolio site for **Abdulrahman Manawer Alrashidi** — Computer Information Systems
senior at King Faisal University, working toward a career as a Systems & Business Analyst.

Available in English and Arabic: [alrashidi-25.github.io](https://alrashidi-25.github.io) ·
[alrashidi-25.github.io/ar](https://alrashidi-25.github.io/ar/)

## Live preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

## Sections

- **Hero** — headline, profile snapshot, quick links
- **About** — background and how the pieces fit together
- **Focus** — Systems & Requirements → Business Analysis → Data & BI → Delivery & Security
- **Projects** — Jisr (business analysis, database and Power BI), Ruaa (CSV analysis engine), Masar (GPA planner) and the senior capstone project
- **Skills** — business analysis, data & BI, project management, cybersecurity, programming, cloud & AI
- **Experience** — virtual job simulations with BCG, Siemens, stc, Microsoft, Accenture and Misk
- **Certifications** — twelve certificates with image and PDF viewers
- **Workshops** — university bootcamps, workshops and campus activities
- **Education** — King Faisal University, CIS
- **Contact** — email, LinkedIn, GitHub

## Structure

```
.
├── index.html            # the portfolio (English — the source of truth)
├── ar/index.html         # Arabic page, generated from index.html
├── style.css
├── ar.css                # right-to-left overrides and Arabic fonts for ar/
├── script.js             # nav, scroll reveals, counters, lightbox
├── 404.html              # custom not-found page
├── tools/build_ar.py     # regenerates ar/index.html
└── assets/
    ├── certs/            # certificate images (.jpg), originals (pdf/) and workshops/
    └── projects/         # project preview images
```

## Editing

Edit `index.html`, then regenerate the Arabic page:

```bash
python3 tools/build_ar.py
```

The script holds the Arabic for every English string. If a string in `index.html` changes, it stops
and prints the ones that need a new translation.

## Things to fill in

1. **Profile photo** — drop the image in `assets/` and swap the monogram block in the About
   section (there's a comment in `index.html` marking the exact spot).
2. **Graduation project** — the last project card has a placeholder comment; add the title,
   the problem, your role, the tools and a screenshot.
3. **CV** — `assets/Abdulrahman_Alrashidi_CV.pdf` is the public copy (phone number left out on
   purpose). Replace the file to update it; the nav, hero and contact links all point to it.

## Related repos

| Project | Repo | Live |
|---|---|---|
| Ruaa — in-browser CSV analysis | [Alrashidi-25/ruaa](https://github.com/Alrashidi-25/ruaa) | [alrashidi-25.github.io/ruaa](https://alrashidi-25.github.io/ruaa/) |
| Masar — GPA planner | [Alrashidi-25/masar](https://github.com/Alrashidi-25/masar) | [alrashidi-25.github.io/masar](https://alrashidi-25.github.io/masar/) |
| Jisr — business analysis case study | [Alrashidi-25/jisr-business-analysis](https://github.com/Alrashidi-25/jisr-business-analysis) | [alrashidi-25.github.io/jisr-business-analysis](https://alrashidi-25.github.io/jisr-business-analysis/) |
| Jisr — database & SQL | [Alrashidi-25/jisr-database](https://github.com/Alrashidi-25/jisr-database) | |
| Jisr — Power BI dashboard | [Alrashidi-25/jisr-powerbi](https://github.com/Alrashidi-25/jisr-powerbi) | |

The projects live in their own repos and are served by GitHub Pages under this domain.

## Tech

HTML5, CSS3 (custom properties, grid, flexbox) and vanilla JavaScript. No frameworks and no
dependencies; the only script is the Python one that generates the Arabic page.

## Contact

[Email](mailto:a.alrashiddi@gmail.com) ·
[LinkedIn](https://www.linkedin.com/in/abdulrahman-alrashidi-9b9543249/) ·
[GitHub](https://github.com/Alrashidi-25)
