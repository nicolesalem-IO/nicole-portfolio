"""Generates the static site into ../public from content.py.

Run:  python3 build/build.py
Edit project text in build/content.py, then re-run and commit.
"""
import html
import os
import shutil

from content import ABOUT_IMG, CATEGORIES, HEADSHOT, LINKEDIN, PROJECTS, RESUME

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
SITE_URL = "https://nicolesalem.com"
REPORTS = os.path.join(ROOT, "build", "reports")

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ')
ARROW = SVG + 'class="h-4 w-4" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>'
BACK = SVG + 'class="h-4 w-4" aria-hidden="true"><path d="m12 19-7-7 7-7"></path><path d="M19 12H5"></path></svg>'
MENU = SVG + 'class="icon-menu h-6 w-6" aria-hidden="true"><line x1="4" x2="20" y1="12" y2="12"></line><line x1="4" x2="20" y1="6" y2="6"></line><line x1="4" x2="20" y1="18" y2="18"></line></svg>'
CLOSE = SVG + 'class="icon-close hidden h-6 w-6" aria-hidden="true"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>'
LINKEDIN_ICON = SVG + 'class="h-4 w-4" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect width="4" height="12" x="2" y="9"></rect><circle cx="4" cy="4" r="2"></circle></svg>'

e = html.escape


def nav_link(href, label, active, mobile=False):
    cur = ' aria-current="page"' if active else ""
    if mobile:
        return f'<a class="text-lg{" text-primary" if active else ""}" href="{href}"{cur}>{label}</a>'
    cls = "text-[0.78rem] font-semibold uppercase tracking-[0.16em] transition-colors hover:text-primary " + ("text-primary" if active else "text-foreground/70")
    return f'<a class="{cls}" href="{href}"{cur}>{label}</a>'


def page(path, title, description, main, section):
    links = [("/", "Home", "home"), ("/projects", "Projects", "projects"), ("/about", "About", "about")]
    desktop = "".join(nav_link(h, l, s == section) for h, l, s in links)
    mobile = "".join(nav_link(h, l, s == section, True) for h, l, s in links)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{HEADSHOT}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&amp;display=swap">
<link rel="stylesheet" href="/styles.css">
<script src="/site.js" defer></script>
</head>
<body>
<div class="flex min-h-screen flex-col border-t-[6px] border-[#facc15]">
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-background focus:p-3">Skip to content</a>
<header class="sticky top-0 z-30 border-b border-foreground/15 bg-background/90 backdrop-blur">
<div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
<a class="group flex items-center gap-3" href="/"><span class="h-3 w-3 rounded-[4px] bg-[#ec4899] transition-transform duration-300 group-hover:rotate-45" aria-hidden="true"></span><span class="font-heading text-xl font-semibold tracking-tight">Nicole Salem</span></a>
<nav aria-label="Main" class="hidden items-center gap-9 md:flex">{desktop}</nav>
<button type="button" id="menu-toggle" class="-mr-2 rounded-sm p-2 transition-colors hover:bg-secondary md:hidden" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">{MENU}{CLOSE}</button>
</div>
<nav id="mobile-nav" aria-label="Main" class="hidden flex-col gap-4 border-t border-foreground/15 px-6 py-5 md:hidden">{mobile}</nav>
</header>
<main id="main" class="flex-1">
{main}
</main>
<footer class="border-t border-foreground/15 bg-secondary/70">
<div class="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-10 sm:flex-row sm:items-center sm:justify-between">
<div><p class="font-heading text-lg font-semibold">Nicole Salem</p><p class="mt-1 text-sm text-foreground/70">Operations &amp; People Leadership · Industrial-Organizational Psychology</p></div>
<div class="flex flex-wrap items-center gap-x-6 gap-y-3 text-sm font-medium"><a class="transition-colors hover:text-primary" href="/projects">Projects</a><a class="transition-colors hover:text-primary" href="/about">About</a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 transition-colors hover:text-primary">{LINKEDIN_ICON} LinkedIn</a></div>
</div>
</footer>
</div>
</body>
</html>
"""


def card(p):
    url = f"/projects/{p['slug']}"
    img = (f'<img alt="" class="mb-5 h-44 w-full border border-foreground/10 object-cover" src="{p["card_image"]}" loading="lazy">'
           if p.get("card_image") else "")
    return (f'<article class="card-tint flex h-full flex-col border border-foreground/20 bg-background p-6">{img}'
            f'<p class="text-[0.7rem] font-semibold uppercase tracking-[0.16em] text-primary">{e(p["category"])}</p>'
            f'<p class="mt-1.5 text-sm text-foreground/65">{e(p["eyebrow"])}</p>'
            f'<h3 class="mt-3 text-2xl leading-snug"><a class="transition-colors hover:text-primary" href="{url}">{e(p["title"])}</a></h3>'
            f'<p class="mt-3 text-base text-foreground/80">{e(p["summary"])}</p>'
            f'<a class="link-arrow mt-auto inline-flex items-center gap-2 pt-6 font-medium text-primary" href="{url}">View project {ARROW}'
            f'<span class="sr-only">: {e(p["title"])}</span></a></article>')


def home():
    featured = "".join(card(p) for p in PROJECTS[:3])
    return f"""<div class="pb-14"><section class="mx-auto max-w-[92rem] px-5 md:px-8"><h1 class="drift-in mt-6 text-[18vw] font-extrabold uppercase leading-[0.8] tracking-[-0.045em] sm:mt-10 sm:text-[11vw]">Nicole<br class="sm:hidden"><span class="hidden sm:inline"> </span>Salem</h1><div class="mt-8 grid items-start gap-8 border-t border-foreground/25 pt-8 sm:mt-12 sm:gap-10 md:grid-cols-[1.1fr_1fr] md:pt-12 lg:gap-16"><img alt="Nicole Salem" class="aspect-[2/3] w-full object-cover" src="{HEADSHOT}"><div><p class="text-xs font-bold uppercase leading-[1.9] tracking-[0.24em] sm:text-sm">Operations &amp; People Leadership<br>Industrial-Organizational Psychology</p><p class="mt-6 text-lg leading-relaxed text-foreground/85 sm:mt-8 sm:text-xl">For years, my work has been leading teams and finding ways to make work run better. Now, as a master’s student in Industrial-Organizational Psychology, I’m bringing research to the questions every leader eventually faces.</p><p class="mt-4 text-base leading-relaxed text-foreground/65">How do we train people for the work they actually do? How do we make hiring decisions more consistent? How do we tell whether a change is helping?</p><div class="mt-8 flex flex-wrap items-center gap-x-6 gap-y-4 border-t border-foreground/15 pt-6"><a class="btn btn-solid" href="/projects">Explore my projects {ARROW}</a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" class="ulink font-semibold">Connect on LinkedIn</a></div></div></div></section>
