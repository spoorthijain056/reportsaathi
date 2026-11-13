# Product Requirements Document (PRD): ReportSaathi MVP

**Document Reference:** `docs/05-prd.md`  
**Related Documents:** `docs/01-problem.md` (Product Vision) | `docs/02-research.md` (Market & Legal Research) | `docs/03-scope.md` (Scope & Flow) | `docs/04-design.md` (Screen States & UI Direction)  
**Date:** November 2026  
**Status:** Approved for Implementation  
**Target Release:** MVP Phase 1 (Web Application for Mobile Devices)  

---

## 1. Product Overview & Strategic Context

**ReportSaathi** is an AI-powered, multilingual health document comprehension assistant. It translates complex diagnostic laboratory reports into simple, patient-friendly explanations, visual reference indicators, and actionable doctor discussion questions in the user's preferred Indian language, accompanied by native voice narration.

In accordance with the market research in `docs/02-research.md` and the ruthless scope pruning in `docs/03-scope.md`, the MVP is deliberately scoped to **printed and digital diagnostic laboratory reports** (e.g., Blood Tests, Lipid Panels, Liver/Kidney Function Tests). It intentionally excludes handwritten doctor prescriptions and conversational chatbots from the initial release to eliminate clinical hallucination liabilities and regulatory exposure under CDSCO Medical Device Rules.

---

## 2. Goals & Non-Goals

### 2.1. Product Goals
* **G-01 (Comprehension):** Enable individuals with limited medical literacy or non-English proficiency to understand what their diagnostic biomarkers measure in everyday terms within 60 seconds of upload.
* **G-02 (De-escalation & Anti-Panic):** Eliminate unnecessary health anxiety and "cyberchondria" by replacing alarming red asterisks and raw numbers with calm, color-coded visual gauges and contextual explanations.
* **G-03 (Doctor Empowerment):** Equip patients and caregivers with 2–3 specific, informed questions to ask their prescribing physician at their next follow-up consultation.
* **G-04 (Accessibility First):** Provide 1-click native voice narration (Text-to-Speech) in regional Indian languages (Hindi, Tamil, Telugu, English) to serve elderly and low-literacy users.
* **G-05 (Privacy & Zero Retention):** Operate under a strict, verifiable DPDP-compliant "Zero-Data-Retention" policy where medical records are processed entirely in transient memory and automatically purged post-session.

### 2.2. Non-Goals (Strict Out-of-Scope for MVP)
* **NG-01 (No Autonomous Diagnosis):** The product will **never** diagnose a medical condition, disease, or pathology based on lab values (e.g., will never output *"You have Type 2 Diabetes"* or *"You have Chronic Kidney Disease"*).
* **NG-02 (No Medication Advice or Dosage Alteration):** The product will **never** recommend starting, stopping, increasing, or decreasing any pharmaceutical drug or therapy.
* **NG-03 (No Handwritten Prescription Deciphering):** The MVP will **not** attempt to parse or interpret cursive, handwritten doctor slips due to high clinical error rates (>25%).
* **NG-04 (No Persistent User Accounts / Profiles):** The MVP will **not** maintain user databases, login credentials, passwords, or stored patient histories.
* **NG-05 (No Free-Form Conversational Medical Chat):** The product will **not** provide an open-ended medical chatbot interface, preventing conversational drift into unauthorized practice of medicine.
* **NG-06 (No Commercial Teleconsultation or Medicine Upselling):** The product will **not** act as an e-commerce funnel for pharmacy sales or sponsored doctor appointments.

---

## 3. Target User Personas

### Persona A: Smt. Kamla Devi (68, Retired Teacher, Tier-2 City)
* **Background:** Manages hypertension and mild diabetes. Holds a budget Android smartphone (Samsung Galaxy M04). Comfortable speaking and reading Hindi; struggles with technical English medical terms.
* **Pain Point:** Receives an HbA1c and lipid report from a local lab with multiple values highlighted in red bold text. Cannot understand if she is in danger and waits in extreme anxiety for four days until her specialist appointment.
* **Product Need:** A simple screen where she can upload her report, listen to a 45-second explanation in Hindi audio, and see calm green/amber indicators.

