# BUSINESS_CASE.md

## 1. Problem Statement

The startup ecosystem is dynamic and competitive.  
- Investors need to track where talent is flowing to evaluate growth signals.  
- Recruiters must identify companies that are actively hiring in order to prioritize outreach.  
- Educators (universities, training programs) want to align curricula with real-world demand.  

However, job market data is fragmented. Each startup hosts its own career board, usually via third-party Applicant Tracking Systems (ATS) like Greenhouse. There is no central directory of startup job postings. This makes it difficult to systematically compare hiring trends across industries.

---

## 2. Proposed Solution

We built a **Hiring Trends Radar** that scrapes publicly available postings from **Greenhouse job boards** and organizes them by industry.

- **Single pipeline:** Extract job data via the Greenhouse API.  
- **Industry catalog:** Use a CSV (`startups.csv`) to classify companies by sector (AI, Fintech, Health, etc.).  
- **Output:** Structured dataset (`output.json`) that can be easily analyzed, shared, or visualized.  

This system creates a unified view of startup hiring trends across multiple industries.

---

## 3. Value Proposition

**For Investors:**  
- Detect emerging industries with rapid headcount growth.  
- Spot early signals of expansion (new offices, new roles).  
- Validate portfolio performance through hiring activity.

**For Recruiters:**  
- Prioritize outreach to high-growth startups with many open roles.  
- Identify niche technical roles (e.g., AI safety engineer) that indicate demand.  
- Reduce time spent browsing individual career sites.

**For Educators / Training Programs:**  
- Align curricula with skills that startups are actively hiring for.  
- Provide students with real-time insights into the startup job market.  
- Strengthen industry-academic collaboration.

---

## 4. Market Analysis

- **Recruitment software market size (2024):** ~$3.1B globally, projected to grow >7% annually (MarketsandMarkets).  
- **Global EdTech market:** ~$250B, with strong demand for job market insights.  
- **VC investment market:** ~$450B deployed annually; investors increasingly rely on real-time hiring data as a proxy for growth.

This shows that a Hiring Trends Radar has multiple monetization opportunities:  
- Subscription dashboards for VCs.  
- Lead lists for recruiters.  
- Industry reports for universities.

---

## 5. Pricing Strategy (Hypothetical)

1. **Free tier (academic use):** Limited industries, weekly data refresh.  
2. **Professional tier (recruiters):** $99/month per user — access to all industries, daily refresh.  
3. **Enterprise tier (investors/VCs):** Custom pricing — bulk data exports, API access, portfolio monitoring.

---

## 6. Risks & Mitigations

- **Legal / Ethical:** Scraping must comply with CFAA, GDPR, and Terms of Service (see `ETHICS.md`).  
- **Data Completeness:** Not all startups use Greenhouse (some use Lever, Ashby, Workday). Future versions can extend support.  
- **Data Freshness:** Over-scraping could harm site performance. We mitigate via backoff, delays, and respecting robots.txt.

---

## 7. Conclusion

The Hiring Trends Radar transforms scattered Greenhouse job postings into a **systematic intelligence platform**.  
By focusing on aggregate hiring signals, it creates value for investors, recruiters, and educators — each of whom depends on accurate, timely labor market insights.

