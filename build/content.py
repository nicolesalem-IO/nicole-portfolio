from html import escape as e

HEADSHOT = "/media/nicole-hero.webp"
ABOUT_IMG = "/media/nicole-about.webp"
RESUME = "/media/Nicole-Salem-Resume.pdf"
LINKEDIN = "https://www.linkedin.com/in/nicole-salem-hr/"
OYP_BRAND = "/media/own-your-presence-brand.webp"

CATEGORIES = [
    "Training & Development",
    "Data & Analytics",
    "Selection & Assessment",
    "Performance Management",
    "Leadership & Organizational Development",
    "Compensation & Global Mobility",
    "Applied Research",
    "Apps & Workflow Design",
]


# ---------- building blocks ----------

def pdfs(*links):
    return '<div class="mt-6 flex flex-wrap gap-3">' + "".join(links) + "</div>"


def quote(text):
    return ('<blockquote class="ml-4 border-l-2 border-primary pl-6 font-heading text-xl italic md:text-2xl">'
            + text + "</blockquote>")


def related(slug, title):
    return (f'<ul class="space-y-3"><li><a class="ulink font-medium text-primary" '
            f'href="/projects/{slug}">{title}</a></li></ul>')


def demo(url):
    return (f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            f'class="btn btn-solid">Visit the live demo</a>')


def caption(text):
    return f'<figcaption class="fig-caption">{text}</figcaption>'


def table(headers, rows, cap):
    head = "".join(f"<th scope=\"col\">{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(
        (f'<th scope="row">{e(c)}</th>' if i == 0 else f"<td>{e(c)}</td>") for i, c in enumerate(r)) + "</tr>"
        for r in rows)
    return (f'<figure class="fig"><div class="table-wrap"><table class="data-table"><thead><tr>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>{caption(cap)}</figure>")


def steps(items, cap):
    lis = "".join(f'<li><span class="step-name">{e(t)}</span><span class="step-text">{e(d)}</span></li>'
                  for t, d in items)
    return f'<figure class="fig"><ol class="steps">{lis}</ol>{caption(cap)}</figure>'


def tiers(groups, cap):
    cols = "".join(
        f'<div class="tier tier-{level.lower()}"><p class="tier-label">{level} risk</p><ul>'
        + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul></div>"
        for level, items in groups)
    return f'<figure class="fig"><div class="tiers">{cols}</div>{caption(cap)}</figure>'


def cards(items, cap):
    inner = "".join(f'<div class="mini-card"><p class="mini-title">{e(t)}</p><p>{e(d)}</p></div>' for t, d in items)
    return f'<figure class="fig"><div class="mini-cards">{inner}</div>{caption(cap)}</figure>'


def callout(label, text):
    return f'<aside class="callout"><p class="callout-label">{e(label)}</p><p>{e(text)}</p></aside>'


def bars(rows, cap, label):
    """Horizontal bar chart on a 0-1 scale. rows: (name, value or None, note)."""
    w, left, right, rh = 640, 230, 70, 44
    h = rh * len(rows) + 34
    plot = w - left - right
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="{e(label)}">']
    for t in (0, .25, .5, .75, 1):
        x = left + plot * t
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="0" y2="{h-26}" class="grid"/>'
                   f'<text x="{x:.1f}" y="{h-8}" class="tick" text-anchor="middle">{"0" if t == 0 else ("1" if t == 1 else f"{t:.2f}".lstrip("0"))}</text>')
    for i, (name, val, note) in enumerate(rows):
        y = i * rh + 10
        out.append(f'<text x="{left-12}" y="{y+17}" class="lbl" text-anchor="end">{e(name)}</text>')
        if val is None:
            out.append(f'<text x="{left+6}" y="{y+17}" class="note">{e(note)}</text>')
        else:
            bw = plot * val
            cls = "bar bar-weak" if note == "weak" else "bar"
            out.append(f'<g class="hit"><title>{e(name)}: {val:.2f}</title>'
                       f'<rect x="{left}" y="{y+4}" width="{bw:.1f}" height="18" rx="3" class="{cls}"/>'
                       f'<text x="{left+bw+8:.1f}" y="{y+18}" class="val">{f"{val:.2f}".lstrip("0")}</text></g>')
    out.append("</svg>")
    return f'<figure class="fig chart-fig">{"".join(out)}{caption(cap)}</figure>'


