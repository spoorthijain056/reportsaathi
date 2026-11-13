# Technical Architecture & System Design: ReportSaathi MVP

**Document Reference:** `docs/06-architecture.md`  
**Related Documents:** `docs/01-problem.md` (Product Vision) | `docs/02-research.md` (Market & Legal Research) | `docs/03-scope.md` (Scope & Boundaries) | `docs/04-design.md` (Screen States & UI Direction) | `docs/05-prd.md` (Product Requirements)  
**Date:** November 2026  
**Status:** Approved Technical Architecture  
**Constraint:** 100% Free and Open-Source Software (FOSS) & Free Tier Viable  

---

## 1. Architecture Philosophy: The Simplest Suitable Architecture

ReportSaathi’s architecture is guided by three non-negotiable architectural axioms:
1. **Stateless Ephemerality (Zero-Persistence):** To completely eliminate data breach liability under India's Digital Personal Data Protection Act, 2023 (DPDP Act) and avoid database management overhead, the backend operates **without a persistent database**. All files, extracted text, and AI responses live in transient server memory (RAM) with strict Time-To-Live (TTL) eviction.
2. **Deterministic-First Clinical Guardrails:** Diagnostic numerical comparison, biomarker range checking, and legal disclaimers are executed **100% deterministically in code**. AI/LLMs are strictly restricted to linguistic summarization, layman translation, and conversational question phrasing.
3. **Budget Client Optimization:** The client-side footprint is engineered for low-cost Android hardware (e.g., 360dp screens, 1GB RAM, 3G/4G connectivity) with a tiny JavaScript bundle (<30 KB), CSS-driven animations, and zero heavy client-side frameworks.

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              SYSTEM ARCHITECTURE PIPELINE                                            |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                                      |
|   [ Client: Budget Android Browser (360dp) ]                                                                         |
|         │                                                                                                            |
|         ▼  HTTPS / TLS 1.3 (Cloudflare Free Edge SSL)                                                                |
|   [ Reverse Proxy & Rate Limiter ] ───► slowapi (5 req/10 min per IP)                                                |
|         │                                                                                                            |
|         ▼                                                                                                            |
|   [ FastAPI Application Server (Python 3.11) ]                                                                       |
|         │                                                                                                            |
|         ├──► 1. Pre-Flight Validator ────────► (OpenCV Laplacian blur check, file format)  [DETERMINISTIC]          |
|         │                                                                                                            |
|         ├──► 2. In-Memory Extraction Engine                                                                          |
|         │      ├── Digital PDF Layer ────────► pdfplumber / PyMuPDF                        [DETERMINISTIC]          |
|         │      └── Scanned Photo Fallback ───► Tesseract OCR (Pytesseract)                 [DETERMINISTIC]          |
|         │                                                                                                            |
|         ├──► 3. Clinical Range Comparator ───► Python Mathematical Evaluator               [DETERMINISTIC]          |
|         │      (Classifies Normal / Low / High strictly based on printed lab ranges)                                 |
|         │                                                                                                            |
|         ├──► 4. Layman & Vernacular Engine ──► Google Gemini Free API Tier (Flash)         [AI / LLM MODEL]         |
|         │      (Strict temperature: 0.0, grounded prompt, zero diagnostic assertion)                                |
|         │                                                                                                            |
|         ├──► 5. Safety Blacklist Interceptor ► Regex Term Filter                           [DETERMINISTIC]          |
|         │                                                                                                            |
|         ├──► 6. Native Audio Synthesizer ────► edge-tts (Free Indic Voice Models)           [OPEN SERVICE]           |
|         │                                                                                                            |
|         ▼                                                                                                            |
|   [ JSON Response Delivered to Client ]                                                                              |
|         │                                                                                                            |
|         ▼                                                                                                            |
|   [ Automatic In-Memory Garbage Collection / TTL Purge ] ──► (Zero bytes stored to disk)    [DPDP COMPLIANT]         |
|                                                                                                                      |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Stack Evaluation & Recommendation

We evaluate two free/open-source full-stack architectures suitable for building ReportSaathi:

