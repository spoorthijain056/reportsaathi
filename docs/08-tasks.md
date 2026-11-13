# Implementation Task Plan: ReportSaathi MVP

**Document Reference:** `docs/08-tasks.md`  
**Related Documents:** `docs/05-prd.md` (PRD) | `docs/06-architecture.md` (Architecture) | `docs/06a-api-contract.md` (API Contract) | `docs/06b-safety-rules.md` (Safety Rules) | `docs/07-test-plan.md` (Test Plan)  
**Test Fixtures:** `tests/fixtures/` (10 Anonymised Sample Lab Reports)  
**Date:** November 2026  
**Status:** Ready for Sprint Execution  
**Granularity Rule:** Every task is scoped for a **single, reviewable Pull Request (PR)**.  

---

## 1. Execution Dependency Graph & Parallel Workstreams

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              WORKSTREAM PIPELINE MAP                                                 |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                                      |
|   [ MILESTONE 1: WALKING SKELETON & CONTRACT ]                                                                       |
|   Task 1.1 (Repo Setup) ──► Task 1.2 (Pydantic Models) ──► Task 1.3 (Deployed Skeleton) ──► Task 1.4 (UI Shell)     |
|                                                                                                                      |
|   [ MILESTONE 2: INGESTION & MEMORY ENGINE ]                                                                         |
|         ┌───────────────────────────────────────┬────────────────────────────────────┐                               |
|         ▼ [PARALLEL WORKSTREAM A]               ▼ [PARALLEL WORKSTREAM B]            ▼ [PARALLEL WORKSTREAM C]       |
|   Task 2.1 (Pre-Flight Blur Check)        Task 2.2 (TTLCache Zero-Disk)        Task 2.3 (Rate Limiting)              |
|         │                                       │                                    │                               |
|         └───────────────────────────────────────┼────────────────────────────────────┘                               |
|                                                 ▼                                                                    |
|                                           Task 2.4 (Screen 1 Upload Frontend)                                        |
|                                                                                                                      |
|   [ MILESTONE 3: DETERMINISTIC PARSING & RANGE ENGINE ]                                                              |
|         ┌───────────────────────────────────────┬────────────────────────────────────┐                               |
|         ▼ [PARALLEL WORKSTREAM A]               ▼ [PARALLEL WORKSTREAM B]            ▼ [PARALLEL WORKSTREAM C]       |
|   Task 3.1 (Vector PDF Parser)            Task 3.2 (OCR Fallback)              Task 3.3 (Non-Lab Classifier)         |
|         │                                       │                                                                    |
|         └───────────────────────────────────────┴────────────────────────────────────┐                               |
|                                                                                      ▼                               |
|                                            Task 3.4 (Deterministic Range Comparator) [HUMAN APPROVAL]                |
|                                            Task 3.5 (Critical Panic Evaluator)       [HUMAN APPROVAL]                |
|                                                                                                                      |
|   [ MILESTONE 4: AI LAYMAN ENGINE & SAFETY INTERCEPTOR ]                                                             |
|         ┌───────────────────────────────────────┬────────────────────────────────────┐                               |
|         ▼ [PARALLEL WORKSTREAM A]               ▼ [PARALLEL WORKSTREAM B]            ▼ [PARALLEL WORKSTREAM C]       |
|   Task 4.1 (Prompt & Layman Mapping)      Task 4.2 (Blacklist Interceptor)     Task 4.4 (Screen 2 Processing UI)     |
|   [HUMAN APPROVAL]                        [HUMAN APPROVAL]                           │                               |
|         │                                       │                                    │                               |
|         └───────────────────────────────────────┴────────────────────────────────────┘                               |
|                                                 ▼                                                                    |
|                                           Task 4.3 (Vernacular Translation HI/TE/TA) [HUMAN APPROVAL]                |
|                                                                                                                      |
|   [ MILESTONE 5: VOICE SYNTHESIS & REPORT CARD UI ]                                                                  |
|         ┌────────────────────────────────────────────────────────────────────────────┐                               |
|         ▼ [PARALLEL WORKSTREAM A]                                                    ▼ [PARALLEL WORKSTREAM B]       |
|   Task 5.1 (edge-tts Voice Pipeline)                                           Task 5.3 (Screen 3 UI & Gauges)       |
|   Task 5.2 (Process & Audio Endpoints)                                         Task 5.4 (Printable A4 Sheet)         |
|         │                                                                            │                               |
|         └───────────────────────────────────────┬────────────────────────────────────┘                               |
|                                                 ▼                                                                    |
|   [ MILESTONE 6: AUDIT, END-TO-END VERIFICATION & RELEASE ]                                                          |
|   Task 6.1 (DPDP Zero-Retention Audit) [HUMAN APPROVAL]                                                              |
|   Task 6.2 (Adversarial Safety Suite)  [HUMAN APPROVAL]                                                              |
|   Task 6.3 (10 Fixtures E2E Test Suite)                                                                              |
|   Task 6.4 (Budget Phone Ergonomics & Performance Audit)                                                             |
|   Task 6.5 (Production Release & Cutover) [HUMAN APPROVAL]                                                           |
|                                                                                                                      |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Detailed Task Specifications by Milestone

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
| LEGEND FOR TASK ATTRIBUTES:                                                                                          |
| • Owner:        Backend | Frontend | Database (In-Memory) | AI / NLP | QA | DevOps | Compliance                  |
| • Requirements: PRD (docs/05-prd.md), Architecture (docs/06), Safety (docs/06b)                                      |
| • Tests:        Test IDs from docs/07-test-plan.md                                                                   |
| • Parallel:     Can run concurrently with specified tasks                                                           |
| • Approval:     Flagged if clinical, regulatory, legal, or production sign-off is mandatory                         |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

