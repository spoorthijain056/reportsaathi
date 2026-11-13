# API Contract & Endpoint Specification: ReportSaathi MVP

**Document Reference:** `docs/06a-api-contract.md`  
**Related Documents:** `docs/05-prd.md` (PRD) | `docs/06-architecture.md` (Architecture) | `docs/06b-safety-rules.md` (Safety Rules)  
**Date:** November 2026  
**Status:** Approved OpenAPI 3.1 Specification  
**Protocol:** REST over HTTPS (TLS 1.3)  
**Base URL:** `https://reportsaathi.onrender.com` (or `http://localhost:8000` for local testing)  

---

## 1. Global Architectural & Security Policies

1. **Zero-Retention Guarantee:** Every response containing health document data is served with `Cache-Control: no-store, no-cache, must-revalidate, private` to prevent intermediary caching or proxy persistence.
2. **Standard Error Envelope:** All error responses follow the RFC 7807 Problem Details specification:
   ```json
   {
     "type": "https://reportsaathi.org/errors/INVALID_FILE_FORMAT",
     "title": "Invalid File Format",
     "status": 415,
     "detail": "Only PDF, JPG, and PNG files are supported.",
     "instance": "/api/upload",
     "error_code": "ERR_UNSUPPORTED_MEDIA"
   }
   ```
3. **Rate Limiting Headers:** Responses from mutation endpoints include standard headers:
   * `X-RateLimit-Limit`: Maximum requests permitted per window (e.g., 5).
   * `X-RateLimit-Remaining`: Remaining requests in current window.
   * `X-RateLimit-Reset`: Epoch timestamp when window resets.

---

## 2. Endpoint Specifications

### 2.1. `POST /api/upload`
Uploads a diagnostic laboratory document (PDF or camera photo), executes pre-flight validation (MIME-type verification, byte limit check, OpenCV blur detection), and registers a transient session in memory.

* **Request Format:** `multipart/form-data`
* **Request Headers:**
  * `Content-Type: multipart/form-data`
  * `Accept: application/json`
* **Form Fields:**
  * `file` (Binary, Required): PDF or image file (max 10MB).
  * `language` (String, Optional): Preferred language code (`hi`, `te`, `ta`, `en`). Defaults to `hi`.
* **Success Response (200 OK):**
  ```json
  {
    "status": "success",
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "file_name": "blood_report_kamla_devi.pdf",
    "file_type": "application/pdf",
    "file_size_bytes": 1048576,
    "pages_detected": 1,
    "language": "hi",
    "expires_in_seconds": 900
  }
  ```
* **Error Responses:**
  * `400 Bad Request` (Image Too Blurry):
    ```json
    {
      "status": 400,
      "title": "Image Blurry or Low Quality",
      "detail": "Laplacian blur variance is below threshold (54 < 100). Please retake the photo in bright light.",
      "error_code": "ERR_IMAGE_BLURRY"
    }
    ```
  * `413 Payload Too Large`:
    ```json
    {
      "status": 413,
      "title": "File Too Large",
      "detail": "Uploaded file exceeds maximum limit of 10 MB.",
      "error_code": "ERR_FILE_TOO_LARGE"
    }
    ```
  * `415 Unsupported Media Type`:
    ```json
    {
      "status": 415,
      "title": "Unsupported File Type",
      "detail": "Received text/plain. Only application/pdf, image/jpeg, image/png are permitted.",
      "error_code": "ERR_UNSUPPORTED_MEDIA"
    }
    ```
  * `429 Too Many Requests`:
    ```json
    {
      "status": 429,
      "title": "Rate Limit Exceeded",
      "detail": "Limit of 5 uploads per 10 minutes exceeded. Please wait 7 minutes.",
      "error_code": "ERR_RATE_LIMIT"
    }
    ```

---

### 2.2. `POST /api/process`
Orchestrates deterministic table cell extraction, range comparison, layman translation, and doctor questions generation for an active transient session.

* **Request Format:** `application/json`
* **Request Headers:**
  * `Content-Type: application/json`
  * `Accept: application/json`
* **Request Body Schema:**
  ```json
  {
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "language": "hi"
  }
  ```