def sem_chart(cands, cutoff, sem, cap):
    w, left, right, rh = 640, 120, 30, 46
    lo, hi = 55, 90
    h = rh * len(cands) + 60
    plot = w - left - right
    X = lambda v: left + (v - lo) / (hi - lo) * plot
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Candidate scores with plus or minus one standard error of measurement, and the cutoff of {cutoff}">']
    for t in range(lo, hi + 1, 5):
        out.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="20" y2="{h-26}" class="grid"/>'
                   f'<text x="{X(t):.1f}" y="{h-8}" class="tick" text-anchor="middle">{t}</text>')
    out.append(f'<line x1="{X(cutoff):.1f}" x2="{X(cutoff):.1f}" y1="14" y2="{h-26}" class="cutoff"/>'
               f'<text x="{X(cutoff)+6:.1f}" y="14" class="cut-lbl">Cutoff {cutoff}</text>')
    for i, (name, score) in enumerate(cands):
        y = 40 + i * rh
        a, b = score - sem, score + sem
        out.append(f'<text x="{left-14}" y="{y+5}" class="lbl" text-anchor="end">{e(name)}</text>'
                   f'<g class="hit"><title>{e(name)}: {score} (likely range {a:.1f} to {b:.1f})</title>'
                   f'<rect x="{X(a):.1f}" y="{y-7}" width="{X(b)-X(a):.1f}" height="14" rx="7" class="band"/>'
                   f'<circle cx="{X(score):.1f}" cy="{y}" r="5.5" class="dot"/>'
                   f'<text x="{X(b)+8:.1f}" y="{y+5}" class="val">{score}</text></g>')
    out.append("</svg>")
    return f'<figure class="fig chart-fig">{"".join(out)}{caption(cap)}</figure>'


def shots(items, cap):
    imgs = "".join(f'<img src="/media/{src}" alt="{e(alt)}" loading="lazy" width="540">' for src, alt in items)
    return f'<figure class="fig"><div class="shots">{imgs}</div>{caption(cap)}</figure>'


def local_pdf(file, label):
    return (f'<a href="/media/{file}" target="_blank" rel="noopener noreferrer" '
            f'class="btn btn-line text-base">{label}</a>')

def p(text):
    return f"<p>{text}</p>"


