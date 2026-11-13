# ReportSaathi: Core Flow Screen States & Design Direction

**Document Reference:** `docs/04-design.md`  
**Related Documents:** `docs/01-problem.md` (Product Vision) | `docs/02-research.md` (Market Research & Legal Framework) | `docs/03-scope.md` (Core Flow & Scope)  
**Visual Artifacts:** `docs/references/` (Screen State & Reference Comparison Artifacts)  
**Date:** November 2026  
**Status:** Design Specification & UI Architecture  

---

## Executive Overview

This document specifies the interface architecture, screen state definitions, and design direction for **ReportSaathi**. The product is engineered specifically for **older adults** and **caregivers** using **low-cost Android smartphones** (360dp viewport baseline) across **vernacular Indian languages** (Devanagari, Tamil, Telugu, etc.) with non-Latin scripts and long compound words.

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              SCREEN PIPELINE IN CORE FLOW                                            |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                                      |
|   ┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐                |
|   │         SCREEN 1          │      │         SCREEN 2          │      │         SCREEN 3          │                |
|   │     Upload & Language     │ ───► │   In-Memory Processing    │ ───► │    Report Card & Audio    │                |
|   │         Selection         │      │       & Extraction        │      │    Doctor Preparation     │                |
|   └───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘                |
|     • 4 Language Chips                 • In-Memory Progress Check         • Plain-Language Translation               |
|     • Camera / PDF Upload Card         • Reassuring Status Steps          • Visual Range Gauge (Amber/Green)         |
|     • Zero-Login Guest Entry           • DPDP Zero-Retention Notice       • 1-Click Native Audio Player              |
|                                                                           • 2–3 Doctor Discussion Questions          |
|                                                                                                                      |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 1. Comprehensive Screen State Definitions

The MVP core flow consists of **three sequential screens**. Each screen is defined across four mandatory system states: **Default**, **Empty**, **Loading**, and **Error**.

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
| Visual Reference: docs/references/screen-1-upload-states.png                                                         |
| Visual Reference: docs/references/screen-2-processing-states.png                                                     |
| Visual Reference: docs/references/screen-3-report-card-states.png                                                     |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

### 1.1. Screen 1: Document Upload & Language Selection (Ingestion Screen)
*The entry screen where users select their preferred vernacular tongue and supply their diagnostic report.*

#### A. Default State
* **Header / Branding:** Minimalist top bar with "ReportSaathi" logo and regional subtitle: *"Understand Your Health, In Your Language"*.
* **Language Selection Matrix:** High-contrast pill chips prominently displaying native scripts alongside English names:
  * `हिन्दी (Hindi)` [Selected by default based on system locale]
  * `English`
  * `తెలుగు (Telugu)`
  * `தமிழ் (Tamil)`
  * Minimum touch target: 52dp height, 16px bold typography.
* **Document Upload Zone:** A large, high-contrast dashed container (220dp height) featuring two clear, high-affordance buttons:
  * Primary Button (Green `#16A34A`): `[ 📷 Take Photo with Camera ]` (56dp touch height, 18px text).
  * Secondary Button (Slate `#F1F5F9` with `#0D5C75` border): `[ 📄 Choose PDF from Phone ]`.
* **Micro-Copy:** *"Works with printed lab reports from Dr Lal, Metropolis, Agilus, Apollo, and local hospital labs."*
* **Trust & Privacy Banner:** A calming padlock icon with text: *"100% Free • No Sign-up Required • Your document is processed in memory and never stored permanently."*

#### B. Empty State
* **Trigger:** User taps "Upload Report" without selecting or capturing a file, or opens the app fresh.
* **Visual Representation:** Upload container displays an illustrated guide showing a well-lit, flat lab report with a checkmark, contrasting with a crumpled, dark photo with a cross mark.
* **Instructional Text:** *"Please snap a clear photo of your printed blood test or select a PDF report to begin."*
* **Primary Action:** CTA button remains disabled or pulses gently: `[ Select a Medical Document ]`.

#### C. Loading State
* **Trigger:** User selects a 5MB multi-page PDF or snaps a high-resolution camera photograph.
* **Visual Representation:** Upload box transitions into a clean transfer card:
  * Native horizontal progress bar (Teal `#0D5C75`) with animated stripes.
  * Real-time percentage indicator (`"Uploading: 65%..."`).
  * Micro-copy: *"Encrypting and transferring file securely to temporary memory..."*
