
# ReportSaathi 🩺

### Making Medical Reports Easier to Understand

ReportSaathi is a web-based application designed to make medical reports more accessible and easier to understand. It aims to help users, especially elderly people and individuals with limited technical knowledge, access information from their medical documents conveniently.

The current version allows users to upload PDF medical reports and extract their text through a simple web interface.

## 🎯 Problem Statement

Medical reports often contain complex medical terminology and technical information that can be difficult for ordinary people to understand. This creates challenges for patients and their family members when reviewing medical documents.

ReportSaathi aims to simplify access to medical report information through an easy-to-use digital platform.

## ✨ Features

- **PDF Upload:** Upload medical reports in PDF format.
- **Text Extraction:** Extract text from uploaded PDF documents.
- **Page Information:** Display the total number of pages processed.
- **User-Friendly Interface:** Simple interface for convenient document uploading and viewing extracted text.
- **API Integration:** Backend processing using FastAPI.
- **Error Handling:** Provides feedback for unsuccessful uploads or processing errors.
- **Safety Notice:** Reminds users to verify extracted information against the original medical report.

## 🛠️ Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| PDF Processing | PyPDF |
| API Documentation | Swagger UI |
| Server | Uvicorn |
| Testing | Pytest |
| Version Control | Git and GitHub |

## 📂 Project Structure

```text
reportsaathi/
│
├── .github/
│   └── workflows/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── static/
│   │       └── index.html
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/
│   ├── 01-problem.md
│   ├── 02-research.md
│   ├── 03-scope.md
│   ├── 04-design.md
│   ├── 05-prd.md
│   ├── 06-architecture.md
│   ├── 06a-api-contract.md
│   ├── 06b-safety-rules.md
│   ├── 07-test-plan.md
│   └── 08-tasks.md
│
├── frontend/
│   └── package.json
│
├── tests/
│   └── fixtures/
│
├── .gitignore
├── make_review_zip.py
├── pyproject.toml
├── render.yaml
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/spoorthijain056/reportsaathi.git
```

### 2. Navigate to the Project Folder

```bash
cd reportsaathi
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r backend/requirements.txt
```

### 6. Run the Application

```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

### 7. Open the Application

Visit the following URL in your browser:

- Application: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/api/health

## 🔄 Application Workflow

1. Open the ReportSaathi web application.
2. Select a medical report in PDF format.
3. Upload the selected PDF.
4. The backend processes the document.
5. Extracted text and page information are displayed.
6. The user can review the extracted content alongside the original report.

## 📸 Screenshots

Screenshots of the working application will be added here.

| Application Interface | PDF Upload |
|---|---|
| Add homepage screenshot | Add upload screenshot |

| Successful Processing | Extracted Text |
|---|---|
| Add success screenshot | Add extracted text screenshot |

## 🚀 Future Enhancements

The following features are planned for future development:

- Simplification of complex medical terminology.
- Support for multiple regional languages.
- AI-assisted medical report explanations.
- Identification and highlighting of abnormal report values.
- Audio-based explanations for elderly users.
- Improved accessibility and user experience.

## ⚠️ Medical Disclaimer

ReportSaathi is an informational tool and is not a substitute for professional medical advice, diagnosis, or treatment.

The current version extracts text from PDF documents. Extracted text may contain errors or omissions. Always verify information against the original medical report and consult a qualified healthcare professional for medical interpretation.

## 👩‍💻 Developer

**Spoorthi Jain**

GitHub: [@spoorthijain056](https://github.com/spoorthijain056)

Project Repository: [ReportSaathi](https://github.com/spoorthijain056/reportsaathi)

---

⭐ If you find this project interesting, consider giving the repository a star!