```
+───────────────────────────────────+───────────────────────────────────+──────────────────────────────────────────────+
| Dimension                         | Option A: Python FastAPI +        | Option B: Full-Stack Node.js /               |
|                                   | Lightweight HTML/Tailwind/Vanilla | Next.js (TypeScript)                         |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────────────────────────+
| Backend Framework                 | FastAPI (Python 3.11+)            | Next.js App Router / Node.js                 |
| PDF & Document Extraction         | pdfplumber + PyMuPDF (Superior)   | pdf-parse (Rudimentary text stream)          |
| OCR Engine                        | Tesseract + OpenCV (Native C++)   | tesseract.js (WASM / Heavy: >15MB download)  |
| Client Bundle Size                | < 30 KB (Zero framework overhead) | 180 KB – 350 KB (React + Next.js runtime)    |
| Server Memory on Free Hosting     | ~65 MB RAM baseline               | ~220 MB RAM baseline (High OOM crash risk)   |
| Audio Synthesis (TTS)             | edge-tts (Direct Python library)  | External API wrapper or Web Speech API only  |
| Indic Script / Font Rendering     | Native server Jinja2 or clean DOM | React Hydration overhead on budget devices   |
| Developer Velocity for AI / NLP   | Native home of AI/ML tooling      | Requires wrappers for Python AI ecosystems   |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────────────────────────+
```

### Detailed Analysis of Options:

#### Option A: Python FastAPI + Lightweight HTML5/Tailwind/Vanilla JS (RECOMMENDED)
* **Strengths:**
  1. **Medical Document Parsing Superiority:** Python is the undisputed leader in PDF text-layer extraction and table analysis. Libraries like `pdfplumber` and `PyMuPDF` extract table cells, bounding boxes, and multi-column lab structures deterministically with >99% precision. In contrast, Node's `pdf-parse` flattens text into a disordered string, breaking multi-column biomarker-to-range associations.
  2. **Minimal Server Memory Footprint:** FastAPI runs efficiently on Uvicorn, consuming only 60–75MB of RAM at idle. This fits comfortably within the strict 512MB RAM limits of free hosting platforms (Render, Railway, Hugging Face Spaces) without triggering Out-Of-Memory (OOM) fatal kills.
  3. **Ultra-Lightweight Client Execution:** By serving clean, semantic HTML styled with Tailwind CSS and powered by minimal Vanilla JavaScript (<30KB gzipped), low-cost Android phones with 1GB RAM load the app in under 1 second without React virtual DOM hydration lag.
  4. **Integrated Free Audio Synthesis:** The open-source `edge-tts` Python library provides high-fidelity, natural-sounding Indic voices (Hindi, Tamil, Telugu) with zero API keys and zero cost.

#### Option B: Full-Stack Next.js (Node.js / React)
* **Weaknesses:**
  1. **Poor Tabular OCR & PDF Extraction:** Running OCR in Node via `tesseract.js` requires downloading a massive WebAssembly binary (>15MB), which crashes browser tabs on cheap 1GB RAM Android phones. Running OCR on the Node server requires spawning heavy child processes that quickly exceed 512MB server RAM.
  2. **Heavy Client Bundle:** React + Next.js client-side JavaScript runtimes easily exceed 200KB–300KB, degrading Time-To-Interactive (TTI) on spotty Indian 3G/4G networks.
  3. **Table Alignment Breakdown:** Node's open-source PDF parsers struggle to distinguish between a test's observed value and its reference interval when columns are closely spaced.

### Final Stack Recommendation:
**Adopt Option A (Python FastAPI + HTML5/Tailwind/Vanilla JS).** It provides the highest document extraction accuracy, the lowest memory footprint on free hosting, and the fastest load times for low-end mobile browsers.

---

## 3. Deterministic Code vs. AI Model Partition

