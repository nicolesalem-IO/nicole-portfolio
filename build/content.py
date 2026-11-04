from html import escape as e

HEADSHOT = "https://base44.app/api/apps/6aeb6d24517ad9a537d05c86/files/mp/public/6aeb6d24517ad9a537d05c86/d1e1e3d7c_headshot.jpeg"
RESUME = "https://base44.app/api/apps/6aeb6d24517ad9a537d05c86/files/mp/public/6aeb6d24517ad9a537d05c86/b25e5299c_Nicole-Salem-Resume.pdf"
LINKEDIN = "https://www.linkedin.com/in/nicole-salem-hr/"
MEDIA = "https://media.base44.com/files/public/user_6aeb68b39348f0600718113a/"

CATEGORIES = [
    "Training & Development",
    "Selection & Assessment",
    "Performance Management",
    "Leadership & Organizational Development",
    "Compensation & Global Mobility",
    "Applied Research",
    "Apps & Workflow Design",
]


# ---------- building blocks ----------

def pdf(file, label):
    return (f'<a href="{MEDIA}{file}" target="_blank" rel="noopener noreferrer" '
            f'class="btn btn-line text-base">{label}</a>')


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
            ("Work sample", pdfs(pdf("abd1e38d7_TrainingEvaluationPlan_FinalCoursePlan95621AM.pdf", "View full PDF"))),
            ("Recommendation or status", p("Evaluation centers on one question: are supervisors using the feedback process consistently, and is it reducing documentation-related issues? Managers hold weekly check-ins during the first month, and documentation trends get reviewed 60 to 90 days after launch.")),
        ],
    },
    {
        "slug": "hiring-system-implementation-consultants",
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
             + pdfs(pdf("9aecb3a21_LegalEthicalRiskAssessmentMemo120717PM.pdf", "Download Meridian hiring risk memo (PDF)"))),
            ("Recommendation or status", p("Approve the system on the condition of targeted revisions: strengthen the structured interview first, expand internal validation, build measurement error into score interpretation, and document the rationale behind every step.")),
        ],
    },
    {
        "slug": "pace",
        "category": "Apps & Workflow Design",
        "eyebrow": "Independent app prototype",
        "title": "Pace",
        "summary": "A concussion-recovery tracker for logging symptoms, energy, and activity throughout the day.",
        "header_extra": demo("https://mtbiperfectpace.netlify.app/"),
        "sections": [
            ("The question", quote("How can someone keep a record of how they feel and what they do throughout the day during concussion recovery?")),
            ("My approach", p("Quick check-ins during the day and a short reflection at the end of it. Keeping both in one place puts how someone feels right next to what they’ve been doing.")
             + shots([("pace-signin.webp", "Paced app sign-in screen, with a note that it is a personal reflection tool, not a medical device")],
                     "Paced on mobile. The app frames itself as a personal reflection tool, not a medical device.")),
            ("Recommendation or status", p("Pace is an independent prototype. Related graduate research looks at adherence and perceived self-regulatory awareness during concussion tracking.")),
            ("Related work", related("understanding-adherence-concussion-tracking", "Understanding Adherence to Concussion Tracking")),
        ],
    },
    {
        "slug": "understanding-adherence-concussion-tracking",
        "category": "Applied Research",
        "eyebrow": "Graduate research in progress",
        "title": "Understanding Adherence to Concussion Tracking",
        "summary": "An evidence review and conceptual model exploring how digital and paper tracking shape adherence and self-regulatory awareness during concussion recovery.",
        "sections": [
            ("My approach", p("The model examines how ease of use and the ongoing effort of tracking might explain why people engage with it so differently.")),
            ("Related work", related("pace", "Pace")),
        ],
    },
    {
        "slug": "overtime-performance-ratings",
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
             '<p class="mt-4 text-sm text-foreground/75">Adapted from the manager practice and calibration recommendations on page 5 of the Tech Solutions case analysis.</p>'
             + pdfs(pdf("62fcf5a0c_RaterBiasandPerformanceEvaluationatTechSolutionsInc11.pdf", "View full PDF"))),
            ("Recommendation or status", p("A follow-up audit would test whether ratings still track overtime among employees with similar responsibilities and core performance.")),
        ],
    },
    {
        "slug": "diagnosing-motivation-workplace-change",
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
            ("Work sample", pdfs(
                pdf("7030437b8_MotivationDiagnosisMatrix.pdf", "Download Riverview diagnosis matrix (PDF)"),
                pdf("762b78eae_AppliedLeadershipandMotivationConsultingBrief.pdf", "Download Northside consulting brief (PDF)"))),
        ],
    },
    {
        "slug": "global-employee-wellness-program",
        "category": "Leadership & Organizational Development",
        "eyebrow": "Graduate program proposal",
        "title": "Designing a Global Employee Wellness Program",
        "summary": "A wellness proposal and needs-assessment survey for a team spread across locations and time zones.",
        "sections": [
            ("My approach", p("A 60-day pilot would test how scheduling practices, focus time, and wellness supports work for teams with different coverage needs. The evaluation pairs employee feedback with indicators such as meeting load and use of wellness resources.")),
        ],
    },
    {
        "slug": "pay-for-performance-skill-development",
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
            ("Work sample", pdfs(
                pdf("4335191ae_ProposalforImplementingPerformance-BasedandCompetency-BasedPaySystems.pdf", "View full PDF"),
                pdf("1f216510e_AnalysisofManagerialandExecutiveCompensationStrategies_RecommendationsforMountainWest.pdf", "Download managerial and executive compensation analysis (PDF)"))),
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
        ],
    },
]