### Milestone 1: Foundation, Contract & Deployed Walking Skeleton

#### Task 1.1: Repository Setup, Tooling & Test Harness
* **Owner:** Backend / DevOps
* **Requirements:** `NFR-03`, `NFR-10`
* **Tests:** `TC-NFR-10`, environment bootstrapping check
* **Dependencies:** None
* **Can Run in Parallel With:** None
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Configure Python 3.11+ virtual environment with `pyproject.toml` / `requirements.txt`.
  * Add dependencies: `fastapi`, `uvicorn`, `pydantic`, `pytest`, `pytest-asyncio`, `ruff`.
  * Create base directory structure (`app/`, `tests/`, `static/`).
  * Add GitHub Actions CI workflow to run linter and test suite on commit.
* **Definition of Done (DoD):**
  * `pytest` runs and passes on empty test suite in CI.
  * `ruff check .` executes with zero errors.

#### Task 1.2: API Contract Scaffold, Pydantic Data Models & RFC 7807 Error Envelope
* **Owner:** Backend
* **Requirements:** `FR-01`, `FR-07`, `FR-10`, `NFR-11`, `docs/06a-api-contract.md`
* **Tests:** `TC-FR-01`, `TC-FR-07`, `TC-FR-10` (Schema validation)
* **Dependencies:** Task 1.1
* **Can Run in Parallel With:** None
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement Pydantic schemas in `app/schemas.py`: `ExtractedBiomarker`, `BiomarkerStatus` (Enum), `DoctorQuestion`, `ProcessedReportCard`.
  * Implement RFC 7807 problem details error model and exception handler in `app/exceptions.py`.
  * Add automated contract test verifying that schemas match `docs/06a-api-contract.md` field-for-field.
* **Definition of Done (DoD):**
  * Schemas validate valid JSON payloads from `tests/fixtures/sample_01_cbc_normal.json`.
  * Schema serialization tests pass 100%.

#### Task 1.3: Deployed Walking Skeleton & Health Probe
* **Owner:** Backend / DevOps
* **Requirements:** `NFR-10`, `docs/06a-api-contract.md` Section 2.5
* **Tests:** `GET /healthz` returning 200 OK
* **Dependencies:** Task 1.1, Task 1.2
* **Can Run in Parallel With:** None
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement FastAPI app in `app/main.py` with `GET /healthz` endpoint returning `{status: "healthy", version: "1.0.0-mvp"}`.
  * Create `Dockerfile` with multi-stage build.
  * Connect repository to Render.com / Hugging Face Spaces free tier for automated CD.
