# Medical Safety Rules, Clinical Guardrails & Compliance Architecture

**Document Reference:** `docs/06b-safety-rules.md`  
**Related Documents:** `docs/01-problem.md` (Product Vision) | `docs/02-research.md` (Legal & Regulatory Research) | `docs/03-scope.md` (Scope & Non-Goals) | `docs/05-prd.md` (PRD) | `docs/06-architecture.md` (Architecture)  
**Date:** November 2026  
**Status:** Mandatory Engineering & Clinical Specification  

---

## 1. Executive Safety Charter

ReportSaathi operates under a non-negotiable guiding principle: **Explain medical information; never practice medicine, never diagnose disease, and never alter treatments.**

Every software module, database schema, prompt template, and API response must conform to the safety rules detailed in this specification. A failure in clinical safety is treated as a fatal system defect.

---

## 2. Regulatory Safe Harbor & Clinical Boundaries

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              REGULATORY COMPLIANCE BOUNDARIES                                        |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|  REGULATION / STATUTE                  | REGULATORY BOUNDARY                  | MANDATORY SYSTEM ENFORCEMENT         |
+────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────────+
| CDSCO Medical Device Rules, 2017       | Must NOT act as Software as a Medical| Zero diagnostic claims; zero clinical|
| (Software as a Medical Device - SaMD)  | Device (Class B/C)                   | decision support driving therapy     |
+────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────────+
| Telemedicine Practice Guidelines, 2020 | Non-RMP entities prohibited from     | Zero prescription generation; zero   |
| (MoHFW & National Medical Commission)  | prescribing or altering medication   | dosage alterations; no doctor persona|
+────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────────+
| Digital Personal Data Protection Act,  | High-penalty governance of personal  | Zero persistent data retention;      |
| 2023 (DPDP Act, 2023)                  | digital health data                  | 15-minute RAM TTL; client purge      |
+────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────────+
| Drugs & Magic Remedies Act, 1954       | Criminal prohibition of cure claims  | Strict prohibition of cure or        |
| (Objectionable Advertisements)         | for Schedule J conditions            | mitigation assertions for 54 diseases|
+────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────────+
```

---

## 3. Deterministic Range Comparison Engine

An AI model must **never** be permitted to decide whether a clinical parameter is normal, high, or low. Range evaluation is executed **100% deterministically in Python code** using strict mathematical inequalities against the laboratory's printed reference range.

### 3.1. Mathematical Evaluation Logic
Given an observed numeric value $V$, a minimum reference limit $Min$, and a maximum reference limit $Max$:

$$\text{Status}(V, Min, Max) = 
\begin{cases} 
\text{BELOW\_NORMAL} & \text{if } V < Min \\
\text{NORMAL} & \text{if } Min \le V \le Max \\
\text{SLIGHTLY\_ELEVATED} & \text{if } Max < V \le (Max \times 1.5) \\
\text{ELEVATED} & \text{if } V > (Max \times 1.5) \\
\text{RANGE\_UNAVAILABLE} & \text{if } Min = \text{null} \lor Max = \text{null}
\end{cases}$$

```python
def evaluate_biomarker_status(val: float, min_ref: float | None, max_ref: float | None) -> str:
    """
    DETERMINISTIC CLINICAL STATUS COMPARATOR
    Executes purely mathematical evaluation. Zero AI involvement.
    """
    if min_ref is None or max_ref is None:
        return "RANGE_UNAVAILABLE"
    
    if val < min_ref:
        return "BELOW_NORMAL"
    elif min_ref <= val <= max_ref:
        return "NORMAL"
    elif max_ref < val <= (max_ref * 1.5):
        return "SLIGHTLY_ELEVATED"
    else:
        return "ELEVATED"