### Persona B: Rajesh Nair (34, Software Engineer, Bengaluru)
* **Background:** Caregiver living in a metro city, remotely managing healthcare for his elderly parents residing in Kerala.
* **Pain Point:** Parents receive lab PDFs on WhatsApp and forward them to him. Rajesh spends hours searching Google/Reddit to decode unfamiliar markers like *eGFR* and *Alkaline Phosphatase*, worried that search engines will show worst-case cancer scenarios.
* **Product Need:** A rapid tool to generate a clear, objective summary with specific questions his parents can ask their local doctor.

---

## 4. User Stories & Acceptance Criteria

### Story 1: Document Upload & Language Selection
* **As a** vernacular patient holding a printed blood test report,  
* **I want to** take a photo of my report and pick my language on a single, clean screen without signing up,  
* **So that** I can get an immediate explanation without passwords or app installation hurdles.

#### Acceptance Criteria (Gherkin):
```gherkin
Scenario: Successful document upload with language selection
  Given the user lands on the ReportSaathi homepage
  When the user selects "हिन्दी" as their preferred language
  And uploads a valid printed lab report PDF or JPEG photo
  Then the system displays an upload progress bar
  And transitions to the in-memory processing screen within 2 seconds
```

### Story 2: In-Memory Processing & Privacy Transparency
* **As a** privacy-conscious user,  
* **I want to** see that my health document is being read safely without being stored permanently,  
* **So that** I have full confidence that my personal medical data will not leak.

#### Acceptance Criteria:
```gherkin
Scenario: Transparent progress check
  Given an uploaded lab report is being analyzed
  When the system extracts text and reference ranges
  Then the user sees a 4-step progressive verification checklist
  And a permanent notice confirms data is processed in transient memory only
```

### Story 3: Plain-Language Report Card & Range Indication
* **As an** anxious patient whose lab report has numbers out of range,  
* **I want to** see whether my numbers are normal or slightly elevated on a calm, color-coded gauge with plain-language definitions,  
* **So that** I understand what the tests measure without panicking.

#### Acceptance Criteria:
```gherkin
Scenario: Displaying simplified biomarker card
  Given a parsed lab report containing "HbA1c: 7.4% (Normal: 4.0 - 5.6%)"
  When the Report Card is rendered
  Then the status is displayed as "Slightly Elevated" with a warm amber badge (#D97706)
  And an objective 2-sentence plain-language explanation describes what HbA1c measures
  And no diagnostic disease labels (e.g. "Diabetes") are asserted
```

### Story 4: Vernacular Voice Narration (Audio Readout)
* **As an** elderly user with diminished vision or reading fatigue,  
* **I want to** tap a single prominent button to hear the explanation spoken aloud in my language,  
* **So that** I can comprehend the results without struggling to read small screen text.

#### Acceptance Criteria:
```gherkin
Scenario: 1-Click native audio narration
  Given the Report Card is rendered in Hindi
  When the user taps "[ ▶ सुनो (Listen in Hindi) ]"
  Then natural-sounding Hindi voice audio begins playing within 2.5 seconds
  And an interactive waveform scrubber with a pause button is displayed
```

### Story 5: Doctor Consultation Questions & Session Purge
* **As a** patient preparing for a follow-up appointment,  
* **I want to** receive 2–3 specific questions tailored to my report and be able to scrub my data immediately,  
* **So that** I have a productive dialogue with my doctor and leave zero digital footprint.

#### Acceptance Criteria:
```gherkin
Scenario: Doctor preparation and data purge
  Given the user has reviewed their Report Card
  When they scroll to the bottom
  Then they see 2-3 tailored questions for their doctor consultation
  And when they tap "[ 🗑 Clear Session & Delete Data ]"
  Then all session memory is immediately wiped and the user is returned to the clean upload screen
```