* **Definition of Done (DoD):**
  * Live URL (`https://reportsaathi.onrender.com/healthz`) returns HTTP 200 over public internet with valid HTTPS certificate.

#### Task 1.4: Minimal Walking Skeleton UI Shell (360dp Viewport)
* **Owner:** Frontend
* **Requirements:** `NFR-03`, `NFR-04`, `NFR-07`, `NFR-09`, `docs/04-design.md`
* **Tests:** `TC-NFR-03`, `TC-NFR-04`, `TC-NFR-07`, `TC-NFR-09`
* **Dependencies:** Task 1.3
* **Can Run in Parallel With:** None
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Create single-page `static/index.html` mounted by FastAPI at `GET /`.
  * Configure Tailwind standalone CSS (no node build pipeline required).
  * Enforce mobile viewport `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">`.
  * Establish Indic system font stack and `line-height: 1.6` base styles.
  * Add client fetch probe displaying backend health status on screen.
* **Definition of Done (DoD):**
  * Page loads on simulated 320px–360dp mobile viewports with zero horizontal scrollbar.
  * Asset size is `< 25 KB` total gzipped.

---

### Milestone 2: Ingestion, Validation & Ephemeral Memory Engine

#### Task 2.1: Pre-Flight File Validation & OpenCV Blur Detector
* **Owner:** Backend
* **Requirements:** `FR-01`, `FR-03`, `docs/06a-api-contract.md` Section 2.1
* **Tests:** `TC-FR-01`, `TC-FR-03`
* **Dependencies:** Task 1.2
* **Can Run in Parallel With:** Tasks 2.2, 2.3
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement file pre-flight validator in `app/services/validator.py`:
    * Verify file magic bytes (`%PDF-`, `\xFF\xD8\xFF`, `\x89PNG`).
    * Check byte size limit ($10\text{ MB}$).
    * Implement OpenCV Laplacian variance check on decoded image buffers ($\text{Variance} \ge 100$).
  * Expose via internal function `validate_uploaded_file(file_bytes, filename)`.
* **Definition of Done (DoD):**
  * Unit tests pass rejecting blurry photos (`Variance < 100`), oversized files, and fake `.pdf` text files.

#### Task 2.2: Ephemeral In-Memory Storage & TTLCache Manager
* **Owner:** Database (In-Memory) / Backend
* **Requirements:** `FR-04`, `FR-23`, `FR-24`, `SR-03`, `docs/06b-safety-rules.md` Rules P-01 & P-03
* **Tests:** `TC-FR-04`, `TC-FR-23`, `TC-FR-24`, `TC-SEC-02`
* **Dependencies:** Task 1.2
* **Can Run in Parallel With:** Tasks 2.1, 2.3
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement `SessionMemoryStore` in `app/services/session_store.py` using `cachetools.TTLCache(maxsize=500, ttl=900)`.
  * Store files strictly as in-memory `io.BytesIO` objects with HMAC-SHA256 session keys.
  * Implement `POST /api/session/purge` endpoint to evict session and trigger `gc.collect()`.
* **Definition of Done (DoD):**
  * Automated test confirms session data auto-purges after 900 seconds.
  * Linux `inotifywait` test verifies zero file creation on `/tmp` or server disk.

#### Task 2.3: Rate Limiting Middleware (`slowapi`)
* **Owner:** Backend / Security
* **Requirements:** `NFR-10`, `docs/06a-api-contract.md`, `TC-SEC-01`
* **Tests:** `TC-SEC-01`
* **Dependencies:** Task 1.2
* **Can Run in Parallel With:** Tasks 2.1, 2.2
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Integrate `slowapi` limiter into FastAPI app.
  * Configure limit: `5/10minute` per client IP on mutation routes.
  * Add response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
* **Definition of Done (DoD):**
  * 6th consecutive request from same IP returns HTTP 429 with RFC 7807 problem details.

