# ReportSaathi: Core Flow, Feature Breakdown, and MVP Scope Definition

**Document Reference:** `docs/03-core-flow.md`  
**Related Documents:** `docs/01-problem.md` (Product Vision) | `docs/02-research.md` (Market Research & Regulatory Analysis)  
**Date:** November 2026  
**Status:** Product Scope & Boundary Definition  

---

## 1. The Single Core Flow

The single core flow of ReportSaathi is designed to deliver immediate relief from medical jargon, anxiety, and confusion for patients and caregivers receiving diagnostic lab reports.

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                                   THE SINGLE CORE FLOW                                                  |
+-------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                         |
|   [ 1. Land on Web UI ]                                                                                                 |
|             │                                                                                                           |
|             ▼                                                                                                           |
|   [ 2. Upload Lab Report ] ────────► (PDF document or clear smartphone camera photo)                                    |
|             │                                                                                                           |
|             ▼                                                                                                           |
|   [ 3. Select Language ] ──────────► (English, Hindi, Tamil, Telugu, etc.)                                              |
|             │                                                                                                           |
|             ▼                                                                                                           |
|   [ 4. Ephemeral Extraction ] ─────► (Extract Test Name, Value, Unit, Lab's Printed Reference Range)                    |
|             │                                                                                                           |
|             ▼                                                                                                           |
|   [ 5. Simplified Report Card ] ───► Color-coded status: Normal / Slightly Out of Range / High                          |
|             │                        1-2 sentence plain-language explanation of what biomarker measures                 |
|             ▼                                                                                                           |
|   [ 6. Voice Readout (TTS) ] ──────► 1-click native audio playback in chosen language                                   |
|             │                                                                                                           |
|             ▼                                                                                                           |
|   [ 7. Doctor Questions ] ─────────► 2-3 specific, polite questions for patient's doctor consultation                   |
|             │                                                                                                           |
|             ▼                                                                                                           |
|   [ 8. Safety & Zero-Retention ] ──► Educational disclaimer + automatic session data purge                              |
|                                                                                                                         |
+-------------------------------------------------------------------------------------------------------------------------+
```

### End-to-End Walkthrough of the Core Flow:
1. **Entry:** The user visits a clean, single-screen web interface on any smartphone browser. **No account creation or password required.**
2. **Document Input:** The user taps a prominent upload button to select a digital lab report PDF (e.g., from Dr Lal PathLabs, Agilus, Metropolis, Apollo) or take a clear photo of a printed paper report.
3. **Language Selection:** The user taps their preferred language (e.g., Hindi, Tamil, Telugu, English).
4. **Extraction & Processing:** The system processes the document in-memory, extracting test parameters, reported values, units, and the laboratory's printed reference range.
5. **Plain-Language Summary:** The user sees a clean, large-font "Report Card":
   * Technical names are translated to common terms (e.g., *HbA1c* → *"3-Month Average Blood Sugar"*).
   * Values are visually placed on a simple colored gauge (*Within Normal Range* [Green] vs. *Out of Range* [Amber/Blue]).
   * A 1-2 sentence plain-language explanation describes what the test measures in daily life terms.
6. **Audio Narration:** A prominent "Listen" button plays a clear, natural-sounding voice readout of the summary in their mother tongue.
7. **Empowered Doctor Preparation:** The user receives 2-3 specific, actionable questions to ask their doctor at their upcoming appointment.
8. **Safe Completion & Purge:** The screen displays a mandatory non-diagnostic disclaimer, and the uploaded document is immediately purged from active memory (DPDP privacy compliance).

---

## 2. Feature & Sub-Feature Breakdown

The core flow breaks down into seven modular feature blocks:

```
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| Feature Module                    | Sub-Features                                                                     |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 1. Document Ingestion             | 1.1 Multi-Format File Upload (PDF, JPEG, PNG)                                    |
|                                   | 1.2 Pre-flight Validation (File size limits, basic blur/resolution check)        |
|                                   | 1.3 Ephemeral Buffer (In-memory file stream, zero persistent disk writes)        |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 2. Extraction & Parsing           | 2.1 Native PDF Text Layer Extractor (Deterministic extraction for lab PDFs)      |
|                                   | 2.2 OCR Vision Fallback (For scanned/photographed physical reports)              |
|                                   | 2.3 Medical Entity Mapping (Test Name, Numeric Value, Unit, Lab Normal Range)    |
|                                   | 2.4 Uncertainty & Illegibility Detection (Flags unreadable or skewed areas)      |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 3. Simplification & Normalization | 3.1 Relative Range Comparator (Normal / Low / High based strictly on lab ranges) |
|                                   | 3.2 Layman Medical Dictionary (Mapping clinical terms to patient-friendly words) |
|                                   | 3.3 Reassuring Summary Generator (Concise educational summaries without panic)   |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 4. Multilingual Translation       | 4.1 Vernacular Translation Engine (Hindi, Tamil, Telugu, English)                |
|                                   | 4.2 Medical Cultural Localization (Natural phrasing rather than literal machine) |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 5. Accessibility & Audio          | 5.1 Text-to-Speech (TTS) Voice Narration (Natural local accent audio readout)    |
|                                   | 5.2 Senior-Friendly UI (High-contrast, large typography, touch-friendly buttons)  |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 6. Doctor Consultation Prep       | 6.1 Contextual Question Generator (2-3 tailored questions for the doctor visit)  |
|                                   | 6.2 Visual Status Cards (Color-coded visual gauges for rapid comprehension)      |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
| 7. Safety & Regulatory Compliance | 7.1 Non-Diagnostic Legal Disclaimer Banner (Mandatory educational declaration)   |
|                                   | 7.2 Zero-Retention Privacy Protocol (Immediate automated session data wipe)      |
|                                   | 7.3 Diagnostic Blacklist Guardrails (Strict blocks on disease labeling)          |
+───────────────────────────────────+──────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Challenging the MVP (Ruthless Pruning)

To ensure the MVP is lightweight, fast to build, clinically safe, and legally compliant, every prospective feature is challenged against one criterion: **"Can the single core flow deliver its main value without this feature?"**

### 1. Challenge: User Registration, Login, and Password Authentication
* *Question:* Does a patient need an account to understand their lab report?
* *Verdict:* **CUT FROM MVP.** 
* *Reason:* Forcing elderly or anxious patients to register with passwords or OTPs creates immediate drop-off. A guest session delivers instant value in under 30 seconds. Furthermore, avoiding persistent user accounts eliminates database breach liability under India's DPDP Act, 2023.

### 2. Challenge: Handwritten Prescription OCR (Module A in original plan)
* *Question:* Can the MVP launch without reading handwritten doctor slips?
* *Verdict:* **CUT FROM MVP.**
* *Reason:* Market research (`docs/02-research.md`) proved OCR on messy handwritten Indian prescriptions has a 25%–40% error rate. AI hallucinations on Look-Alike Sound-Alike (LASA) drug names (e.g., *Metformin* vs *Metoprolol*) or dosages (5mg vs 50mg) carry life-threatening liability. Printed lab reports have >99% OCR accuracy and zero drug-misidentification risk.

### 3. Challenge: Open-Ended Conversational AI Chatbot ("Ask Me Anything")
* *Question:* Does the user need a free-text chat box to ask arbitrary medical questions?
* *Verdict:* **CUT FROM MVP.**
* *Reason:* Open-ended medical chatbots invite users to ask "What disease do I have?" or "Can I stop my medicine?", leading the AI into unauthorized medical diagnosis or treatment advice. A structured, one-way "Report Card" is predictable, safe, and senior-friendly.

### 4. Challenge: Historical Biomarker Trend Graphing
* *Question:* Does a first-time user need graphs showing changes over 12 months to understand today's report?
* *Verdict:* **CUT FROM MVP.**
* *Reason:* Trend graphs require persistent user profiles, multi-document cross-referencing, and long-term data storage. The core value is delivered by explaining *the report in the user's hand today*.

### 5. Challenge: Native Mobile Applications (iOS / Android App Stores)
* *Question:* Does the product need to be in the Google Play Store or Apple App Store for MVP?
* *Verdict:* **CUT FROM MVP.**
* *Reason:* Native app development triples development overhead and introduces 50MB+ download friction. A lightweight, responsive web app accessible via mobile browser delivers the exact same experience instantly.

### 6. Challenge: In-App Payment Gateway & Paywalls
* *Question:* Do we need payment integration in MVP?
* *Verdict:* **CUT FROM MVP.**
* *Reason:* Introducing a paywall during MVP disrupts user testing and problem validation. The MVP should be free with a fair-use rate limit (e.g., 3 reports/day per IP).

---

## 4. Feature Sorting: MVP vs. Later vs. Never

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                               FEATURE CATEGORIZATION                                                 |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|  [ MVP ]                    │  [ LATER ]                       │  [ NEVER ]                                          |
|  • Lab Report PDF/Photo Ingest│  • User Accounts & Vault         │  • Autonomous Disease Diagnosis                     |
|  • Printed Report Parser    │  • Historical Trend Graphing     │  • Medication / Dosage Changes                      |
|  • Range Comparator (Lab Ref)│  • Caregiver Sharing & Linking   │  • Autonomous Prescription of Drugs                 |
|  • Layman Summary Generator │  • WhatsApp Business AI Bot      │  • Guessing Illegible Handwriting                   |
|  • Multilingual (EN/HI/TE/TA)│  • Printed Prescription Module  │  • Clinical Risk / Mortality Scoring                |
|  • Text-to-Speech (TTS Audio)│  • All 22 Scheduled Languages    │  • Therapeutic Claims for Sched. J                  |
|  • 3 Doctor Questions       │  • HITL Pharmacist Review        │  • Selling / Monetizing Patient Data                |
|  • Non-Diagnostic Disclaimer│  • ABDM / ABHA Health Locker     │  • Doctor Impersonation / "Dr. AI"                  |
|  • DPDP Zero-Data Retention │  • Downloadable PDF Report Cards │  • Emergency Triage Replacement                     |
|  • Responsive Mobile Web UI │  • B2B Diagnostic Lab White-Label│                                                     |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 4.1. MVP (Must-Have for Core Flow)
These features are strictly necessary to deliver safe, understandable explanations for diagnostic reports:

1. **Lab Report PDF & Photo Upload:** Enables ingestion of digital PDFs (from Dr Lal, Metropolis, etc.) and camera photos of paper printouts.
   * *Reason:* Core input mechanism.
2. **Printed Lab Report Parser:** Extracts Test Name, Observed Value, Unit, and Laboratory-Specified Reference Range.
   * *Reason:* Structured data extraction is required before generating explanations.
3. **Relative Range Status Indicator:** Classifies findings strictly against the lab's printed range (*Normal / Below Normal / Above Normal*).
   * *Reason:* Immediate visual clarity on which parameters require doctor discussion, without diagnosing.
4. **Layman Explanation Generator:** Converts technical terms (e.g., *BUN, Bilirubin, TSH*) into simple 1-2 sentence everyday explanations.
   * *Reason:* Solves the core problem of incomprehensible clinical jargon.
5. **Initial Language Selection (English, Hindi, Telugu, Tamil):** Covers >70% of digital health queries in India.
   * *Reason:* Solves the fundamental linguistic exclusion of non-English speakers.
6. **Text-to-Speech (TTS) Voice Narration:** Audio readout of the generated summary in the selected language.
   * *Reason:* Essential for elderly and low-literacy users who struggle with small smartphone screen text.
7. **Doctor Discussion Questions (2–3 Questions):** Proactive, polite questions tailored to the findings.
   * *Reason:* Empowers the patient to have an informed dialogue with their doctor rather than self-treating.
8. **Statutory Medical Safety Disclaimer:** Unambiguous declaration that the tool is an educational aid, not medical advice.
   * *Reason:* Legal requirement under CDSCO SaMD and Telemedicine Practice Guidelines.
9. **DPDP Zero-Data Retention Protocol:** In-memory document processing with automatic purge after session completion.
   * *Reason:* Avoids data privacy liabilities and regulatory burdens under the DPDP Act, 2023.
10. **Mobile-Responsive Single-Page Web UI:** Clean, large-font interface optimized for smartphone screens without login friction.
    * *Reason:* Eliminates app installation barriers for elderly users.

---

### 4.2. Later (Post-MVP Enhancements)
Valuable capabilities that expand distribution, retention, and monetization, but are non-essential for initial value validation:

1. **User Accounts & Encrypted Health Vault:** Allows returning users to voluntarily save past reports behind OTP authentication.
   * *Reason for Later:* Adds sign-up friction; MVP works cleanly with zero-retention guest sessions.
2. **Historical Biomarker Trend Graphing:** Visualizes tracking over time (e.g., HbA1c over 12 months).
   * *Reason for Later:* Requires persistent data storage and multi-document database architecture.
3. **Caregiver & Family Member Linking:** Enables adult children to manage and view reports for elderly parents remotely.
   * *Reason for Later:* Secondary user persona; primary user flow must be validated first.
4. **WhatsApp Business AI Bot:** Ingestion and voice note delivery directly inside WhatsApp chats.
   * *Reason for Later:* Requires official WhatsApp Business API approvals and per-conversation messaging costs; web MVP validates parsing logic first at near-zero cost.
5. **Printed / Digital Prescription Explainer:** Explains typed or e-prescriptions (purpose, before/after food timing).
   * *Reason for Later:* Lab reports provide cleaner, higher-confidence validation; prescriptions will follow once lab parsing is perfected.
6. **Expansion to All 22 Constitutional Indian Languages:** Expanding beyond Hindi, Tamil, Telugu, and English.
   * *Reason for Later:* Multi-language prompt verification and voice synthesis tuning require staged rollouts.
7. **Human-in-the-Loop (HITL) Pharmacist Review:** Optional asynchronous human review for ambiguous documents.
   * *Reason for Later:* Operationally complex; requires licensed staffing and unit-economics validation.
8. **Ayushman Bharat Digital Mission (ABDM / ABHA) Integration:** Direct connection to India's national health records network.
   * *Reason for Later:* Complex government sandbox certification process (M1/M2/M3).
9. **Downloadable / Shareable Summary PDF:** Generates a clean, one-page localized PDF to print or show family.
   * *Reason for Later:* Web display + TTS readout is sufficient for MVP.
10. **B2B Diagnostic Lab White-Label SDK:** Licensing the engine directly to diagnostic chains (Dr Lal, Metropolis).
    * *Reason for Later:* Requires a validated consumer-facing engine and clinical accuracy proof points before enterprise sales cycles.

---

### 4.3. Never (Explicitly Out of Scope & Prohibited)
*Any feature that would diagnose illness, alter clinical treatment, compromise patient privacy, or violate statutory Indian law:*

1. **Autonomous Disease Diagnosis:**
   * *Prohibited Function:* The platform will never state or infer clinical diagnoses (e.g., *"You have Type 2 Diabetes"*, *"This indicates Chronic Kidney Disease"*).
   * *Reason:* Diagnosing without a licensed Registered Medical Practitioner (RMP) is illegal under the NMC Act, Telemedicine Guidelines 2020, and triggers heavy CDSCO Class C Medical Device regulations.
2. **Medication Prescription or Dosage Modification:**
   * *Prohibited Function:* The platform will never instruct patients to start, stop, increase, or decrease medications (e.g., *"Increase Metformin to 1000mg"*, *"Stop taking your Statin"*).
   * *Reason:* Direct violation of the Drugs and Cosmetics Act and Telemedicine Guidelines; carries lethal clinical liability for adverse drug events.
3. **Autonomous Guessing of Illegible Handwritten Prescriptions:**
   * *Prohibited Function:* The AI will never take probabilistic guesses at unreadable cursive handwriting on prescriptions.
   * *Reason:* High probability of confusing Look-Alike Sound-Alike (LASA) drugs (e.g., *Clonazepam* vs *Clobazam*, *Metformin* vs *Metoprolol*), causing catastrophic patient harm.
4. **Clinical Risk Scoring & Mortality / Morbidity Calculators:**
   * *Prohibited Function:* No cardiovascular risk calculators (ASCVD), Framingham scores, cancer likelihood scores, or life-expectancy projections.
   * *Reason:* Reclassifies software into a high-risk medical device under CDSCO SaMD rules and causes extreme health anxiety (cyberchondria).
5. **Therapeutic Claims for Scheduled Diseases (Schedule J):**
   * *Prohibited Function:* Making claims of curing, preventing, or reversing diseases listed under Schedule J (diabetes, hypertension, cancer, kidney failure, epilepsy, blindness).
   * *Reason:* Criminal offense under Section 3 of the Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954.
6. **Selling or Monetizing Patient Health Data:**
   * *Prohibited Function:* Selling, brokering, or sharing patient medical data with pharmaceutical brands, insurance companies, or advertising networks.
   * *Reason:* Serious statutory offense under India's Digital Personal Data Protection Act, 2023 (DPDP Act), subject to penalties up to ₹250 Crore.
7. **Doctor Impersonation or "Dr. AI" Persona:**
   * *Prohibited Function:* Presenting the system as an artificial doctor or virtual practitioner.
   * *Reason:* Misleading advertising under the Consumer Protection Act, 2019 and violation of medical registration laws.
8. **Emergency Triage or Acute Crisis Replacement:**
   * *Prohibited Function:* Attempting to triage acute medical emergencies (chest pain, stroke symptoms, severe bleeding).
   * *Reason:* Software cannot evaluate acute vitals; all critical flags must immediately direct the user to call local emergency services (112/108) or visit an emergency room.

---

## 5. Summary: MVP Definition at a Glance

The ReportSaathi MVP is a **single-screen, mobile-responsive web application** that allows a patient or caregiver to:
1. Upload a printed diagnostic lab report (PDF or camera photo).
2. Select their language (English, Hindi, Telugu, Tamil,Kannada).
3. Instantly view a color-coded, plain-language breakdown of their results compared to the laboratory's printed normal ranges.
4. Listen to a natural voice readout (TTS) of the summary in their mother tongue.
5. Review 2–3 practical questions to ask their doctor at their upcoming consultation.
6. Exit with zero data saved on the server.

*This minimal footprint delivers 100% of the core comprehension value while eliminating login barriers, app download friction, clinical hallucination liability, and data privacy risks.*