* **State Safeguard:** Secondary action button: `[ Cancel ]` (48dp height) in soft grey to allow cancellation without app freeze.

#### D. Error State
* **Sub-Case 1: Blurry / Dark Photograph:**
  * Visual: Warning container with warm ochre/amber border (`#D97706`).
  * Copy: *"The photo is too blurry or dark to read the numbers safely. Please retake the photo in good lighting, holding your phone directly above the paper."*
  * CTA: `[ 📷 Retake Photo ]` in full-width primary green.
* **Sub-Case 2: Unsupported File Type / Corrupted PDF:**
  * Visual: Red-tinted card (`#EF4444`).
  * Copy: *"We can only read PDF documents or JPG/PNG photos of diagnostic reports. Word documents and spreadsheets cannot be processed."*
  * CTA: `[ Choose Another File ]`.
* **Sub-Case 3: Network Drop during Upload:**
  * Copy: *"Internet connection interrupted. No data was lost."*
  * CTA: `[ 🔄 Tap to Retry ]`.

---

### 1.2. Screen 2: In-Memory Extraction & Verification (Processing Screen)
*An ephemeral progress screen that maintains user confidence and satisfies statutory transparency requirements under the DPDP Act.*

#### A. Default State (Progressive Extraction)
* **Visual Layout:** Single-column card showing an animated multi-step clinical verification sequence.
* **Checklist Stepper:**
  1. `[✓] Document validated (Digital Pathology Report)` (Green checkmark)
  2. `[✓] Biomarkers detected (HbA1c, Serum Creatinine, SGPT)` (Green checkmark)
  3. `[⏳] Reading laboratory normal ranges...` (Active pulsating spinner)
  4. `[  ] Preparing Hindi explanation and audio...` (Pending grey circle)
* **Estimated Duration:** Clear text counter: *"Usually takes 4 to 8 seconds."*
* **Statutory Privacy Notice:** A permanent, calm footer card: *"Privacy Notice: Processing occurs in transient memory. Document data is scrubbed automatically post-session."*

#### B. Empty State
* **Trigger:** User navigates directly to `/process` URL without an active uploaded payload.
* **Display:** Graceful redirection screen: *"No active document found in session."*
* **Action:** Single prominent button: `[ ⬅ Back to Upload ]`.

#### C. Loading State (Deep Analysis Phase)
* **Visual:** Occurs during the optical character extraction of multi-page complex panels (e.g., Complete Hemogram with 25 parameters).
* **Display:** A circular progress ring with biomarker snippet previews: *"Extracted 12 parameters... Analyzing reference ranges..."*
* **Auditory Cue:** Optional soft tactile haptic vibration when extraction completes to alert elderly users whose attention may have drifted.

#### D. Error State
* **Sub-Case 1: Non-Diagnostic Document (e.g., Selfie, Grocery Bill, Discharge Memo):**
  * Visual: Soft red warning box (`#FEF2F2` background, `#B91C1C` text).
  * Copy: *"This does not look like a diagnostic lab report. ReportSaathi is designed to explain blood tests and diagnostic parameters. We could not find test names or reference intervals."*
  * CTA: `[ Upload a Lab Report ]`.
* **Sub-Case 2: Illegible Cursive / Damaged Page:**
  * Copy: *"The laboratory numbers on this document are unreadable. To protect your medical safety, we cannot guess unclear data."*
  * CTA: `[ Retake Clearer Photo ]`.

---

### 1.3. Screen 3: Report Card, Audio & Doctor Preparation (Value Delivery Screen)
*The primary destination screen that delivers plain-language comprehension, vernacular voice narration, and actionable doctor questions.*

#### A. Default State (The "Report Card")
* **Summary Banner:** Clean overview card showing the patient's test name, date detected, and an overarching reassuring sentiment:
  * *"Lab Report Summary: 1 Parameter Slightly High, 3 Parameters Normal."*