#### Task 2.4: Screen 1 Frontend (Upload & Language Matrix)
* **Owner:** Frontend
* **Requirements:** `FR-01`, `FR-02`, `FR-15`, `NFR-07`, `NFR-08`, `docs/04-design.md` Section 1.1
* **Tests:** `TC-FR-01`, `TC-FR-02`, `TC-NFR-07`, `TC-NFR-08`
* **Dependencies:** Task 1.4, Task 2.1
* **Can Run in Parallel With:** Tasks 2.2, 2.3
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement Screen 1 UI states in `static/index.html` and `static/app.js`:
    * Default state: 4 language chips (`हिन्दी`, `English`, `తెలుగు`, `தமிழ்`), large dashed upload container.
    * Empty state: Instructional prompt with well-lit sample guide.
    * Loading state: Progress bar showing upload percentage.
    * Error state: Blurry photo retry card and invalid file notices.
  * Wire upload form to `POST /api/upload`.
* **Definition of Done (DoD):**
  * Touch targets measure $\ge 52\text{dp}$.
  * Camera triggers on mobile device; upload progress displays accurately.

---

### Milestone 3: Deterministic Parsing & Clinical Range Engine

#### Task 3.1: Vector PDF Table Parser (`pdfplumber` / `PyMuPDF`)
* **Owner:** Backend
* **Requirements:** `FR-05`, `FR-07`
* **Tests:** `TC-FR-05`, `TC-FR-07` against `sample_01`, `sample_02`, `sample_03`
* **Dependencies:** Task 2.1
* **Can Run in Parallel With:** Task 3.2
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement `parse_vector_pdf()` in `app/services/pdf_parser.py`:
    * Extract tabular columns (Test Name, Observed Value, Unit, Reference Interval).
    * Filter out lab metadata, footer disclaimers, and doctor signature lines.
    * Output structured list of unclassified biomarker dictionaries.
* **Definition of Done (DoD):**
  * Extracts 100% of biomarkers from `sample_01_cbc_normal.txt` and `sample_02_diabetic_elevated.txt` without OCR.

#### Task 3.2: Scanned Document OCR Fallback Pipeline (`Tesseract OCR`)
* **Owner:** Backend / AI
* **Requirements:** `FR-06`, `FR-08`
* **Tests:** `TC-FR-06`, `TC-FR-08`
* **Dependencies:** Task 3.1
* **Can Run in Parallel With:** Task 3.1
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement `parse_scanned_image()` in `app/services/ocr_parser.py`:
    * Apply OpenCV grayscale, Otsu thresholding, and deskewing.
    * Execute `pytesseract.image_to_data()` to capture word-level confidence.
    * Reconstruct tabular lines; mark words with confidence $< 90\%$ as `UNCERTAIN`.
* **Definition of Done (DoD):**
  * Parses simulated scanned photos of lab printouts into structured lines.

#### Task 3.3: Non-Lab Document Classifier & Validation Filter
* **Owner:** Backend
* **Requirements:** `FR-08`, `NFR-11`, `docs/06a-api-contract.md`
* **Tests:** `TC-FR-01` failure case against `sample_10_invalid_non_lab_doc`
* **Dependencies:** Task 3.1, Task 3.2
* **Can Run in Parallel With:** None
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement validation check verifying that extracted tokens contain at least one valid diagnostic biomarker and reference interval pair.
  * If zero diagnostic markers are identified, reject document with HTTP 422 `ERR_NON_LAB_DOCUMENT`.
* **Definition of Done (DoD):**
  * `sample_10_invalid_non_lab_doc.json` (prescription invoice) is rejected with clear user-facing guidance.