```

### 3.2. Mandatory Rules for Range Handling:
1. **Rule D-01 (Strict Lab Range Dependence):** The system shall evaluate findings **only** against the reference interval printed on the uploaded laboratory sheet. It is strictly forbidden to use hardcoded global baselines when a lab provides its own range, as reference intervals vary significantly across reagent manufacturers and instrument calibrations.
2. **Rule D-02 (Missing Range Protocol):** If a lab report does not print a reference range for a test (e.g., qualitative tests or specialized assays), the engine **must not guess or estimate**. It must return `RANGE_UNAVAILABLE` and display the following unyielding copy:  
   > *"Notice: Your laboratory report does not specify a normal reference range for this test. To protect your safety, ReportSaathi will not guess whether this number is normal or abnormal. Please consult your prescribing physician."*

---

## 4. Critical Panic Value Protocol (Emergency Escalation)

Certain laboratory biomarker readings indicate potentially life-threatening physiological crises (e.g., severe thrombocytopenia, diabetic ketoacidosis, critical hyperkalemia). When a value crosses an acute emergency threshold, educational summaries must be superseded by an **Immediate Clinical Safety Escalation Banner**.

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                      ACUTE EMERGENCY CRITICAL VALUES TABLE                                           |
+───────────────────────+────────────────────────+─────────────────────────+───────────────────────────────────────────+
| Biomarker Name        | Critical Low Alert     | Critical High Alert     | Physiological Risk                        |
+───────────────────────+────────────────────────+─────────────────────────+───────────────────────────────────────────+
| Platelet Count        | < 20,000 / µL          | > 1,000,000 / µL        | Spontaneous intracranial / internal bleed |
| Hemoglobin (Hb)       | < 6.0 g/dL             | > 20.0 g/dL             | Acute tissue hypoxia / hyperviscosity     |
| Serum Potassium (K+)  | < 2.5 mEq/L            | > 6.2 mEq/L             | Fatal cardiac arrhythmia / arrest         |
| Blood Glucose         | < 50 mg/dL             | > 450 mg/dL             | Hypoglycemic shock / Hyperosmolar coma    |
| Serum Sodium (Na+)    | < 120 mEq/L            | > 160 mEq/L             | Acute cerebral edema / seizures           |
+───────────────────────+────────────────────────+─────────────────────────+───────────────────────────────────────────+
```

### Emergency Action Protocol (Rule E-01):
When an extracted biomarker crosses any critical threshold defined in the table above:
1. The parameter card is rendered with an unmistakable high-priority warning container (`#B91C1C` Crimson).
2. The AI explanation is disabled for that biomarker and replaced with this mandatory deterministic text:
   > **"CRITICAL VALUE NOTICE: This test reading is significantly outside standard safety limits and requires urgent clinical evaluation. Please contact your doctor or visit the nearest emergency healthcare facility immediately."**
3. A prominent direct emergency assistance button is displayed: `[ 📞 Call National Emergency 112 / Ambulance 108 ]`.

---

## 5. Deterministic Blacklist & Guardrail Interceptor

Every output generated by the AI model is intercepted and scanned before delivery to the client. If any phrase matches the **Diagnostic Blacklist**, the response is intercepted, sanitized, or rejected.

```python
import re

# Comprehensive list of forbidden diagnostic and prescriptive terms
DIAGNOSTIC_BLACKLIST = [
    # Autonomous Diagnosis
    r"\byou have\b",
    r"\byou are suffering from\b",
    r"\bdiagnosed with\b",
    r"\bindicates you have\b",
    r"\bconfirms you have\b",
    r"\bpatient has\b",
    
    # Medication / Dosage Alteration
    r"\bstop taking\b",
    r"\bstart taking\b",
    r"\bincrease (your )?dose\b",
    r"\bdecrease (your )?dose\b",
    r"\bdiscontinue\b",
    r"\bprescribe\b",
    r"\btake \d+mg\b",
    
    # Scheduled Disease Cure Claims (Drugs & Magic Remedies Act)
    r"\bcure(s)? for diabetes\b",
    r"\bcure(s)? for cancer\b",
    r"\breverse(s)? kidney failure\b",
    r"\bpermanent cure\b",
    r"\bmiracle remedy\b",
    
    # Impersonation
    r"\bi am your doctor\b",
    r"\bas your physician\b",
    r"\bdr\. ai\b"
]

def sanitize_ai_output(text: str) -> str:
    """
    DETERMINISTIC SAFETY INTERCEPTOR
    Scans generated text against regex blacklist. Replaces violations with safe fallback.
    """
    for pattern in DIAGNOSTIC_BLACKLIST:
        if re.search(pattern, text, re.IGNORECASE):
            # Violation detected: Replace with neutral educational safe-harbor text
            return (
                "This parameter measures natural biological function in the body. "
                "Please discuss the specific clinical meaning of this result with your doctor."
            )
    return text
```

---