<section aria-labelledby="featured" class="mx-auto mt-14 max-w-[92rem] border-t border-foreground/25 px-5 py-10 md:mt-20 md:px-8 md:py-14"><div class="flex flex-wrap items-end justify-between gap-4"><h2 id="featured" class="text-3xl font-extrabold uppercase tracking-[-0.035em] sm:text-5xl">Selected work</h2><a class="link-arrow inline-flex items-center gap-2 text-sm font-bold uppercase tracking-[0.16em]" href="/projects">All projects {ARROW}</a></div><div class="mt-8 grid gap-5 sm:mt-10 md:grid-cols-2 lg:grid-cols-3">{featured}</div></section></div>"""


def projects():
    btn = "border px-4 py-2 text-sm font-medium transition-colors"
    buttons = f'<button type="button" aria-pressed="true" data-filter="all" class="{btn}">All projects</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-filter="{e(c)}" class="{btn}">{e(c)}</button>' for c in CATEGORIES)
    cards = "".join(
        f'<div class="drift-in" data-category="{e("|".join(p.get("categories", [p["category"]])))}" style="animation-delay: {i * 60}ms;">{card(p)}</div>'
        for i, p in enumerate(PROJECTS))
    return f"""<div><header class="mx-auto max-w-6xl px-6 pt-14 pb-10 md:pt-20 md:pb-14"><p class="eyebrow drift-in">Selected work</p><h1 class="drift-in mt-5 text-5xl leading-[0.98] md:text-6xl lg:text-7xl">Projects</h1><p class="drift-in mt-6 max-w-3xl text-xl leading-relaxed text-foreground/85 md:text-2xl">A collection of my graduate work, independent apps, and applied projects across training, assessment, organizational development, and research.</p></header><div class="sticky top-[4.5rem] z-20 border-y border-foreground/15 bg-background/95 backdrop-blur"><div class="mx-auto max-w-6xl px-6 py-4"><div role="group" aria-label="Filter projects by skill" id="project-filters" class="flex flex-wrap gap-2">{buttons}</div></div></div><div class="mx-auto max-w-6xl px-6"><p class="pt-8 text-sm font-medium uppercase tracking-[0.16em] text-foreground/60" id="project-count">{len(PROJECTS)} projects</p><div class="grid gap-6 pb-20 pt-6 md:grid-cols-2 lg:grid-cols-3" aria-live="polite" id="project-grid">{cards}</div></div></div>"""


def about():
    return f"""<div class="mx-auto max-w-6xl px-6 pb-20 pt-14 md:pt-20"><p class="eyebrow drift-in">About</p><h1 class="drift-in mt-5 text-5xl leading-[0.98] md:text-7xl">Hello, I’m <span class="accent-underline">Nicole</span></h1><div class="mt-10 grid items-start gap-12 lg:grid-cols-[1.2fr_0.8fr] lg:gap-16"><div class="max-w-2xl"><p class="text-xl leading-relaxed text-foreground/90 md:text-2xl">Finance, operations, and people leadership make up my background: leading teams, building training, and working through the day-to-day challenges of a growing business.</p><p class="mt-5 text-lg leading-relaxed text-foreground/80">At Marian University, a master’s in Industrial-Organizational Psychology is giving that experience a research foundation through work in training, assessment, and applied research. Next, I want to bring both into people operations and organizational development in healthcare or education.</p><div class="mt-10 flex flex-wrap gap-4"><a href="{RESUME}" target="_blank" rel="noopener noreferrer" class="btn btn-solid">View résumé {ARROW}</a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" class="btn btn-line">Connect on LinkedIn</a></div></div><div class="relative mx-auto w-full max-w-sm lg:mx-0 lg:max-w-none"><div class="brand-gradient absolute -inset-3 rotate-3 rounded-[2rem]" aria-hidden="true"></div><img alt="Nicole Salem" class="relative aspect-[1199/1312] w-full rounded-[2rem] object-cover" src="{ABOUT_IMG}"></div></div></div>"""