#### Task 3.4: Deterministic Clinical Range Comparator Engine
* **Owner:** Backend / Clinical Safety
* **Requirements:** `FR-09`, `FR-10`, `FR-11`, `FR-12`, `SR-01`, `docs/06b-safety-rules.md` Section 3
* **Tests:** `TC-FR-09`, `TC-FR-10`, `TC-FR-11`, `TC-FR-12`, `TC-EDG-01`
* **Dependencies:** Task 3.1
* **Can Run in Parallel With:** Task 3.5
* **Human Approval Required:** **YES [CLINICAL APPROVAL: Pathologist / Medical Lead sign-off on mathematical thresholds]**
* **Pull Request Scope:**
  * Implement pure mathematical evaluation in `app/services/range_evaluator.py`:
    * $V < Min \implies \text{BELOW\_NORMAL}$
    * $Min \le V \le Max \implies \text{NORMAL}$
    * $Max < V \le (Max \times 1.5) \implies \text{SLIGHTLY\_ELEVATED}$
    * $V > (Max \times 1.5) \implies \text{ELEVATED}$
    * $Min = \text{null} \lor Max = \text{null} \implies \text{RANGE\_UNAVAILABLE}$
  * Zero AI model calls in this module.
* **Definition of Done (DoD):**
  * Unit test suite verifies boundary values ($V = Max$, $V = Min$) and missing ranges with 100% mathematical accuracy.

#### Task 3.5: Critical Emergency Panic Value Evaluator
* **Owner:** Backend / Clinical Safety
* **Requirements:** `SR-01`, `docs/06b-safety-rules.md` Section 4
* **Tests:** `TC-ADV-03` against `sample_07_critical_emergency_panic`
* **Dependencies:** Task 3.4
* **Can Run in Parallel With:** Task 3.4
* **Human Approval Required:** **YES [CLINICAL APPROVAL: Doctor sign-off on Acute Panic Value cutoffs]**
* **Pull Request Scope:**
  * Implement acute emergency checker in `app/services/panic_evaluator.py`:
    * Platelets $< 20,000\text{ /µL}$
    * Hemoglobin $< 6.0\text{ g/dL}$
    * Serum Potassium $> 6.2\text{ mEq/L}$
    * Glucose $< 50\text{ mg/dL}$ or $> 450\text{ mg/dL}$
  * Sets `critical_flag_triggered = True` and binds Emergency Crimson Banner text.
* **Definition of Done (DoD):**
  * `sample_07` correctly triggers acute emergency state and binds `tel:112` call action.

---

### Milestone 4: AI Layman Engine, Translation & Safety Interceptor

#### Task 4.1: Layman Medical Dictionary & Grounded Prompt Engine
* **Owner:** AI / Backend
* **Requirements:** `FR-13`, `FR-14`, `FR-20`, `FR-21`, `SR-02`, `SR-04`, `docs/06b-safety-rules.md` Section 6
* **Tests:** `TC-FR-13`, `TC-FR-14`, `TC-FR-20`, `TC-FR-21`, `TC-SR-01`, `TC-SR-02`, `TC-SR-04`
* **Dependencies:** Task 3.4
* **Can Run in Parallel With:** Task 4.2
* **Human Approval Required:** **YES [CLINICAL & LEGAL APPROVAL: Non-diagnostic prompt grounding sign-off]**
* **Pull Request Scope:**
  * Implement Gemini 1.5 Flash client in `app/services/llm_engine.py` with `temperature=0.0`.
  * Inject system prompt enforcing negative constraints (no diagnosis, no prescription, no dosage advice).
  * Format prompt with pre-computed deterministic biomarker statuses.
  * Instruct model to generate 1–2 sentence layman descriptions and exactly 2–3 doctor questions.
* **Definition of Done (DoD):**
  * Generates valid JSON adhering to schema without asserting disease labels across all test fixtures.

#### Task 4.2: Deterministic Blacklist & Safety Interceptor
* **Owner:** Backend / Clinical Safety
* **Requirements:** `FR-26`, `SR-02`, `SR-04`, `docs/06b-safety-rules.md` Section 5
* **Tests:** `TC-FR-26`, `TC-ADV-01`, `TC-ADV-02`
* **Dependencies:** Task 4.1
* **Can Run in Parallel With:** Task 4.1
* **Human Approval Required:** **YES [LEGAL & COMPLIANCE APPROVAL: 50+ Banned Medical Terms regex list]**
* **Pull Request Scope:**
  * Implement `sanitize_ai_output()` in `app/services/safety_interceptor.py`:
    * Scan model output for regex patterns: `\byou have\b`, `\bdiagnosed with\b`, `\bstop taking\b`, `\btake \d+mg\b`, `\bcure for diabetes\b`.
    * If pattern matches, replace offending string with safe neutral educational fallback.