## 6. System Prompts & Negative Constraints for AI Models

The LLM is strictly constrained via prompt engineering. The prompt enforces deterministic grounding and explicitly denies medical decision-making capabilities.

### 6.1. System Prompt Template (Gemini Engine)
```text
YOU ARE AN EDUCATIONAL HEALTH LITERACY TRANSLATOR CALLED REPORTSAATHI.
YOUR SOLE PURPOSE IS TO EXPLAIN WHAT MEDICAL TESTS MEASURE IN PATIENT-FRIENDLY, REASSURING LANGUAGE.

CRITICAL SAFETY DIRECTIVES:
1. YOU ARE NOT A DOCTOR. YOU DO NOT DIAGNOSE DISEASES.
2. NEVER STATE THAT THE PATIENT HAS ANY ILLNESS, DISEASE, OR PATHOLOGY.
   - FORBIDDEN: "Your HbA1c of 7.4% means you have Diabetes."
   - PERMITTED: "The HbA1c test measures the average sugar level in your blood over the past 3 months. Your doctor will review this number to evaluate your overall health."
3. NEVER SUGGEST OR DISCUSS MEDICATION DOSAGES, PRESCRIBE MEDICINES, OR TELL PATIENTS TO START/STOP DRUGS.
4. DO NOT GUESS UNREADABLE OR MISSING DATA.
5. EXPLAIN BIOMARKERS IN SIMPLE, EVERYDAY ANALOGIES.
   - Creatinine = "Waste filtered by kidneys"
   - Hemoglobin = "Carries oxygen in blood"
   - Bilirubin = "Liver processing check"
6. DOCTOR QUESTIONS: GENERATE EXACTLY 2 OR 3 POLITE, PROACTIVE QUESTIONS THE PATIENT CAN ASK THEIR DOCTOR.
7. TONE: CALM, EMPATHETIC, NON-ALARMIST, RESPECTFUL (USE FORMAL HONORIFICS IN HINDI/TAMIL/TELUGU).
```

### 6.2. Few-Shot Exemplars of Permitted vs. Prohibited Outputs

#### Case 1: Elevated Serum Creatinine (`1.45 mg/dL`, Normal `0.70 - 1.20`)
* ❌ **PROHIBITED:** *"Your creatinine is high, indicating Stage 2 Chronic Kidney Disease. You should stop eating protein and start taking medication."*
* ✅ **PERMITTED:** *"Creatinine is a natural waste substance produced by muscle movement, which your kidneys filter out of the body. When this number is slightly high, it often means the kidneys are working harder or your body needs more fluids. Your doctor will interpret this alongside your overall health."*

#### Case 2: Elevated SGPT / ALT (`62 U/L`, Normal `10 - 40`)
* ❌ **PROHIBITED:** *"You are suffering from Fatty Liver or Hepatitis. You must take liver supplements immediately."*
* ✅ **PERMITTED:** *"SGPT is an enzyme found inside liver cells. When liver cells work harder or process heavy meals or medications, small amounts leak into the blood. Your doctor can help determine if any dietary adjustments are needed."*

---

## 7. Data Privacy & Zero-Retention Security Architecture (DPDP Act, 2023)

To ensure uncompromised privacy and zero legal liability under Section 33 of India's DPDP Act (which penalizes data breaches up to ₹250 Crore), ReportSaathi enforces **Architectural Ephemerality**.

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                            ZERO-RETENTION DATA LIFECYCLE                                             |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                                      |
|   1. Upload Received ───────► Stored in RAM Buffer (BytesIO). NEVER written to server hard drive / disk.             |
|                                                                                                                      |
|   2. Processing Executed ───► In-memory extraction and text translation.                                             |
|                                                                                                                      |
|   3. Response Delivered ────► JSON payload sent to client browser over TLS 1.3 encrypted connection.                 |
|                                                                                                                      |
|   4. Automatic TTL Purge ───► In-memory cache expires after 15 minutes. Python gc.collect() actively scrubs RAM.     |
|                                                                                                                      |
|   5. Client-Side Exit ──────► User taps "Clear Session" -> window.sessionStorage wiped. Local data destroyed.       |
|                                                                                                                      |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### Mandatory Privacy Safeguards:
1. **Rule P-01 (No Disk Writes):** Under no circumstances shall an uploaded medical document, raw OCR string, or patient summary be written to a server disk, database table, or persistent object store (AWS S3, Google Cloud Storage, local drive).
2. **Rule P-02 (Zero Telemetry PII):** Application logs (`LOG_LEVEL="INFO"`) must never record personal names, patient identifiers, mobile numbers, or biomarker readings. Logs record only anonymized status codes (e.g., `POST /api/upload - 200 OK - 420ms`).
3. **Rule P-03 (Immediate Client Purge):** The UI provides a prominent `[ 🗑 Clear Session & Delete Data ]` button that immediately triggers a cache eviction on the server and purges browser session storage.