To guarantee medical safety, eliminate hallucinations, and remain legally compliant with CDSCO regulations, the system enforces a strict boundary between deterministic algorithms and AI models:

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  DETERMINISTIC CODE vs. AI MODEL PARTITION TABLE                                     |
+───────────────────────────────────+────────────────────+─────────────────────────────────────────────────────────────+
| System Task / Operation           | Execution Engine   | Mechanism & Safety Rationale                                |
+───────────────────────────────────+────────────────────+─────────────────────────────────────────────────────────────+
| 1. File Format & Size Validation  | Deterministic Code | Python MIME-type verification & byte size limit check (<10MB)|
| 2. Image Blur & Quality Check     | Deterministic Code | OpenCV Laplacian variance thresholding (>100 = Sharp)       |
| 3. Digital PDF Text Extraction    | Deterministic Code | pdfplumber coordinate-based table cell parsing              |
| 4. Biomarker Entity Extraction    | Deterministic Code | Regex pattern matching for values, units, and intervals     |
| 5. Range Comparison (Low/Normal/Hi| Deterministic Code | Mathematical inequality: (Min <= Value <= Max) -> Zero AI!  |
| 6. Status Badge Color Assignment  | Deterministic Code | Static rule table (Green, Warm Amber, Blue, Coral)          |
| 7. Missing Range Fallback Notice  | Deterministic Code | If range is Null -> Static unyielding safety warning        |
| 8. Layman Medical Translation     | AI Model (Gemini)  | LLM converts clinical terms to plain biological meaning     |
| 9. Vernacular Localization        | AI Model (Gemini)  | LLM translates summary into Hindi/Tamil/Telugu              |
| 10. Doctor Questions Generation   | AI Model (Gemini)  | LLM synthesizes 2-3 consultation questions from findings    |
| 11. Diagnostic Blacklist Filter   | Deterministic Code | Regex scanner blocking 50+ forbidden diagnostic phrases     |
| 12. Audio Synthesis (TTS)         | Deterministic Code | edge-tts streams deterministic text to Indic voice models    |
| 13. Data Purge & Memory Scrubbing | Deterministic Code | Python TTLCache expiry & gc.collect() zero-retention         |
+───────────────────────────────────+────────────────────+─────────────────────────────────────────────────────────────+
```

### Why Deterministic Range Comparison is Mandatory:
An LLM must **never** be asked: *"Is this blood sugar value of 7.4 high?"*  
Large language models are probabilistic and prone to contextual drift. Instead, the Python backend mathematically calculates:
$$\text{If } 7.4 > 5.6 \implies \text{Status} = \text{SLIGHTLY\_ELEVATED}$$
The LLM is only supplied the pre-computed status and instructed: *"Explain what the HbA1c test measures in simple words without diagnosing diabetes."*

---

## 4. In-Memory Data Models (Pydantic Schemas)

The entire data lifecycle operates within transient Pydantic schemas in Python memory:

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class BiomarkerStatus(str, Enum):
    NORMAL = "NORMAL"
    BELOW_NORMAL = "BELOW_NORMAL"
    SLIGHTLY_ELEVATED = "SLIGHTLY_ELEVATED"
    ELEVATED = "ELEVATED"
    RANGE_UNAVAILABLE = "RANGE_UNAVAILABLE"
    UNCERTAIN = "UNCERTAIN"

class ExtractedBiomarker(BaseModel):
    test_name: str = Field(description="Standardized name of the laboratory test")
    layman_name: str = Field(description="Patient-friendly translation, e.g., Kidney Filter Marker")
    observed_value: float = Field(description="The numeric value reported by the laboratory")
    unit: str = Field(description="Unit of measurement, e.g., mg/dL, %")
    min_reference: Optional[float] = Field(default=None, description="Lower normal threshold")
    max_reference: Optional[float] = Field(default=None, description="Upper normal threshold")
    status: BiomarkerStatus = Field(description="Deterministic range comparison outcome")
    plain_explanation: str = Field(description="1-2 sentence non-diagnostic explanation")

class DoctorQuestion(BaseModel):
    question_text: str = Field(description="Polite, proactive question for the doctor visit")
    rationale: str = Field(description="Brief reason why this question is helpful")

class ProcessedReportCard(BaseModel):
    session_id: str = Field(description="Ephemeral UUIDv4 session identifier")
    language: str = Field(default="hi", description="ISO language code: hi, te, ta, en")
    overall_summary: str = Field(description="Reassuring, non-alarmist overview of report")
    biomarkers: List[ExtractedBiomarker] = Field(default_factory=list)
    doctor_questions: List[DoctorQuestion] = Field(default_factory=list)
    audio_available: bool = Field(default=True)
    disclaimer: str = Field(description="Mandatory statutory medical disclaimer")
    created_at_epoch: float = Field(description="Timestamp for TTL garbage collection")
```

---

## 5. API Endpoints & Routes

```
+────────+─────────────────────────+───────────────────────────────────────────────────────────────────────────────────+
| Method | Route                   | Description & Functionality                                                       |
+────────+─────────────────────────+───────────────────────────────────────────────────────────────────────────────────+
| GET    | /                       | Serves the lightweight, mobile-optimized single-page web UI (Screen 1).          |
| POST   | /api/upload             | Receives file stream, runs pre-flight validation, creates ephemeral session.      |
| POST   | /api/process            | Orchestrates extraction, deterministic comparison, and LLM explanation.           |
| GET    | /api/audio/{session_id} | Streams generated native voice MP3/Opus audio synthesized by edge-tts.            |
| POST   | /api/session/purge      | Client-triggered endpoint that immediately wipes all session data from RAM.       |
| GET    | /healthz                | Simple health check probe for hosting platforms and uptime monitors.              |
+────────+─────────────────────────+───────────────────────────────────────────────────────────────────────────────────+
```

### Route Specifications:

#### 1. `POST /api/upload`
* **Request:** `multipart/form-data` containing `file` (PDF/Image) and `language` (`hi`, `te`, `ta`, `en`).
* **Processing:**
  1. Validates file signature (Magic bytes: `%PDF-`, `\xFF\xD8\xFF`, `\x89PNG`).
  2. If image, executes OpenCV Laplacian blur check ($\text{Variance} > 100$).
  3. Allocates ephemeral `session_id = uuid.uuid4()` in `TTLCache`.
* **Response (JSON):**
  ```json
  {
    "status": "success",
    "session_id": "4a7b9c1d-8e2f-4a3b-9c1d-8e2f4a3b9c1d",
    "pages_detected": 1,
    "file_type": "application/pdf"
  }
  ```

#### 2. `POST /api/process`
* **Request (JSON):** `{"session_id": "4a7b9c1d...", "language": "hi"}`
* **Processing:**
  1. Fetches file buffer from ephemeral memory.
  2. Executes `pdfplumber` / `pytesseract` to extract test lines.
  3. Executes deterministic range logic to assign `BiomarkerStatus`.
  4. Dispatches prompt to Google Gemini API (Free tier) with strict clinical constraints.
  5. Passes output through the Deterministic Blacklist Interceptor.
  6. Dispatches synthesized text to `edge-tts` to prepare audio stream.
* **Response (JSON):** Conforms to `ProcessedReportCard` schema.

#### 3. `GET /api/audio/{session_id}`
* **Response:** `audio/mpeg` binary audio stream generated by `edge-tts` for immediate streaming in the client's audio tag.

#### 4. `POST /api/session/purge`
* **Request (JSON):** `{"session_id": "4a7b9c1d..."}`
* **Processing:** Explicitly deletes the session key from `TTLCache`, invokes `gc.collect()`, and responds with `{"status": "purged"}`.

---

## 6. Authentication & Session Security (Zero-Persistence Model)

* **No User Accounts:** To satisfy the core requirements in `docs/03-scope.md` and remove user registration friction, there are no usernames, passwords, or emails.
* **Ephemeral Signed Sessions:** 
  * When an upload is accepted, the server issues an ephemeral cryptographically signed token: `HMAC-SHA256(session_id, SESSION_SECRET_KEY)`.
  * The token is stored strictly in the client's temporary `window.sessionStorage` (which self-destructs when the mobile browser tab is closed).
* **In-Memory TTL Cache:**
  * Active sessions are stored in an in-memory `cachetools.TTLCache(maxsize=500, ttl=900)` (900 seconds = 15 minutes).
  * After 15 minutes, the cache automatically discards all objects, freeing memory.
* **Abuse & Rate Limiting:**
  * Open-source `slowapi` middleware enforces a rate limit of **5 uploads per 10 minutes per client IP address**, protecting the free LLM API quota and preventing DDoS degradation.

---

## 7. Third-Party Services & Open-Source Tools (100% Free / FOSS)

```
+───────────────────────+───────────────────────────+──────────────────────────────────────────────────────────────────+
| Service Category      | Selected Tool / Service   | Licensing / Cost Tier                                            |
+───────────────────────+───────────────────────────+──────────────────────────────────────────────────────────────────+
| PDF Parsing           | pdfplumber & PyMuPDF      | 100% Open-Source (MIT / AGPL)                                    |
| OCR Engine            | Tesseract OCR             | 100% Open-Source (Apache 2.0)                                    |
| Image Quality Check   | OpenCV-Python (Headless)  | 100% Open-Source (Apache 2.0)                                    |
| Large Language Model  | Google Gemini API (Flash) | Google AI Studio Free Tier (15 RPM, 1,500 RPD, Free of Cost)     |
| Local/Open LLM Option | Qwen2.5-7B-Instruct       | Open-Weights (Apache 2.0) via Hugging Face Inference API / Local |
| Text-to-Speech (TTS)  | edge-tts                  | 100% Open-Source Python wrapper for free Microsoft voice models  |
| Web Framework         | FastAPI & Uvicorn         | 100% Open-Source (BSD / MIT)                                     |
| Styling & UI          | Tailwind CSS (Standalone) | 100% Open-Source (MIT)                                            |
| Rate Limiting         | slowapi                   | 100% Open-Source (MIT)                                            |
+───────────────────────+───────────────────────────+──────────────────────────────────────────────────────────────────+
```

### Notes on Integration:
* **LLM Engine:** Google AI Studio offers a free tier for `gemini-2.5-flash` / `gemini-1.5-flash` that supports multilingual comprehension and structured JSON output mode with generous zero-cost limits.
* **Voice Models (`edge-tts`):**
  * Hindi: `hi-IN-SwaraNeural` (Natural female voice) / `hi-IN-MadhurNeural` (Natural male voice).
  * Tamil: `ta-IN-PallaviNeural`.
  * Telugu: `te-IN-ShrutiNeural`.
  * English: `en-IN-NeerjaNeural` (Indian English accent).
* **Messaging & Maps:** In strict alignment with the MVP scope, **no messaging APIs (WhatsApp/Twilio) and no maps APIs** are integrated for Phase 1.

---

## 8. Free-Tier Hosting & Deployment Architecture

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              FREE DEPLOYMENT TOPOLOGY                                                |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                                      |
|   [ Internet / Mobile Client ]                                                                                       |
|               │                                                                                                      |
|               ▼                                                                                                      |
|   [ Cloudflare DNS & Free CDN ] ────────► Handles SSL termination, DDoS protection, and static asset caching         |
|               │                                                                                                      |
|               ▼                                                                                                      |
|   [ Render.com Free Web Service ] ──────► Linux Container running FastAPI + Uvicorn                                  |
|     (or Hugging Face Spaces Docker)       512MB RAM / 0.5 CPU / Auto-sleep after 15 min inactivity                   |
|                                           Zero persistent disk volumes attached                                      |
|                                                                                                                      |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### Hosting Strategy:
1. **Primary Hosting:** **Render.com Free Web Service** or **Hugging Face Spaces (Docker Free Tier)**:
   * Provides 512MB to 16GB RAM container options with free HTTPS subdomains (`reportsaathi.onrender.com`).
   * Runs a clean Docker container encapsulating Python 3.11, Tesseract binary, and Uvicorn.
2. **Cold Start Mitigation:** Free tier web services spin down after 15 minutes of inactivity. When a client visits the homepage, a lightweight loading indicator gracefully informs the user: *"Starting secure medical engine (takes ~15 seconds on initial load)..."*

---

## 9. Environment Variables Specification

The application requires only seven configuration parameters, manageable via a single `.env` file:

```bash
# ==============================================================================
# REPORTSAATHI MVP CONFIGURATION
# ==============================================================================

# 1. AI Engine Configuration
GEMINI_API_KEY="AIzaSyYourFreeGeminiKeyFromAIStudio"
LLM_MODEL_NAME="gemini-1.5-flash"
LLM_TEMPERATURE=0.0

# 2. Security & Session Secrets
SESSION_SECRET_KEY="generate-random-64-character-hex-string-for-hmac"
SESSION_TTL_SECONDS=900

# 3. Operational Constraints
MAX_UPLOAD_SIZE_MB=10
RATE_LIMIT_RULE="5/10minute"

# 4. Networking & CORS
ALLOWED_ORIGINS="https://reportsaathi.onrender.com,http://localhost:8000"

# 5. Environment & Logging
ENVIRONMENT="production"
LOG_LEVEL="INFO"
```

---

## 10. Open Questions & Technical Unknowns

In accordance with strict technical integrity, the following unverified assumptions and edge cases are documented for empirical validation during early prototype testing:

1. **Edge-TTS Concurrency Limits:** `edge-tts` relies on public endpoints. While it has proven exceptionally reliable for single-user prototyping, it is unknown whether high burst concurrency (e.g., 50 simultaneous synthesis requests) will trigger upstream IP rate-limiting from Microsoft servers.  
   *Fallback Plan:* Integrate client-side browser `Web Speech API` as a zero-latency fallback if the server audio stream fails.
2. **Unaccredited Tier-3 Lab PDF Variances:** While accredited laboratory chains (Dr Lal, Metropolis, Agilus, Apollo) produce well-structured vector PDFs, local neighborhood diagnostic centers often generate non-standardized layouts with uncalibrated coordinates. The exact percentage of printed reports requiring fallback OCR needs field testing.
3. **RAM Ceiling on 512MB Free Containers:** When OpenCV processes a full-resolution 12-megapixel smartphone photo (4000×3000 pixels), uncompressed bitmap arrays can temporarily consume 100MB–150MB of RAM. If two users upload photos simultaneously on a 512MB free container, memory usage could approach the container ceiling.  
   *Mitigation:* Implement client-side canvas downscaling (resize to max 1600px width before upload).
4. **Dialect Nuance in Rural Telugu & Tamil:** While the Gemini model generates excellent formal Hindi, its natural phrasing of specific medical terms in rural Dravidian vernacular dialects (e.g., Telangana regional Telugu vs. Coastal Andhra phrasing) requires human clinical validation by native medical speakers.