* **Success Response (200 OK):**
  ```json
  {
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "language": "hi",
    "overall_summary": "आपकी रिपोर्ट में अधिकांश जाँच सामान्य हैं, और रक्त शर्करा (HbA1c) सामान्य सीमा से थोड़ा अधिक है।",
    "critical_flag_triggered": false,
    "biomarkers": [
      {
        "test_name": "HbA1c (Glycosylated Hemoglobin)",
        "layman_name": "3 महीने का औसत रक्त शर्करा स्तर",
        "observed_value": 7.4,
        "unit": "%",
        "min_reference": 4.0,
        "max_reference": 5.6,
        "status": "SLIGHTLY_ELEVATED",
        "plain_explanation": "यह जाँच पिछले 3 महीनों के दौरान आपके रक्त में औसत चीनी के स्तर को मापती है। यह सामान्य से थोड़ा अधिक है।",
        "visual_gauge": {
          "status_color": "#D97706",
          "status_label": "SLIGHTLY_ELEVATED",
          "scale_min": 3.0,
          "scale_max": 10.0
        }
      },
      {
        "test_name": "Serum Creatinine",
        "layman_name": "किडनी अपशिष्ट निष्कासन जाँच",
        "observed_value": 0.9,
        "unit": "mg/dL",
        "min_reference": 0.7,
        "max_reference": 1.2,
        "status": "NORMAL",
        "plain_explanation": "यह जाँच दर्शाती है कि आपकी किडनी शरीर से अपशिष्ट पदार्थों को कितनी अच्छी तरह फ़िल्टर कर रही है। यह परिणाम सामान्य है।",
        "visual_gauge": {
          "status_color": "#16A34A",
          "status_label": "NORMAL",
          "scale_min": 0.3,
          "scale_max": 2.0
        }
      }
    ],
    "doctor_questions": [
      {
        "question_text": "डॉक्टर साहब, मेरा HbA1c 7.4% आया है। क्या मुझे अपने खान-पान या दवा में कोई बदलाव करने की आवश्यकता है?",
        "rationale": "Clarifies medication or dietary adjustments for blood sugar"
      },
      {
        "question_text": "मुझे यह रक्त शर्करा जाँच दोबारा कितने समय बाद करानी चाहिए?",
        "rationale": "Establishes monitoring cadence"
      }
    ],
    "audio_available": true,
    "audio_stream_url": "/api/audio/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "disclaimer": "चिकित्सीय अस्वीकरण: रिपोर्टसाथी केवल एक शैक्षिक साधन है। यह किसी भी बीमारी का निदान या इलाज नहीं करता है। हमेशा पंजीकृत चिकित्सक (डॉक्टर) से परामर्श लें।"
  }
  ```
* **Error Responses:**
  * `404 Not Found` (Session Expired or Missing):
    ```json
    {
      "status": 404,
      "title": "Session Not Found or Expired",
      "detail": "The requested session has expired or was purged from memory.",
      "error_code": "ERR_SESSION_EXPIRED"
    }
    ```
  * `422 Unprocessable Entity` (Non-Lab Document):
    ```json
    {
      "status": 422,
      "title": "Non-Diagnostic Document",
      "detail": "Could not identify standard diagnostic biomarkers or reference ranges in this document.",
      "error_code": "ERR_NON_LAB_DOCUMENT"
    }
    ```

---

### 2.3. `GET /api/audio/{session_id}`
Streams a synthesized vernacular audio narration (MP3/Opus) corresponding to the session's overall summary and key biomarker findings.

* **Request Format:** HTTP GET
* **Path Parameters:**
  * `session_id` (String, Required): UUIDv4 of active session.
* **Success Response (200 OK):**
  * `Content-Type: audio/mpeg`
  * `Content-Disposition: inline; filename="summary_hi.mp3"`
  * `Cache-Control: no-store`
  * Body: Binary audio byte stream.
* **Error Responses:**
  * `404 Not Found`: Session expired or audio synthesis failed.

---

### 2.4. `POST /api/session/purge`
Client-triggered endpoint that immediately destroys all in-memory buffers associated with a session (supporting the DPDP Act Right to Erasure).

* **Request Format:** `application/json`
* **Request Body:**
  ```json
  {
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
  ```
* **Success Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "Session memory successfully purged and scrubbed.",
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
  ```

---

### 2.5. `GET /healthz`
Health probe for reverse proxy and container monitoring.

* **Success Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "timestamp": 1731498600,
    "version": "1.0.0-mvp",
    "memory_active_sessions": 3
  }
  ```