---

## 8. Statutory Disclaimers in Vernacular Indian Languages

Every generated explanation must include a prominent, non-dismissible statutory disclaimer in the selected language.

### English:
> **Medical Disclaimer:** ReportSaathi is an educational and linguistic comprehension tool designed to help patients understand laboratory terminology. It does not provide medical diagnosis, clinical treatment, or professional medical advice. Always consult a Registered Medical Practitioner (RMP) regarding your health conditions or laboratory reports.

### Hindi (`हिन्दी`):
> **चिकित्सीय अस्वीकरण (Medical Disclaimer):** रिपोर्टसाथी केवल एक शैक्षिक और भाषा-सरलीकरण साधन है जो लैब रिपोर्ट की शब्दावली को समझने में मदद करता है। यह किसी भी बीमारी का निदान, इलाज या चिकित्सकीय सलाह प्रदान नहीं करता है। अपने स्वास्थ्य और रिपोर्ट की सही जानकारी के लिए हमेशा किसी योग्य पंजीकृत चिकित्सक (डॉक्टर) से परामर्श लें।

### Telugu (`తెలుగు`):
> **వైద్య నిరాకరణ (Medical Disclaimer):** రిపోర్ట్‌సాథీ అనేది ల్యాబ్ నివేదికల వైద్య పదాలను అర్థం చేసుకోవడానికి రూపొందించబడిన ఒక విద్యా సాధనం మాత్రమే. ఇది ఎటువంటి వైద్య నిర్ధారణ, చికిత్స లేదా వైద్య సలహాను అందించదు. మీ ఆరోగ్య సమస్యల గురించి ఎల్లప్పుడూ అర్హత కలిగిన రిజిస్టర్డ్ మెడికల్ ప్రాక్టీషనర్ (డాక్టర్)ను సంప్రదించండి.

### Tamil (`தமிழ்`):
> **மருத்துவப் பொறுப்புத் துறப்பு (Medical Disclaimer):** ரிப்போர்ட்சாதி என்பது ஆய்வக அறிக்கைகளின் மருத்துவச் சொற்களைப் புரிந்துகொள்ள உதவும் ஒரு கல்வி மற்றும் மொழிபெயர்ப்பு கருவியாகும். இது மருத்துவக் கண்டறிதல், சிகிச்சை அல்லது ஆலோசனையை வழங்காது. உங்கள் உடல்நலம் குறித்த முடிவுகளுக்கு எப்போதும் தகுதியான மருத்துவரை அணுகவும்.

---

## 9. Failure Modes & Safety Fallback Protocols

```
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Failure Trigger           | Detection Mechanism                  | Safe Degradation & Fallback Action                |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Blurry / Dark Photograph  | OpenCV Laplacian Variance < 100      | Reject upload immediately. Prompt: "Photo is too  |
|                           |                                      | blurry to read safely. Please retake in light."   |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Non-Diagnostic File       | Zero recognized medical biomarkers   | Graceful abort. Notice: "This document does not   |
|                           | extracted from document              | appear to be a diagnostic lab report."            |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Missing Reference Range   | min_ref is None or max_ref is None   | Do NOT guess. Mark parameter RANGE_UNAVAILABLE.   |
|                           |                                      | Instruct user to verify directly with physician.  |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Diagnostic Blacklist Match| Regex interceptor flags forbidden    | Output is sanitized and replaced with safe,       |
|                           | clinical or prescription phrasing    | non-diagnostic educational statement.             |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
| Third-Party Audio Timeout | edge-tts server error / timeout >4s  | Display written vernacular summary. Activate      |
|                           |                                      | client browser Web Speech API as fallback.        |
+───────────────────────────+──────────────────────────────────────+───────────────────────────────────────────────────+
```