* **Definition of Done (DoD):**
  * Adversarial injection attack tests (`TC-ADV-01`, `TC-ADV-02`) pass 100%.

#### Task 4.3: Vernacular Localization Engine (Hindi, Tamil, Telugu)
* **Owner:** AI / Frontend
* **Requirements:** `FR-15`, `FR-16`, `NFR-09`, `docs/04-design.md` Section 3.2
* **Tests:** `TC-FR-15`, `TC-FR-16`, `TC-EDG-04`, `TC-NFR-09`
* **Dependencies:** Task 4.1, Task 4.2
* **Can Run in Parallel With:** None
* **Human Approval Required:** **YES [LINGUISTIC APPROVAL: Native speakers review Hindi, Tamil, Telugu phrasing]**
* **Pull Request Scope:**
  * Configure multilingual output mode in LLM prompt.
  * Validate that Devanagari, Tamil, and Telugu scripts render cleanly.
  * Verify elder-respectful honorifics (Hindi: *आप / आपका*; Tamil: *உங்கள்*; Telugu: *మీరు / మీ*).
  * Enforce CSS `overflow-wrap: break-word` and line-height $1.6\times$.
* **Definition of Done (DoD):**
  * `sample_02` renders in Hindi, Tamil, and Telugu without glyph clipping or text overflow.

#### Task 4.4: Screen 2 Frontend (In-Memory Processing Stepper)
* **Owner:** Frontend
* **Requirements:** `NFR-01`, `NFR-04`, `NFR-11`, `docs/04-design.md` Section 1.2
* **Tests:** `TC-NFR-01`, Screen 2 state verification
* **Dependencies:** Task 2.4, Task 3.1
* **Can Run in Parallel With:** Tasks 4.1, 4.2
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement Screen 2 UI in `static/index.html`:
    * Animated 4-step clinical verification stepper with green checkmarks.
    * Calming privacy notice explaining in-memory processing.
    * Error card with retry button if parsing fails.
* **Definition of Done (DoD):**
  * Transitions smoothly between upload completion and result delivery.

---

### Milestone 5: Voice Synthesis, Report Card UI & Action Screen

#### Task 5.1: Native Audio Synthesis Pipeline (`edge-tts`)
* **Owner:** Backend / AI
* **Requirements:** `FR-17`, `FR-19`, `NFR-02`
* **Tests:** `TC-FR-17`, `TC-FR-19`, `TC-NFR-02`
* **Dependencies:** Task 4.3
* **Can Run in Parallel With:** Task 5.3
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement `synthesize_audio()` in `app/services/tts_engine.py` using `edge-tts`:
    * Map language codes to neural voices: `hi` $\to$ `hi-IN-SwaraNeural`, `ta` $\to$ `ta-IN-PallaviNeural`, `te` $\to$ `te-IN-ShrutiNeural`, `en` $\to$ `en-IN-NeerjaNeural`.
    * Stream lightweight MP3 payload ($< 300\text{ KB}$).
    * Fallback to Web Speech API signal if synthesis times out ($> 3.0\text{s}$).
* **Definition of Done (DoD):**
  * Synthesizes audio for 45-second summary in $< 2.2$ seconds.

#### Task 5.2: `POST /api/process` & `GET /api/audio/{session_id}` Integration
* **Owner:** Backend
* **Requirements:** All FRs, `docs/06a-api-contract.md` Sections 2.2 & 2.3
* **Tests:** Contract & Integration tests for `/api/process` and `/api/audio`
* **Dependencies:** Tasks 3.4, 3.5, 4.1, 4.2, 4.3, 5.1
* **Can Run in Parallel With:** Task 5.3
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement route handlers in `app/routes/process.py` and `app/routes/audio.py`.
  * Wire orchestrator: fetch session $\to$ parse text $\to$ evaluate ranges $\to$ call LLM $\to$ run blacklist $\to$ synthesize audio $\to$ return JSON.
* **Definition of Done (DoD):**
  * Automated integration test passes against all 10 fixtures in `tests/fixtures/`.