* **Biomarker Explanation Cards (Stacked vertically in single column):**
  * **Card Header:** Test Name in bold (`18px`) + Layman subtitle (`15px`):
    * *Serum Creatinine* → *"Kidney Waste Filtration Marker"*
  * **Visual Range Gauge (Continuous Bar):**
    * A horizontal tri-color track (`12dp` height) showing:
      * Blue (Low) | Green (Normal: 0.70 - 1.20 mg/dL) | Warm Amber (High)
    * A large circular marker indicator positioned at the patient's value (`1.45 mg/dL`).
  * **Status Badge:** A soft pill badge using calming, non-alarmist tones:
    * `[ SLIGHTLY ELEVATED ]` (Warm Ochre `#B45309` on Amber `#FEF3C7`).
    * *Note:* Crimson red is strictly reserved for critical physiological panic values.
  * **Plain-Language Meaning (2 Sentences):**
    * *"Creatinine is a natural waste product made by your muscles. Your kidneys filter it out of your body. When it is slightly high, it often means your body needs more water or your kidneys worked harder recently."*
* **1-Click Vernacular Voice Narration (The Audio Bar):**
  * Positioned immediately below the card for instant access:
  * Large green action container (`#0D5C75` or `#128C7E`, `56dp` height):
    * `[ ▶ सुनो (Listen in Hindi) - 0:45 min ]`
* **Doctor Discussion Questions (Card):**
  * Section title: *"Questions to Ask Your Doctor at Your Next Visit:"*
  * Bulleted list in clear conversational language:
    * *"1. Doctor, my creatinine is slightly above normal at 1.45. Should I increase my daily water intake?"*
    * *"2. Does any medicine I am currently taking affect this test result?"*
    * *"3. When should we re-test this blood marker?"*
* **Statutory Medical Disclaimer (Non-Dismissible Footer):**
  * Soft grey container (`#F1F5F9`, `13px` dark grey text):
  * *"Medical Notice: ReportSaathi is an educational comprehension tool. It does not provide medical diagnosis, treatment plans, or doctor consultations. Always share your original laboratory report with a Registered Medical Practitioner (RMP)."*
* **Session Termination / Privacy Action:**
  * Full-width button: `[ 🗑 Clear Session & Delete My Data ]` (Triggers immediate memory scrub).

#### B. Empty State (No Parameters Recognized)
* **Trigger:** An uploaded lab sheet has all values completely blurred or ripped off.
* **Display:** A neutral informational card: *"We could not extract any specific test parameters from this page."*
* **Action:** `[ Try Scanning Again ]` or `[ Ask a Caregiver to Assist ]`.

#### C. Loading State (Audio Narration Synthesis)
* **Trigger:** User taps "Listen in Hindi/Tamil".
* **Visual:** The Play button pulses gently with a miniature waveform animation:
  * Text updates: *"Generating Hindi voice narration (takes ~2 seconds)..."*
  * Smooth transition directly into audio playback with a visible pause button (`[ ⏸ Pause ]`) and playback scrubber.

#### D. Error State
* **Sub-Case 1: Laboratory Reference Range Missing on Printout:**
  * Visual: Amber informational card with question mark icon (`#D97706`).
  * Copy: *"Sodium: 138 mEq/L. Notice: Your laboratory report did not print a normal reference interval for this parameter. To keep you safe, ReportSaathi will not guess whether this number is high or low. Please verify this value directly with your doctor."*
* **Sub-Case 2: Audio Synthesis / Speaker Failure:**
  * Copy: *"Audio playback could not load. You can read the written Hindi summary above."*
  * CTA: `[ 🔄 Retry Audio ]`.

---

## 2. Review of Reference Products (What to Borrow & What to Avoid)

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
| Visual Reference: docs/references/ref-01-diagnostic-lab-dr-lal.png                                                  |
| Visual Reference: docs/references/ref-02-symptom-checker-ada.png                                                     |
| Visual Reference: docs/references/ref-03-pharmacy-1mg.png                                                            |
| Visual Reference: docs/references/ref-04-whatsapp-audio.png                                                         |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 2.1. Reference 1: Diagnostic Lab Apps (Dr Lal PathLabs, Agilus Diagnostics, Metropolis)
*See artifact:* [ref-01-diagnostic-lab-dr-lal.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-01-diagnostic-lab-dr-lal.png)
* **What to Borrow:**
  * **Structured Reference Intervals:** Diagnostic labs provide unambiguous lower and upper statistical limits for healthy populations. We borrow their exact minimum/maximum numerical boundaries to ground our logic.
  * **Parameter Clustering:** Labs organize tests into logical biological panels (e.g., Kidney Function Test, Lipid Profile, Liver Panel). We borrow this grouping so related markers appear together.
