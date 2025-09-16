# ETHICS.md

## 1. Legal Analysis

Web scraping raises both legal and ethical concerns depending on jurisdiction.

- **Computer Fraud and Abuse Act (CFAA), 18 U.S.C. § 1030 (United States):**  
  Scraping can be problematic if it bypasses authentication or technical barriers. However, Greenhouse job boards are **publicly accessible** without login, which lowers risk.

- **HiQ Labs v. LinkedIn Corp., 938 F.3d 985 (9th Cir. 2019):**  
  The Ninth Circuit held that scraping publicly available data (without circumventing security) is not a violation of the CFAA. Our Greenhouse scraping falls closer to this category.

- **Terms of Service:**  
  Greenhouse’s [Terms of Service](https://www.greenhouse.io/terms) govern platform use. Automated scraping may technically violate contractual terms. This is a civil (contract) matter rather than criminal law but should be acknowledged.

- **EU GDPR (General Data Protection Regulation, Regulation (EU) 2016/679):**  
  Scraped job postings rarely contain personal data, but if a job description inadvertently includes personally identifiable information (PII), storage/processing must comply with GDPR.

---

## 2. Impact on Website Operations

- **Server Load:**  
  Automated scrapers, if aggressive, can generate undue traffic and degrade performance for actual job seekers and companies.  
  **Mitigation:** We implemented:
  - Respectful rate limits (`time.sleep` + random delay).  
  - Retry with exponential backoff.  
  - Adherence to `robots.txt` unless explicitly overridden for testing.  

- **Data Freshness:**  
  Frequent scraping risks hammering the site. Our approach justifies update frequency (daily or weekly, not real-time).

---

## 3. Privacy Considerations

- **Public Job Data Only:**  
  We only scrape job titles, locations, and links. No personal candidate or employee information is accessed.  

- **Data Storage:**  
  Results are saved in `data/output.json`. We avoid collecting or storing sensitive metadata.  

- **Compliance:**  
  Since no PII is collected, GDPR/CCPA risks are minimal. Still, all stored data should be handled responsibly, with access restricted to project stakeholders.

---

## 4. Ethical Framework

Our team adopted the following principles:

- **Transparency:** Documenting exactly what was scraped, how often, and with what tools (see `AI_USAGE.md`).  
- **Respect:** Limiting requests and respecting `robots.txt` whenever possible.  
- **Proportionality:** Collecting only as much data as needed to analyze **hiring trends**, not exhaustively harvesting every field.  
- **Accountability:** Bugs, failures, and design choices are logged so others can evaluate the approach.  

We believe this framework balances the educational purpose of the assignment with respect for platforms and their users.

---

## 5. Alternative Approaches Considered

1. **Official APIs:**  
   Some companies offer RSS feeds or APIs for job postings. Using those would reduce legal/ethical concerns but limit coverage.

2. **Partnerships with Startups:**  
   A more sustainable model would involve requesting datasets directly from companies or ATS providers (Greenhouse, Lever, etc.).

3. **Third-party Aggregators:**  
   Services like Indeed, LinkedIn, or Levels.fyi already aggregate job data. However, scraping them would introduce greater legal/ethical risks because they explicitly restrict scraping and contain personal data.

4. **Manual Data Collection:**  
   Human researchers could periodically record openings. While compliant, this approach is less scalable and less educational in terms of automation.

---

**Conclusion:**  
By limiting scope to **Greenhouse job boards**, implementing respectful scraping practices, and focusing only on aggregate job data, we minimize legal, operational, and privacy risks while still fulfilling the assignment’s goals.

