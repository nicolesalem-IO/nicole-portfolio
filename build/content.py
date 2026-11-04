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


# Order matches the Projects page. The first three are featured on Home.
PROJECTS = [
    {
        "slug": "supervisor-coaching-healthcare-clinic",
        "category": "Training & Development",
        "eyebrow": "Graduate training design and evaluation plan",
        "title": "Designing Supervisor Coaching for a Healthcare Clinic",
        "summary": "I designed a supervisor coaching program for a healthcare clinic case involving recurring documentation errors.",
        "sections": [
            ("The question", quote("The clinic’s front-line employees received feedback when documentation mistakes occurred, yet similar errors kept coming up. How could supervisors make that feedback more useful and follow up consistently?")),
            ("My approach", "<p>I designed training around the coaching conversations supervisors would have on the job. I connected the performance gaps to learning objectives, practice activities, and evaluation measures. I also developed a follow-up checklist so supervisors would have a tool to use after training.</p>"),
            ("Work sample", pdfs(pdf("abd1e38d7_TrainingEvaluationPlan_FinalCoursePlan95621AM.pdf", "View full PDF"))),
            ("Recommendation or status", "<p>The evaluation plan proposes checking how supervisors apply the coaching process on the job and whether documentation errors change over time.</p>"),
        ],
    },
    {
        "slug": "hiring-system-implementation-consultants",
        "category": "Selection & Assessment",
        "eyebrow": "Graduate assessment memo",
        "title": "Evaluating a Hiring System for Healthcare Implementation Consultants",
        "summary": "I evaluated a proposed hiring system and recommended ways to make interview scoring more consistent and decisions near cutoffs easier to justify.",
        "sections": [
            ("The question", quote("How much confidence should hiring managers place in interview scores when interviewers apply rating standards inconsistently or candidates score close to a cutoff?")),
            ("My approach", "<p>I reviewed the proposed assessments, the evidence supporting their use, and how measurement error could affect individual hiring decisions. I identified inconsistent interview administration and scoring as priorities for improvement.</p>"),
            ("Work sample",
             '<div class="space-y-4"><p class="font-semibold">Recommendations from the assessment memo</p>'
             '<ul class="list-disc space-y-2 pl-6"><li>Have interviewers score independently before discussing candidates.</li>'
             '<li>Clarify behavioral anchors and train interviewers to apply them consistently.</li>'
             '<li>Monitor rater agreement and account for measurement error when interpreting scores near cutoffs.</li></ul></div>'
             '<p class="mt-4 text-sm text-foreground/75">Selected recommendations from the Validity &amp; Criterion Defense Memo, pages 6–7.</p>'
             + pdfs(pdf("9aecb3a21_LegalEthicalRiskAssessmentMemo120717PM.pdf", "Download Meridian hiring risk memo (PDF)"))),
            ("Recommendation or status", "<p>I recommended proceeding after these revisions and documenting the evidence supporting the selection process.</p>"),
        ],
    },
    {
        "slug": "pace",
        "category": "Apps & Workflow Design",
        "eyebrow": "Independent app prototype",
        "title": "Pace",
        "summary": "I built a concussion-tracking prototype that helps users record symptoms, energy, and activity during recovery.",
        "header_extra": demo("https://mtbiperfectpace.netlify.app/"),
        "sections": [
            ("The question", quote("How can someone keep a record of how they feel and what they do throughout the day during concussion recovery?")),
            ("My approach", "<p>I built a workflow for checking in during the day and reflecting at the end of it. The tracker gives users a place to record how they feel alongside what they’ve been doing.</p>"),
            ("Recommendation or status", "<p>Pace is an independent app prototype. My related graduate research examines adherence and perceived self-regulatory awareness during concussion tracking.</p>"),
            ("Related work", related("understanding-adherence-concussion-tracking", "Understanding Adherence to Concussion Tracking")),
        ],
    },
    {
        "slug": "understanding-adherence-concussion-tracking",
        "category": "Applied Research",
        "eyebrow": "Graduate research in progress",
        "title": "Understanding Adherence to Concussion Tracking",
        "summary": "I’m developing an evidence review and conceptual model about how digital and paper tracking may shape adherence and perceived self-regulatory awareness during concussion recovery.",
        "sections": [
            ("My approach", "<p>I’m examining how factors such as ease of use and the effort required to keep tracking may help explain why people engage with tracking differently.</p>"),
            ("Related work", related("pace", "Pace")),
        ],
    },
    {
        "slug": "overtime-performance-ratings",
        "category": "Performance Management",
        "eyebrow": "Graduate case analysis",
        "title": "When Overtime Shapes Performance Ratings",
        "summary": "I analyzed why employees who worked overtime received higher ratings despite similar core performance, then proposed manager training and calibration to ground ratings in observable work.",
        "sections": [
            ("The question", quote("In the Tech Solutions case, employees who worked overtime received higher ratings even when their core performance was similar. What evidence should managers use to evaluate work quality and collaboration?")),
            ("Work sample",
             '<div class="space-y-4"><p>For a manager practice exercise, I proposed comparing two scenarios: an employee who completes skilled work during scheduled hours and an employee who stays late but frequently needs corrections. Managers would rate both examples against shared standards and explain the evidence behind each rating. In calibration meetings, HR would ask managers to support their ratings with specific examples from the review period.</p></div>'
             '<p class="mt-4 text-sm text-foreground/75">Adapted from the manager practice and calibration recommendations on page 5 of my Tech Solutions case analysis.</p>'
             + pdfs(pdf("62fcf5a0c_RaterBiasandPerformanceEvaluationatTechSolutionsInc11.pdf", "View full PDF"))),
            ("Recommendation or status", "<p>I proposed a follow-up audit to see whether ratings continued to vary with overtime among employees with similar responsibilities and core performance.</p>"),
        ],
    },
    {
        "slug": "diagnosing-motivation-workplace-change",
        "category": "Leadership & Organizational Development",
        "eyebrow": "Graduate case analyses",
        "title": "Diagnosing Motivation During Workplace Change",
        "summary": "I used two workplace cases to show how leaders can investigate changes in motivation and choose a response based on the evidence.",
        "sections": [
            ("My approach", "<p>In Riverview Patient Access, I compared two explanations for declining motivation and identified what evidence would strengthen or weaken each one. In Northside Shared Services, I used a decision map to connect my diagnosis to recommended actions.</p>"),
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
        "summary": "I designed a workplace wellness proposal and a needs assessment survey for a team working across locations and time zones.",
        "sections": [
            ("My approach", "<p>I proposed a 60-day pilot to learn how scheduling practices, focus time, and wellness supports would work for teams with different coverage needs. The evaluation plan combines employee feedback with indicators such as meeting load and use of wellness resources.</p>"),
        ],
    },
    {
        "slug": "pay-for-performance-skill-development",
        "category": "Compensation & Global Mobility",
        "eyebrow": "Graduate compensation proposal",
        "title": "Designing Pay for Performance and Skill Development",
        "summary": "I proposed a pay design for a credit union case that recognizes both performance and skill development.",
        "sections": [
            ("My approach", "<p>I recommended making quality a condition of incentive eligibility and piloting the design with a limited number of job groups before expanding it.</p>"),
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
        "summary": "I designed a compensation and benefits approach for a hypothetical two-year assignment in Germany.",
        "sections": [
            ("My approach", "<p>I recommended a balance sheet approach for the temporary assignment. I separated base pay from one-time moving costs and temporary allowances, and addressed benefits continuity and planning for the employee’s return.</p>"),
        ],
    },
    {
        "slug": "own-your-presence",
        "category": "Apps & Workflow Design",
        "eyebrow": "Independent app",
        "title": "Own Your Presence",
        "summary": "I built a career development app for women navigating career transitions.",
        "header_extra": demo("https://own-your-presence.netlify.app/"),
        "sections": [
            ("My approach", "<p>I designed an onboarding flow and short reflection prompts to help users identify their strengths and prepare for career conversations.</p>"),
        ],
    },
]