---

## 5. Numbered Functional Requirements

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
| FUNCTIONAL REQUIREMENT MODULES                                                                                       |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|  FR-01 to FR-04: Document Ingestion & File Pre-Flight                                                                |
|  FR-05 to FR-08: Text Extraction & Entity Parsing                                                                    |
|  FR-09 to FR-12: Deterministic Range Comparison & Clinical Grounding                                                 |
|  FR-13 to FR-16: Layman Translation & Multilingual Output                                                            |
|  FR-17 to FR-19: Voice Synthesis (Text-to-Speech)                                                                    |
|  FR-20 to FR-22: Doctor Preparation & Actionable Output                                                              |
|  FR-23 to FR-26: Privacy, Ephemeral Lifecycle & Safety Guards                                                        |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 5.1. Document Ingestion & Pre-Flight
* **FR-01 (Multi-Format Support):** The system shall accept PDF documents (up to 10MB, up to 5 pages) and JPEG, PNG, and WebP image files (up to 10MB).
* **FR-02 (Mobile Capture Integration):** The web interface shall trigger the native mobile camera capture interface via `<input type="file" capture="environment">` on Android/iOS.
* **FR-03 (Pre-Flight Resolution Check):** The system shall inspect uploaded images for minimal resolution (minimum 800×600 pixels) and detect severe blurriness via a Laplacian variance check before processing.
* **FR-04 (Ephemeral Streaming):** Uploaded files shall be received as temporary in-memory streams and shall **never** be written to persistent database storage or permanent cloud object stores.

### 5.2. Text Extraction & Entity Parsing
* **FR-05 (Deterministic PDF Parsing):** For digital PDF uploads, the system shall directly extract the embedded text layer using deterministic PDF layout parsers (`pdfplumber` / `PyMuPDF`), bypassing optical character recognition to achieve >99% character accuracy.
* **FR-06 (Optical Character Recognition Fallback):** For image uploads and scanned PDFs, the system shall utilize an OCR pipeline (`Tesseract OCR`) with image thresholding and contrast optimization.
* **FR-07 (Medical Entity Mapping):** The extraction engine shall identify four mandatory tuples for each biomarker:
  1. `Test Name` (e.g., *Serum Creatinine, HbA1c, TSH*)
  2. `Observed Numeric Value` (e.g., *1.45, 7.4, 3.2*)
  3. `Measurement Unit` (e.g., *mg/dL, %, uIU/mL*)
  4. `Reference Interval` (e.g., *0.70 - 1.20, 4.0 - 5.6*)
* **FR-08 (Uncertainty Flagging):** If a biomarker's numeric value or unit is partially obscured or ambiguous (OCR confidence <90%), the system shall flag the parameter as `UNCERTAIN` rather than guessing.

### 5.3. Deterministic Range Comparison & Clinical Grounding
* **FR-09 (Strict Range Grounding):** The system shall categorize biomarker values **strictly against the reference range printed on the uploaded report**. It shall not apply external baseline ranges unless the report range is missing.
* **FR-10 (Deterministic Classification Rules):** Range classification shall execute via deterministic mathematical logic:
  * If $Value < Min$: Status = `BELOW_NORMAL` (Blue badge `#2563EB`)
  * If $Min \le Value \le Max$: Status = `NORMAL` (Green badge `#16A34A`)
  * If $Max < Value \le (Max \times 1.5)$: Status = `SLIGHTLY_ELEVATED` (Warm Amber badge `#D97706`)
  * If $Value > (Max \times 1.5)$: Status = `ELEVATED` (Muted Coral badge `#DC2626`)
* **FR-11 (Missing Range Protocol):** If a lab report does not provide a reference range for a test, the system shall mark the status as `RANGE_UNAVAILABLE` and explicitly instruct the user to verify the number with their doctor.
* **FR-12 (No Risk Compounding):** The system shall evaluate each parameter independently and shall **never** calculate composite disease risk scores (e.g., Framingham, ASCVD).