* **What to Avoid:**
  * **Raw Tabular Layouts:** Dense, unstyled 6-column tables that require horizontal panning and pinch-to-zoom on mobile screens.
  * **Alarmist Red Asterisks:** Marking mild, clinically insignificant deviations with aggressive red text (`*H`, `*L`), which induces acute panic.
  * **Monolingual English Lock-In:** Technical jargon without vernacular translation or audio alternatives.

### 2.2. Reference 2: Digital Symptom Checkers (Ada Health, WebMD, Mediktor)
*See artifact:* [ref-02-symptom-checker-ada.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-02-symptom-checker-ada.png)
* **What to Borrow:**
  * **Calm, Reassuring Aesthetic:** Clean whitespace, soft pastel backgrounds, and uncluttered typography that lower stress levels.
  * **Empathetic Micro-Copy:** Conversational language that treats the patient with dignity and care.
  * **Structured Assessment Cards:** Highlighting next steps clearly in modular cards.
* **What to Avoid:**
  * **Worst-Case Scenario Bias:** Over-triaging benign conditions into catastrophic emergencies (e.g., flagging tension headaches as brain aneurysms to protect against legal liability).
  * **Exhaustive Questionnaires:** 25–35 multi-step questions that exhaust elderly users.
  * **Speculative Diagnosis:** Attempting to infer diseases rather than explaining verified lab facts.

### 2.3. Reference 3: Online Pharmacy Platforms (Tata 1mg, PharmEasy)
*See artifact:* [ref-03-pharmacy-1mg.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-03-pharmacy-1mg.png)
* **What to Borrow:**
  * **Visual Dosage & Timing Icons:** Intuitive iconography (Sun = Morning, Moon = Night, Plate/Cutlery = After Food) that bypasses literacy barriers.
  * **Generic Salt Breakdown:** Translating commercial brand names into simple therapeutic purpose tags.
* **What to Avoid:**
  * **Commercial Clutter & Ad Banners:** Flashing discount banners ("20% OFF DIABETES CARE"), sponsored health products, and upsell popups that confuse seniors.
  * **Prescription Rejections without Explanation:** Cancelling orders due to messy handwriting without explaining what is missing.
  * **E-Commerce Funnels:** Cart checkout flows that distract from patient comprehension.

### 2.4. Reference 4: Conversational Messaging & Voice UX (WhatsApp India)
*See artifact:* [ref-04-whatsapp-audio.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-04-whatsapp-audio.png)
* **What to Borrow:**
  * **Ubiquitous Voice Note Interface:** The 1-tap green audio player with scrubber waveform (`#128C7E` / `#25D366`), which 500M+ Indians already know how to use instinctively.
  * **Bottom-Sheet Navigation:** Smooth, thumb-accessible bottom sheets for language selection and detail drill-downs.
  * **Zero Learning Curve:** Familiar, unpretentious interaction patterns requiring zero technical onboarding.
* **What to Avoid:**
  * **Unverified Viral Forwards:** Unregulated community medical advice, miracle cures, and unscientific health rumors.
  * **Privacy Vulnerabilities:** Open group forwarding where sensitive medical tests are exposed to extended relatives.
  * **Chat Clutter:** Vital medical records buried under morning greetings and festival videos.

---