#### Task 5.3: Screen 3 Frontend (Report Card, Visual Gauge & Voice Player)
* **Owner:** Frontend
* **Requirements:** `FR-10`, `FR-13`, `FR-14`, `FR-17`, `FR-18`, `FR-20`, `FR-25`, `NFR-04`, `NFR-07`, `NFR-08`, `docs/04-design.md` Section 1.3
* **Tests:** `TC-FR-18`, `TC-FR-25`, `TC-NFR-07`, `TC-NFR-08`, `TC-ADV-03`
* **Dependencies:** Task 5.2
* **Can Run in Parallel With:** Tasks 5.1, 5.2
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement Screen 3 UI components:
    * Biomarker cards with continuous tri-color visual gauge (Blue/Green/Amber).
    * Audio bar with 1-click play/pause, scrubber, and $0.8\times/1.0\times$ speed control.
    * Doctor consultation questions container.
    * Mandatory statutory disclaimer in active language.
    * Emergency Crimson Alert banner when `critical_flag_triggered = True`.
    * Full-width `[ 🗑 Clear Session & Delete Data ]` button.
* **Definition of Done (DoD):**
  * Tested on 360dp mobile view; audio plays on single tap; clear button purges screen and memory.

#### Task 5.4: Printable Single-Page Summary (`window.print`)
* **Owner:** Frontend
* **Requirements:** `FR-22`
* **Tests:** `TC-FR-22`
* **Dependencies:** Task 5.3
* **Can Run in Parallel With:** None
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Implement print CSS media query (`@media print`):
    * Hide header navigation, audio controls, and upload buttons.
    * Format biomarker cards, layman explanations, and doctor questions into a clean A4 sheet.
* **Definition of Done (DoD):**
  * Browser print preview formats summary onto a single readable page.

---

### Milestone 6: Privacy Audit, End-to-End Hardening & Launch Readiness

#### Task 6.1: DPDP Act Zero-Retention & PII Telemetry Audit
* **Owner:** Compliance / DevOps
* **Requirements:** `FR-23`, `FR-24`, `SR-03`, `docs/06b-safety-rules.md` Section 7
* **Tests:** `TC-FR-23`, `TC-FR-24`, `TC-SEC-02`, `TC-SEC-03`
* **Dependencies:** Task 5.2
* **Can Run in Parallel With:** Tasks 6.2, 6.3, 6.4
* **Human Approval Required:** **YES [LEGAL & DPO APPROVAL: Data Protection Officer DPDP Sign-Off]**
* **Pull Request Scope:**
  * Execute 100 consecutive automated report uploads.
  * Audit server disk to verify zero persistent files created.
  * Audit server logs to verify zero patient PII/PHI logged.
  * Verify `Cache-Control: no-store` headers on all document responses.
* **Definition of Done (DoD):**
  * DPO sign-off report generated certifying DPDP Act 2023 compliance.

#### Task 6.2: Adversarial Safety Test Suite Execution
* **Owner:** QA / Clinical Safety
* **Requirements:** `SR-01`, `SR-02`, `SR-04`, `TC-ADV-01`, `TC-ADV-02`, `TC-ADV-03`
* **Tests:** 100% pass on adversarial test cases
* **Dependencies:** Task 5.2, Task 5.3
* **Can Run in Parallel With:** Tasks 6.1, 6.3, 6.4
* **Human Approval Required:** **YES [CLINICAL SAFETY APPROVAL: Medical Director Sign-off]**
* **Pull Request Scope:**
  * Run automated test runner executing 50+ adversarial prompt injections and dosage manipulation attempts.
  * Verify Blacklist Interceptor blocks 100% of attempts.
* **Definition of Done (DoD):**
  * Zero diagnostic statements emitted; medical director signs clinical release waiver.