# ---------- projects ----------
# Order matches the Projects page. The first three are featured on Home.
PROJECTS = [
    {
        "slug": "supervisor-coaching-healthcare-clinic",
        "reports": ["supervisor-coaching-healthcare-clinic-1"],
        "category": "Training & Development",
        "eyebrow": "Graduate training design and evaluation plan",
        "title": "Designing Supervisor Coaching for a Healthcare Clinic",
        "summary": "A coaching program that helps clinic supervisors turn recurring documentation errors into clear, consistent feedback conversations.",
        "sections": [
            ("The question", quote("The clinic’s front-line employees received feedback when documentation mistakes occurred, yet similar errors kept coming up. How could supervisors make that feedback more useful and follow up consistently?")),
            ("What the needs analysis found",
             callout("Not a knowledge gap", "Documentation procedures were already in place, and staff had been trained on them. The gap sat with supervisors: many had been promoted for clinical expertise and had little practice giving corrective feedback, documenting coaching, or following up.")),
            ("My approach",
             p("A two-hour workshop built around the coaching conversations supervisors actually have on the job. Each performance gap maps to a learning objective, a practice activity, and a way to measure it.")
             + table(["Performance need", "Learning objective", "Activity", "Evaluation"], [
                 ["Errors are addressed inconsistently", "Identify communication breakdowns behind recurring errors", "Error case discussion", "Knowledge check"],
                 ["Feedback relies on informal verbal reminders", "Run a corrective feedback conversation that covers the issue, expectations, and next steps", "Facilitated role-play", "Observation checklist"],
                 ["Feedback discussions go undocumented", "Complete a coaching documentation form accurately", "Documentation practice", "Form review"],
                 ["Follow-up after feedback is inconsistent", "Build a follow-up plan that reinforces expectations", "Action planning", "Follow-up plan review"],
             ], "Training alignment table, adapted from Appendix A of the course plan.")
             + steps([
                 ("Prepare", "Identify the issue, gather an example, review the standard."),
                 ("Describe", "State the concern using observable behavior."),
                 ("Explain impact", "Connect it to workflow, patient care, or compliance."),
                 ("Clarify", "Say what needs to change and confirm understanding."),
                 ("Invite input", "Ask questions and surface barriers."),
                 ("Set next steps", "Agree on actions and a follow-up date."),
                 ("Follow up", "Document the talk, monitor progress, review improvement."),
             ], "The seven-step corrective feedback job aid supervisors take back to the floor (Appendix C).")),
            ("Recommendation or status", p("Evaluation centers on one question: are supervisors using the feedback process consistently, and is it reducing documentation-related issues? Managers hold weekly check-ins during the first month, and documentation trends get reviewed 60 to 90 days after launch.")),
        ],
    },
    {
        "slug": "hiring-system-implementation-consultants",
        "reports": ["hiring-system-implementation-consultants-1"],
        "category": "Selection & Assessment",
        "eyebrow": "Graduate assessment memo",
        "title": "Evaluating a Hiring System for Healthcare Implementation Consultants",
        "summary": "A review of a proposed hiring system, with recommendations to make interview scoring more consistent and decisions near cutoffs easier to defend.",
        "sections": [
            ("The question", quote("How much confidence should hiring managers place in interview scores when interviewers apply rating standards inconsistently or candidates score close to a cutoff?")),
            ("My approach", p("The review, written for SilverLine Health Technologies’ leadership, weighed each tool in the proposed system (a cognitive ability test, a personality inventory, and a structured interview) on reliability, validity, and how measurement error could tip individual hiring decisions.")),
            ("What the numbers showed",
             p("The cognitive test held up; the interview did not. Its interrater reliability of .54 means scores depend heavily on who conducts the interview, and because reliability caps validity, its predictive value stays limited.")
             + bars([
                 ("Cognitive: internal consistency", .84, ""),
                 ("Cognitive: test–retest", .77, ""),
                 ("Interview: interrater agreement", .54, "weak"),
             ], "Reliability of each selection tool, from the Validity & Criterion Defense Memo. Higher is more consistent.", "Reliability: cognitive internal consistency .84, cognitive test-retest .77, interview interrater .54")
             + bars([
                 ("Cognitive ability test", .39, ""),
                 ("Structured interview", .24, "weak"),
                 ("Personality inventory", None, "No internal validation data"),
             ], "Validity: correlation (r) between each tool and job performance.", "Validity: cognitive r .39, interview r .24, personality no internal data")
             + p("Measurement error matters most near the cutoff. With a standard error of 5.1 points, Candidates X and Z overlap almost entirely, and X’s likely range dips below the cutoff of 65, so accepting or rejecting on a two-point gap is hard to defend.")
             + sem_chart([("Candidate X", 70), ("Candidate Z", 72), ("Candidate Y", 78)], 65, 5.1,
                         "Cognitive test scores with a ±1 standard error band (5.1 points). Overlapping bands mean the difference may not be real.")),
            ("Work sample",
             '<div class="space-y-4"><p class="font-semibold">Recommendations from the assessment memo</p>'
             '<ul class="list-disc space-y-2 pl-6"><li>Have interviewers score independently before discussing candidates.</li>'
             '<li>Clarify behavioral anchors and train interviewers to apply them consistently.</li>'
             '<li>Monitor rater agreement and account for measurement error when interpreting scores near cutoffs.</li>'
             '<li>Validate the personality inventory and interview within SilverLine’s own workforce, and run adverse impact analyses.</li></ul></div>'
             '<p class="mt-4 text-sm text-foreground/75">From the executive recommendation in the Validity &amp; Criterion Defense Memo, pages 6–7.</p>'
             + pdfs(local_pdf("Validity-Criterion-Defense-Memo.pdf", "Download Validity & Criterion Defense Memo (PDF)"))),
            ("Related work: legal and ethical risk review",
             p("A companion memo reviewed a different hiring process, for Client Services Coordinators at Meridian Health Solutions, and ranked its legal and ethical risks.")
             + tiers([
                 ("High", ["No job analysis for the role", "Assessments used without validation evidence", "Interview questions about family responsibilities"]),
                 ("Moderate", ["“Digital natives” recruiting language", "Automatic screening on employment gaps", "Unstructured interviews"]),
                 ("Low", ["Standardized rejection emails"]),
             ], "Risk prioritization from the Meridian hiring risk memo, weighing severity, likelihood of challenge, and how well each practice is documented.")
),
            ("Recommendation or status", p("Approve the system on the condition of targeted revisions: strengthen the structured interview first, expand internal validation, build measurement error into score interpretation, and document the rationale behind every step.")),
        ],
    },
    {
        "slug": "pace",
        "category": "Apps & Workflow Design",
        "eyebrow": "Independent app prototype",
        "title": "Paced",
        "summary": "A concussion recovery companion that helps people pace their day: matching activity to their energy so they rest before symptoms flare, instead of pushing through and setting recovery back.",
        "header_extra": demo("https://mtbiperfectpace.netlify.app/"),
        "sections": [
            ("The question", quote("How can someone recovering from a concussion tell when to keep going and when to rest, before their symptoms make the decision for them?")),
            ("Why it matters", p("Pacing is the hardest part of concussion recovery. Doing too much triggers flare-ups that can set healing back by days; resting too much slows it down. The limits are also easy to miss, because reading, screens, conversations, and noisy rooms drain brain energy just like physical activity does. Most people only find their limit after they’ve crossed it.")),
            ("My approach", p("Paced turns energy into a simple gauge. Across short check-ins from waking up to evening, users rate their energy from 1 to 10, which places them in a green, yellow, or red zone with guidance on what kind of activity fits right now. They also note symptoms and how active they’ve been compared with a typical day, so patterns show up early, while symptoms are still mild.")
             + cards([
                 ("Energy zones", "Green, yellow, and red zones translate a 1–10 rating into a clear next step: keep going gently, ease off, or rest."),
                 ("Recovery trends", "Seven, 14, and 30-day views show energy over time, the most frequent symptoms, and activity against a typical day."),
                 ("Care-team summary", "A one-page recovery summary prints or saves as a PDF to bring to the next medical appointment."),
                 ("Recovery guide", "Plain-language cards on pacing, sleep, healthy habits, relaxation, and a gradual return to work or school."),
             ], "What the app does")
             + p("The design assumes a tired brain. Eye Comfort Mode warms and dims the screen, the guide shows one card at a time, and a built-in 4-4-6 breathing exercise and soft background sound support rest without adding stimulation.")
             + shots([("pace-signin.webp", "Paced app sign-in screen, with a note that it is a personal reflection tool, not a medical device")],
                     "Paced on mobile. The app frames itself as a personal reflection tool, not a medical device.")),
            ("Recommendation or status", p("Paced is an independent prototype and a personal reflection tool, not a medical device; it supports, rather than replaces, guidance from a care team. My graduate research builds on it, looking at what keeps people tracking during recovery and whether tracking sharpens their awareness of their own limits.")),
            ("Related work", related("concussion-tracking-thesis", "Digital and Paper-Based Concussion Tracking")),
        ],
    },
    {
        "slug": "overtime-performance-ratings",
        "reports": ["overtime-performance-ratings-1"],
        "category": "Performance Management",
        "eyebrow": "Graduate case analysis",
        "title": "When Overtime Shapes Performance Ratings",
        "summary": "Why employees who worked overtime earned higher ratings despite similar performance, and how manager training and calibration can tie ratings back to observable work.",
        "sections": [
            ("The question", quote("In the Tech Solutions case, employees who worked overtime received higher ratings even when their core performance was similar. What evidence should managers use to evaluate work quality and collaboration?")),
            ("What the analysis found",
             p("Three well-documented rater biases explain how availability can stand in for performance.")
             + cards([
                 ("Halo effect", "A willingness to take on extra work colors judgments of areas where an employee’s skills are actually weaker."),
                 ("Selective leniency", "Ratings run generous for employees who work overtime, and the audit shows the pattern reaches beyond any one pair."),
                 ("Contrast effect", "One employee’s availability becomes the benchmark, so a colleague can meet collaboration standards and still rate lower."),
             ], "Rater biases identified in the case analysis.")),
            ("Work sample",
             '<div class="space-y-4"><p>One manager practice exercise puts two scenarios side by side: an employee who completes skilled work during scheduled hours, and one who stays late but often needs corrections. Managers rate both against shared standards and explain the evidence behind each rating. In calibration meetings, HR then asks managers to back up every rating with specific examples from the review period.</p></div>'
             '<p class="mt-4 text-sm text-foreground/75">Adapted from the manager practice and calibration recommendations on page 5 of the Tech Solutions case analysis.</p>'),
            ("Recommendation or status", p("A follow-up audit would test whether ratings still track overtime among employees with similar responsibilities and core performance.")),
        ],
    },
    {
        "slug": "diagnosing-motivation-workplace-change",
        "reports": ["diagnosing-motivation-workplace-change-1", "diagnosing-motivation-workplace-change-2"],
        "category": "Leadership & Organizational Development",
        "eyebrow": "Graduate case analyses",
        "title": "Diagnosing Motivation During Workplace Change",
        "summary": "Two workplace cases showing how leaders can investigate a drop in motivation and choose a response the evidence supports.",
        "sections": [
            ("My approach", p("At Riverview Patient Access, two competing explanations for declining motivation are tested against the evidence that would strengthen or weaken each. At Northside Shared Services, a decision map links the diagnosis to specific leadership actions.")),
            ("Riverview: two theories, one problem",
             table(["", "Goal-setting theory", "Expectancy theory"], [
                 ["Diagnostic question", "Are current goals directing attention toward the behaviors leadership wants?", "Do employees believe effort leads to good performance and meaningful rewards?"],
                 ["Case facts", "Tighter call-time targets, weekly rankings, stricter scripts, fewer improvement ideas", "Brief training, software freezes, shifting bonus thresholds"],
                 ["Leadership action", "Measure quality, teamwork, and patient service alongside speed", "Improve training, stabilize technology, explain how performance affects bonuses"],
             ], "Condensed from the Riverview motivation diagnosis matrix.")
             + callout("Leading diagnosis", "Goal-setting theory explains the most: new call-time targets pulled attention toward speed at the expense of quality and improvement. Expectancy theory adds why effort started to feel futile.")),
            ("Northside: measuring whether leadership changes work",
             p("A new case-management system arrived during a 9 percent jump in service volume. The brief pairs performance results with employee-experience measures, so progress shows up in both the work and how people experience it.")
             + table(["Measure", "Type", "What it shows"], [
                 ["Rework, missed deadlines, response time", "Objective", "Whether quality, priorities, and timeliness are improving"],
                 ["Priority clarity, leadership explanation, feedback usefulness", "Perceptual", "Whether communication and coaching feel clear and useful"],
                 ["Fairness, voice, development access", "Pulse survey", "Whether opportunity processes and input channels feel fair"],
             ], "Leadership effectiveness measures from the Northside consulting brief.")),
        ],
    },
    {
        "slug": "global-employee-wellness-program",
        "category": "Leadership & Organizational Development",
        "eyebrow": "Graduate program proposal",
        "title": "Designing a Global Employee Wellness Program",
        "summary": "A legally sound wellness policy and needs-assessment survey for a hybrid team spread across locations and time zones.",
        "reports": ["global-employee-wellness-program-1", "global-employee-wellness-program-2"],
        "sections": [
            ("My approach", p("The policy gives every employee the same access to wellness support, whether they work near the office or from home: gym reimbursement handled through the insurer, optional lunchtime activities on site, and a monthly stipend for remote staff. Participation is voluntary, nothing is tracked, and no health information reaches the employer, which keeps the program within ADA, HIPAA, GINA, and EEOC requirements. A short needs-assessment survey then asks employees what’s working, what gets in the way, and what support they’d want next.")),
        ],
    },
    {
        "slug": "pay-for-performance-skill-development",
        "reports": ["pay-for-performance-skill-development-1", "pay-for-performance-skill-development-2"],
        "category": "Compensation & Global Mobility",
        "eyebrow": "Graduate compensation proposal",
        "title": "Designing Pay for Performance and Skill Development",
        "summary": "A pay design for a credit union that rewards both measurable performance and growing expertise.",
        "sections": [
            ("My approach",
             p("Market-based salary ranges stay the foundation. On top of them, the mix depends on how much control each role has over measurable outcomes and how much its success relies on deepening expertise.")
             + table(["Employee group", "Pay approach", "Evaluated on"], [
                 ["Loan officers", "Base salary + individual incentive", "Lending results, member service, documentation quality, compliance"],
                 ["Member service representatives", "Base + competency progression + team incentive", "Product knowledge, cross-training, service quality, accuracy"],
                 ["Compliance, security, and digital banking", "Base + competency progression; limited team incentive", "Technical or regulatory knowledge, certifications, demonstrated proficiency"],
                 ["Branch managers", "Base + competency progression + team incentive", "Branch results, member service, employee development, compliance"],
             ], "Proposed pay mix by role for Mountain West Community Credit Union.")
             + callout("Guardrail", "Quality and compliance act as a threshold for any incentive. High production can’t offset a serious failure in compliance or member protection.")),
            ("Recommendation or status", p("Pilot the design with a few job groups before expanding it across the credit union.")),
        ],
    },
    {
        "slug": "international-relocation-package",
        "category": "Compensation & Global Mobility",
        "eyebrow": "Graduate case proposal",
        "title": "Designing an International Relocation Package",
        "summary": "A compensation and benefits package for a hypothetical two-year assignment in Germany.",
        "sections": [
            ("My approach", p("A balance sheet approach fits a temporary assignment. Base pay stays separate from one-time moving costs and temporary allowances, with benefits continuity and planning for the employee’s return built in from the start.")),
        ],
    },
    {
        "slug": "own-your-presence",
        "card_image": OYP_BRAND,
        "category": "Apps & Workflow Design",
        "eyebrow": "Independent app",
        "title": "Own Your Presence",
        "summary": "A career-development app for women navigating career transitions.",
        "header_extra": demo("https://own-your-presence.netlify.app/"),
        "sections": [
            ("My approach", p("Twenty-one short sessions, two to five minutes a day, taken at the user’s own pace. A seven-step onboarding flow finds each user’s starting point, and short reflection prompts help her name her strengths and prepare for career conversations.")
             + shots([("oyp-welcome.webp", "Own Your Presence welcome screen: You don’t have to become someone else to be taken seriously"),
                      ("oyp-onboarding.webp", "Onboarding step 1 of 7: What kind of change are you navigating?")],
                     "The welcome screen and the first onboarding step.")),
            ("Work sample",
             f'<figure class="mb-6"><img alt="Brand imagery from the Own Your Presence brand book: Obsidian Black, Sunburst Yellow and Raspberry Pink." class="w-full rounded-md border border-foreground/20" src="{OYP_BRAND}" loading="lazy"></figure>'
             '<p class="mt-4 text-sm text-foreground/75">Brand imagery from the Own Your Presence brand book: Obsidian Black, Sunburst Yellow and Raspberry Pink.</p>'),
        ],
    },
    {
        "slug": "concussion-tracking-thesis",
        "category": "Applied Research",
        "categories": ["Applied Research", "Data & Analytics"],
        "eyebrow": "Thesis proposal",
        "title": "Digital and Paper-Based Concussion Tracking",
        "summary": "My master’s thesis proposal: a critical evidence review and conceptual model of how tracking systems relate to adherence and self-regulatory awareness during concussion recovery.",
        "reports": ["concussion-tracking-thesis-1"],
        "sections": [
            ("Related work", related("pace", "Paced")),
        ],
    },
]