def detail(p):
    extra = f'<div class="mt-8">{p["header_extra"]}</div>' if p.get("header_extra") else ""
    def report(name):
        with open(os.path.join(REPORTS, name + ".html"), encoding="utf-8") as f:
            return f.read()

    sections_list = list(p["sections"])
    sections = "".join(
        f'<section class="border-t border-foreground/15 py-10 md:py-12"><div class="flex items-center gap-3">'
        f'<span class="h-3 w-3 shrink-0 rounded-full bg-[#facc15]" aria-hidden="true"></span><h2 class="text-2xl md:text-3xl">{e(t)}</h2></div>'
        f'<div class="mt-5 text-lg leading-relaxed text-foreground/90">{body}</div></section>'
        for t, body in sections_list if t != "Recommendation or status")
    sections += "".join(report(r) for r in p.get("reports", []))
    sections += "".join(
        f'<section class="border-t border-foreground/15 py-10 md:py-12"><div class="flex items-center gap-3">'
        f'<span class="h-3 w-3 shrink-0 rounded-full bg-[#facc15]" aria-hidden="true"></span><h2 class="text-2xl md:text-3xl">{e(t)}</h2></div>'
        f'<div class="mt-5 text-lg leading-relaxed text-foreground/90">{body}</div></section>'
        for t, body in sections_list if t == "Recommendation or status")
    return (f'<article class="mx-auto max-w-3xl px-6 pb-20"><a class="mt-8 inline-flex items-center gap-2 text-sm font-medium text-foreground/70 transition-colors hover:text-primary" href="/projects">{BACK} Back to projects</a>'
            f'<header class="drift-in border-b border-foreground/15 py-10 md:py-14"><p class="eyebrow">{e(p["eyebrow"])}</p>'
            f'<h1 class="mt-5 text-4xl leading-[1.05] md:text-6xl">{e(p["title"])}</h1>'
            f'<ul class="mt-6 flex flex-wrap gap-2" aria-label="Skills">'
            + "".join(f'<li class="border border-primary/35 bg-primary/5 px-3 py-1 text-[0.7rem] font-semibold uppercase tracking-[0.14em] text-primary">{e(c)}</li>' for c in p.get("categories", [p["category"]]))
            + '</ul>'
            f'<p class="mt-6 text-xl leading-relaxed text-foreground/90 md:text-2xl">{e(p["summary"])}</p>{extra}</header>{sections}</article>')


def not_found():
    return f"""<div class="mx-auto max-w-3xl px-6 pb-20 pt-14 md:pt-20"><p class="eyebrow">404</p><h1 class="mt-5 text-5xl leading-[0.98] md:text-6xl">Page not found</h1><p class="mt-6 text-xl leading-relaxed text-foreground/85">That page doesn’t exist. It may have moved.</p><div class="mt-10"><a class="btn btn-solid" href="/">Go to the home page {ARROW}</a></div></div>"""


def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for asset in ("styles.css", "site.js", "favicon.svg"):
        shutil.copy(os.path.join(ROOT, "assets", asset), OUT)
    if os.path.isdir(os.path.join(ROOT, "media")):
        shutil.copytree(os.path.join(ROOT, "media"), os.path.join(OUT, "media"))

    write("index.html", page("/", "Nicole Salem · Operations & People Leadership",
                             "Portfolio of Nicole Salem: Operations & People Leadership · Industrial-Organizational Psychology.",
                             home(), "home"))
    write("projects/index.html", page("/projects", "Projects · Nicole Salem",
                                      "Graduate work, independent apps, and applied projects across training, assessment, organizational development, and research.",
                                      projects(), "projects"))
    write("about/index.html", page("/about", "About Nicole · Nicole Salem",
                                   "Background in finance, operations, and people leadership, now studying Industrial-Organizational Psychology.",
                                   about(), "about"))
    for p in PROJECTS:
        write(f"projects/{p['slug']}/index.html",
              page(f"/projects/{p['slug']}", f"{p['title']} · Nicole Salem", p["summary"], detail(p), "projects"))
    write("404.html", page("/404", "Page not found · Nicole Salem", "Page not found.", not_found(), ""))

    urls = ["/", "/projects", "/about"] + [f"/projects/{p['slug']}" for p in PROJECTS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print(f"Built {len(urls) + 1} pages into {OUT}")


if __name__ == "__main__":
    main()