## 3. Design Direction: Layout, Typography, Colour, Spacing & Tone

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              DESIGN SYSTEM AT A GLANCE                                               |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|  VIEWPORT:     360dp baseline width (Budget Android: Samsung M04, Redmi 9A, JioPhone Next)                          |
|  LAYOUT:       Single-column vertical stack, 100% thumb-zone accessibility, no horizontal scroll                     |
|  TYPE:         System Indic fallback (Noto Sans Devanagari/Tamil/Telugu), 18px body, 1.55x line-height              |
|  COLOUR:       Medical Deep Teal (#0D5C75), Calming Slate (#F8FAFC), Non-Alarmist Warm Amber (#D97706)              |
|  SPACING:      Minimum 52dp touch targets, 16dp-20dp padding, 12dp card separation                                 |
|  TONE:         Reassuring, respectful, objective, educational, doctor-empowering                                     |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 3.1. Layout: Low-Cost Android Ergonomics
* **Viewport Baseline:** Engineered for **360dp width** (typical 720×1600 physical resolution screens at 2.0x density, e.g., Redmi 9A, Samsung Galaxy M04, Realme C-series, JioPhone Next).
* **Strict Single-Column Flow:** No side-by-side split cards or multi-column grids that cause horizontal scrolling. Every element stacks vertically in a linear narrative.
* **Thumb-Zone Optimization:** All critical action buttons (Upload, Listen to Audio, Doctor Questions) are anchored within the bottom 60% of the screen, easily reachable by a single hand or trembling fingers without requiring thumb stretching.
* **Zero Gestural Complexity:** No swipe-to-delete, pinch-to-zoom, or hidden drawer menus. All actions use explicit, high-contrast, labeled tap buttons.

### 3.2. Typography: Indic Scripts & Long Words
* **Font Family Stack:**
  ```css
  font-family: -apple-system, BlinkMacSystemFont, "Noto Sans Devanagari", "Noto Sans Tamil", 
               "Noto Sans Telugu", "Roboto", "Segoe UI", sans-serif;
  ```
* **Scale for Aging Eyes:**
  * Headings (`h1`, `h2`): `22px` to `26px` (Bold, `#0F172A`).
  * Parameter Titles & Key Values: `18px` to `20px` (Semi-Bold).
  * Body Text & Explanations: Minimum `16px` to `17px` (Regular, `#334155`). Never use sub-14px text for any health copy.
* **Indic Script Vertical Clearance (Matras & Diacritics):**
  * Indian scripts (Devanagari, Telugu, Tamil, Kannada) feature complex vowel signs (*matras*) above and below consonant characters.
  * Standard Latin `line-height: 1.2` or `1.3` will clip these marks, rendering words illegible or grammatically corrupted.
  * **Mandatory Rule:** Enforce `line-height: 1.55` to `1.65` across all vernacular copy to guarantee zero glyph clipping.
* **Word-Wrap for Agglutinative Languages:**
  * Dravidian languages (Telugu, Tamil, Kannada) frequently combine multiple concepts into long compound words (e.g., Telugu: *రక్తంలో చక్కెర స్థాయి* [blood sugar level]).
  * **Mandatory Rule:** Apply `overflow-wrap: break-word; hyphens: auto;` to prevent text truncation or layout breaking on 360dp viewports.

### 3.3. Colour Palette: Calming & Non-Alarmist (WCAG AAA)
* **Primary Brand / Trust:**
  * Deep Medical Teal (`#0D5C75`) — communicates medical authority, calmness, and stability.
  * Clean White (`#FFFFFF`) — card surfaces.
  * Muted Background (`#F8FAFC`) — minimizes glare on cheap TFT/LCD screens in bright Indian daylight.
* **Status Indication (The Anti-Panic Palette):**
  * **Normal / Healthy:** Soft Emerald Green (`#16A34A` text on `#ECFDF5` background).
  * **Slightly Elevated / Borderline:** Warm Ochre / Muted Amber (`#D97706` text on `#FEF3C7` background). **We strictly forbid aggressive crimson red for routine borderline variations**, preventing unnecessary panic.
  * **Critically Out of Range:** Dark Coral / Maroon (`#B91C1C` text on `#FEE2E2` background), paired with an explicit instruction to contact the physician.
* **Contrast Compliance:** All text-to-background combinations exceed **WCAG AAA 7:1 contrast ratio**, ensuring readability for patients with presbyopia, cataracts, or low-brightness smartphone screens.

### 3.4. Spacing & Touch Targets: Senior Motor Support
* **Touch Target Sizing:** All interactive elements (Pill chips, Audio Play button, Upload CTA) feature a **minimum touch height of 52dp to 56dp**.
* **Hit-Area Padding:** Extra invisible padding (`8dp`) around buttons to prevent "near-miss" taps by users with hand tremors or arthritis.
* **Card Breathing Room:** Minimum `16dp` vertical margin between distinct biomarker cards to visually separate distinct clinical parameters.

### 3.5. Tone of Voice: Reassuring, Respectful & Objective
* **Non-Alarmist:** Never use scary medical warnings like *"Dangerous elevation detected"* or *"High risk of organ failure"*. Instead, use supportive, objective framing: *"Your blood sugar marker is slightly above standard laboratory guidelines. This is common and can often be managed with diet and medication adjustments by your doctor."*
* **Empowering, Never Prescriptive:** Never tell the patient what medication to take. Always channel their energy into productive dialogue with their physician: *"Here are three questions you can ask your doctor at your consultation..."*
* **Respectful Cultural Framing:** In Hindi, Tamil, and Telugu, always use respectful honorifics (e.g., Hindi: *आप / आपका*, Tamil: *உங்கள்*, Telugu: *మీరు / మీ*) to maintain trust with senior citizens.

---

## 4. Hardware & Demographic Constraint Checklist

| Constraint Dimension | Technical Reality in Target Segment | ReportSaathi Architectural Solution |
| :--- | :--- | :--- |
| **Elderly Vision (Presbyopia / Cataracts)** | Cannot read 12–14px fonts; struggles with low contrast in sunlight. | Minimum 16–18px font; 7:1+ WCAG AAA contrast; 1-click native voice narration alternative. |
| **Tremors & Fine Motor Loss** | Misses small 32dp buttons; double-taps by accident. | 56dp primary touch targets; generous 16dp spacing; debounce on all tap events. |
| **Low-End Android Device (1GB RAM)** | Apps >50MB crash; complex JavaScript animations drop frames. | Web-first architecture; bundle size <40KB; CSS-driven transitions; zero heavy 3D rendering. |
| **Small 360dp Screen Width** | Multi-column layouts get clipped or overlap. | Strict single-column vertical layout; no horizontal scrollbars; flex-wrap on all button clusters. |
| **Indic Scripts & Matras** | Vowels above/below letters get clipped by tight line heights. | Mandatory `1.55x–1.65x` line-height; native system Indic fonts; zero custom webfont load lag. |
| **Long Compound Words** | Words in Telugu/Tamil break containers or overflow screen. | `overflow-wrap: break-word;` with flexible auto-wrapping card containers. |
| **Spotty 3G/4G Connectivity** | Uploads fail on slow Indian mobile data connections. | Client-side image compression before upload; automatic retry with clear visual progress feedback. |

---

## 5. Summary of Visual References

The following high-resolution design artifacts are archived in [docs/references/](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/):

1. **[ref-01-diagnostic-lab-dr-lal.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-01-diagnostic-lab-dr-lal.png):**  
   *Side-by-side contrast:* Raw tabular lab report with alarming red asterisks (what to avoid) vs. ReportSaathi simplified range card with plain-language explanation (what to borrow).
2. **[ref-02-symptom-checker-ada.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-02-symptom-checker-ada.png):**  
   *Side-by-side contrast:* 35-step questionnaire and worst-case ER alert (what to avoid) vs. calm, reassuring single-step lab explanation card (what to borrow).
3. **[ref-03-pharmacy-1mg.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-03-pharmacy-1mg.png):**  
   *Side-by-side contrast:* Cluttered e-commerce discounts and upsell popups (what to avoid) vs. clean visual dosage timing icons (Sun/Moon/Meal) (what to borrow).
4. **[ref-04-whatsapp-audio.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/ref-04-whatsapp-audio.png):**  
   *Side-by-side contrast:* Viral medical forwards and privacy leaks (what to avoid) vs. familiar 1-tap green voice player and bottom sheets (what to borrow).
5. **[screen-1-upload-states.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/screen-1-upload-states.png):**  
   *Screen 1 States:* Default (language chips & upload box), Empty (instructional prompt), Loading (upload progress bar), and Error (blurry photo guidance).
6. **[screen-2-processing-states.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/screen-2-processing-states.png):**  
   *Screen 2 States:* Default progress stepper, step loading spinner, empty queue, and non-lab parsing error.
7. **[screen-3-report-card-states.png](file:///c:/Users/Spoorthi%20P%20Jain/reportsaathi/docs/references/screen-3-report-card-states.png):**  
   *Screen 3 States:* Default results card, active audio narration waveform, Devanagari Hindi vernacular layout, and missing reference range notice.