### 5.4. Layman Translation & Multilingual Output
* **FR-13 (Layman Mapping):** The system shall map technical medical test names to everyday biological descriptions (e.g., *SGPT / ALT* → *"Liver enzyme check"*; *eGFR* → *"Kidney filtering efficiency"*).
* **FR-14 (Non-Alarmist Summaries):** The system shall generate a concise 1–2 sentence plain-language summary for each out-of-range biomarker, focusing on biological function and common non-emergency factors (e.g., hydration, recent meals, physical exertion).
* **FR-15 (Multilingual Vernacular Generation):** The system shall provide complete translations across four launch languages:
  1. English
  2. Hindi (`हिन्दी`)
  3. Telugu (`తెలుగు`)
  4. Tamil (`தமிழ்`)
* **FR-16 (Respectful Terminology):** All vernacular copy shall employ formal, respectful honorific phrasing suitable for elder communication in India.

### 5.5. Voice Synthesis (Text-to-Speech)
* **FR-17 (1-Click Voice Readout):** The system shall provide a single prominent button to play natural-sounding voice narration of the overall report summary in the chosen vernacular language.
* **FR-18 (Audio Player Controls):** The audio interface shall feature an interactive play/pause toggle, a visual scrubber progress bar, and a playback speed controller (1.0x / 0.8x for slower senior listening).
* **FR-19 (Client-Side Audio Streaming):** Audio synthesis shall be streamed in lightweight MP3 or Opus formats (file size <300KB) to ensure rapid playback on low-bandwidth 3G/4G networks.

### 5.6. Doctor Preparation & Actionable Output
* **FR-20 (Doctor Question Generator):** The system shall generate exactly 2 to 3 contextual, respectful questions for the patient to ask their doctor at their next consultation.
* **FR-21 (Objective Formatting):** Doctor questions must be framed constructively (e.g., *"Should we monitor this value again in 3 months?"*) and must never instruct the doctor on clinical decisions.
* **FR-22 (Printable / Shareable Summary):** The UI shall support native browser printing (`window.print()`) formatted into a clean, single-page summary card that patients can bring to the clinic.

### 5.7. Privacy, Ephemeral Lifecycle & Safety Guards
* **FR-23 (Zero Persistent Data Retention):** All uploaded files, extracted raw text, generated explanations, and audio buffers must be scrubbed from server RAM within **15 minutes** of generation or immediately upon session reset.
* **FR-24 (Client-Triggered Purge):** The UI shall provide a prominent `[ 🗑 Clear Session & Delete Data ]` button that immediately triggers a backend cache purge and clears browser session storage.
* **FR-25 (Mandatory Statutory Disclaimer):** Every screen presenting explanations shall render a prominent, non-dismissible legal disclaimer confirming the tool is for educational purposes and does not replace an RMP consultation.
* **FR-26 (Diagnostic Blacklist Interceptor):** A deterministic regex filter shall intercept all model outputs, blocking forbidden words (e.g., *"You have been diagnosed with"*, *"Stop taking"*, *"Prescription"*).

---

## 6. Non-Functional Requirements (NFRs)

### 6.1. Performance & Latency
* **NFR-01 (End-to-End Latency):** From the moment an upload completes to the rendering of the simplified Report Card, total elapsed time shall not exceed **8.0 seconds** over a standard 4G mobile connection.
* **NFR-02 (Audio Startup Time):** Tapping the audio narration button shall begin voice playback within **2.5 seconds**.
* **NFR-03 (Payload Size):** The initial HTML/CSS/JavaScript bundle delivered to the client shall not exceed **60 KB (compressed)**, ensuring rapid loading on budget Android devices.

### 6.2. Hardware & Browser Constraints
* **NFR-04 (Viewport Resilience):** The UI layout must be fully functional without horizontal clipping or broken elements on screens as narrow as **320px width**, with the design baseline set at **360dp width**.
* **NFR-05 (Low Memory Footprint):** Client-side memory usage shall remain under **40 MB**, preventing browser tab crashes on low-end smartphones with 1GB–2GB of total RAM.
* **NFR-06 (Browser Compatibility):** Must function seamlessly on Google Chrome (Android, v90+), Samsung Internet (v14+), Mobile Safari (iOS 14+), and Android WebViews.