#### Task 6.3: End-to-End Fixture Test Suite Execution (All 10 Sample Reports)
* **Owner:** QA
* **Requirements:** All PRD Functional Requirements (`FR-01` to `FR-26`)
* **Tests:** Automated execution of all 10 fixtures in `tests/fixtures/`
* **Dependencies:** Task 5.3
* **Can Run in Parallel With:** Tasks 6.1, 6.2, 6.4
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Automate end-to-end integration test runner against:
    * `sample_01` (Normal CBC)
    * `sample_02` (Diabetic)
    * `sample_03` (Renal KFT)
    * `sample_04` (Hepatic LFT)
    * `sample_05` (Lipid)
    * `sample_06` (Thyroid)
    * `sample_07` (Emergency Panic)
    * `sample_08` (Missing Range)
    * `sample_09` (Multi-Page Checkup)
    * `sample_10` (Invalid Prescription)
* **Definition of Done (DoD):**
  * All 10 fixtures pass with correct status, visual badges, and localized questions.

#### Task 6.4: Budget Phone Ergonomics & Performance Audit
* **Owner:** QA / Frontend
* **Requirements:** `NFR-01`, `NFR-03`, `NFR-04`, `NFR-05`, `NFR-06`, `NFR-07`, `NFR-08`
* **Tests:** `TC-NFR-01` through `TC-NFR-08`
* **Dependencies:** Task 5.3
* **Can Run in Parallel With:** Tasks 6.1, 6.2, 6.3
* **Human Approval Required:** No
* **Pull Request Scope:**
  * Audit client performance via Lighthouse on throttled 4G / 360dp mobile screen.
  * Verify total JS bundle is $< 45\text{ KB}$.
  * Verify contrast passes WCAG AAA ($7:1+$) across all screens.
  * Verify touch targets measure $\ge 48\times 48\text{dp}$.
* **Definition of Done (DoD):**
  * Lighthouse Performance $\ge 90$, Accessibility $\ge 95$.

#### Task 6.5: Production Deployment & DNS Cutover
* **Owner:** DevOps
* **Requirements:** `NFR-10`
* **Tests:** Live domain health check, Cloudflare SSL handshake
* **Dependencies:** Tasks 6.1, 6.2, 6.3, 6.4
* **Can Run in Parallel With:** None
* **Human Approval Required:** **YES [EXECUTIVE APPROVAL: Final Go/No-Go Release Sign-Off]**
* **Pull Request Scope:**
  * Configure production environment variables on Render.com.
  * Bind custom domain (`reportsaathi.org` or assigned domain).
  * Configure Cloudflare DNS, SSL Full (Strict), and DDoS rules.
  * Verify live end-to-end upload and audio playback.
* **Definition of Done (DoD):**
  * Application is live, accessible worldwide over HTTPS, passing all production health checks.

---

## 3. Human Approval Gate Summary Table

The following critical milestones are hard safety gates requiring human verification before code merging or deployment:

```
+──────────────+────────────────────────────────────────+─────────────────────────+────────────────────────────────────+
| Task ID      | Gated Milestone Component              | Mandatory Human Role    | Core Approval Focus                |
+──────────────+────────────────────────────────────────+─────────────────────────+────────────────────────────────────+
| Task 3.4     | Clinical Range Comparator Thresholds   | Clinical Pathologist    | Mathematical range formula accuracy|
| Task 3.5     | Acute Emergency Panic Value Cutoffs    | Medical Doctor (MD)     | Life-threatening threshold limits  |
| Task 4.1     | Layman Prompt Directives & Grounding   | Clinical Prompt Auditor | Zero-diagnostic grounding check    |
| Task 4.2     | Diagnostic Blacklist 50+ Term Regex    | Legal & Regulatory Lead | CDSCO & Drugs Act compliance list  |
| Task 4.3     | Vernacular Translations (HI, TE, TA)   | Native Medical Speakers | Dialect clarity & respectfulness   |
| Task 6.1     | DPDP Act Zero-Retention Compliance     | Data Protection Officer | Zero-disk & PII log audit certify  |
| Task 6.2     | Adversarial Injection Defense Waiver   | Clinical Safety Lead    | Clinical safety sign-off waiver    |
| Task 6.5     | Final Production Launch Cutover        | Executive Product Lead  | Final Go/No-Go release approval    |
+──────────────+────────────────────────────────────────+─────────────────────────+────────────────────────────────────+
```