### 6.3. Accessibility & Ergonomics
* **NFR-07 (Touch Target Minimum):** Every clickable button, chip, and link must have a physical touch bounding box of at least **48×48dp** (primary actions at **56dp**).
* **NFR-08 (Contrast Compliance):** All text elements must achieve a contrast ratio of at least **7:1 against their background** (WCAG AAA standard for elderly vision).
* **NFR-09 (Typography Scale):** Body text must not fall below **16px**; headings must be at least **22px**; line-height for Indic scripts must be maintained at **1.55x to 1.65x**.

### 6.4. Reliability & Availability
* **NFR-10 (Service Uptime):** The web application shall maintain **99.5% uptime** during operational hours.
* **NFR-11 (Graceful Degradation):** If optical character recognition fails or external translation services timeout, the system must display clear vernacular failure notices with guided recovery actions rather than blank screens or raw stack traces.

---

## 7. Safety & Regulatory Requirements

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
| STATUTORY COMPLIANCE BOUNDARIES                                                                                      |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|  SR-01: CDSCO SaMD Exemption (Informational safe harbor; non-diagnostic)                                             |
|  SR-02: Telemedicine Practice Guidelines, 2020 (No RMP impersonation; zero prescribing)                              |
|  SR-03: DPDP Act, 2023 (Section 5 notice; Section 6 consent; Section 12 erasure; zero retention)                    |
|  SR-04: Drugs & Magic Remedies Act, 1954 (Zero cure/mitigation claims for Schedule J diseases)                       |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

* **SR-01 (CDSCO Software as a Medical Device Exclusion):** The platform must operate strictly within the informational/educational safe harbor of the CDSCO Medical Device Rules, 2017. It shall not output diagnostic assertions, treatment titrations, or clinical decision support driving therapeutic intervention.
* **SR-02 (Prohibition of Medical Practice):** The software shall never use doctor personas (e.g., *"Dr. AI"*), shall not prescribe pharmaceutical compounds, and shall explicitly defer all clinical decisions to Registered Medical Practitioners (RMPs) licensed under the National Medical Commission (NMC) Act.
* **SR-03 (DPDP Act 2023 Compliance):** 
  * Standalone notice in English and the 3 regional languages prior to document processing.
  * Affirmative user consent check before file parsing.
  * Automated data purging ensuring no personal health records are stored in databases or persistent storage volumes.
* **SR-04 (Schedule J Prohibition):** No text, summary, or question generated by the system shall claim to prevent, cure, or reverse any condition listed in Schedule J of the Drugs and Cosmetics Rules (including diabetes, hypertension, renal failure, cancer, cataracts).

---

## 8. Success Metrics & Validation KPIs

```
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Metric Category           | Specific KPI                         | Target Milestone (MVP Validation)                 |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| 1. Comprehension & Relief | Self-Reported Relief Rating          | ≥ 80% of users report reduced anxiety after view  |
| 2. Technical Accuracy     | Deterministic Range Accuracy         | 100% mathematical match with printed lab ranges   |
|                           | Medical Terminology Accuracy         | ≥ 95% clinical review approval on plain summaries |
| 3. Pipeline Success       | End-to-End Extraction Success        | ≥ 88% of standard printed lab reports parsed      |
| 4. Senior Accessibility   | Voice Narration Engagement           | ≥ 45% of users tap audio playback                 |
| 5. Flow Completion        | Funnel Completion Rate               | ≥ 70% from Upload landing to Report Card review   |
| 6. Safety Compliance      | False Diagnostic Assertions          | EXACTLY 0 instances                              |
|                           | Persistent Data Leaks                | EXACTLY 0 bytes stored permanently               |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
```
