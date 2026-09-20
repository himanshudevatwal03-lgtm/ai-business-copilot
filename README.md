# 🚀 AI Business Copilot

> **Snapdragon AI Lab Build & Present Challenge 2026**  
> An on-device ready, local-first enterprise AI assistant that analyzes ERP operations data and answers natural-language business questions about sales, invoices, customers, inventory, and performance.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Qualcomm AI Hub Ready](https://img.shields.io/badge/Qualcomm%20AI%20Hub-Phase%202%20Ready-E10600.svg)](https://aihub.qualcomm.com/)

---

## 📖 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Key Capabilities & Features](#-key-capabilities--features)
3. [Architecture & System Design](#-architecture--system-design)
4. [Technology Stack](#-technology-stack)
5. [Future Qualcomm AI Hub Integration Roadmap (Phase 2)](#-future-qualcomm-ai-hub-integration-roadmap-phase-2)
6. [Local Setup & Running](#-local-setup--running)
7. [Environment Variables](#-environment-variables)
8. [Example Queries & Testing](#-example-queries--testing)
9. [Sample ERP Dataset](#-sample-erp-dataset)
10. [Testing & Verification](#-testing--verification)
11. [Deployment Guide](#-deployment-guide)
    - [Docker](#option-1-docker-single-production-container)
    - [Unified Local Production Run](#option-2-unified-local-production-run)
    - [Render](#option-3-render-single-web-service)

---

## 📌 Executive Summary

Modern enterprise leaders face a common dilemma: ERP systems and financial ledgers hold massive amounts of operational data, but extracting actionable insights requires SQL queries, specialized business analysts, or cumbersome dashboards. Furthermore, enterprises cannot safely upload proprietary financial balance sheets, customer debts, and profit margins to third-party cloud LLMs.

**AI Business Copilot** solves this by establishing a **Local-First, Privacy-Preserving Business Intelligence Assistant**:
- Delivers instant natural-language query resolution over live ERP databases.
- Operates out-of-the-box with **zero external cloud API keys required**.
- Uses an explicit **Modular Inference Architecture** designed to seamlessly slot in quantized on-device models compiled via **Qualcomm AI Hub** for Snapdragon X Elite / Hexagon NPU platforms.

---

## ⚡ Key Capabilities & Features

- **Interactive Natural-Language Q&A:**
  - Executive-level synthesis for sales velocity, cashflow aging, product profitability, and stock deficits.
  - Automatic tabular drill-downs, KPI chips, and proactive follow-up recommendations.
- **Real-Time Executive Dashboard:**
  - Live KPI metric cards (Current Month Revenue, MoM Growth %, Overdue Receivables, Low-Stock Alerts).
  - 6-Month Sales Trajectory & Volume Area Chart.
  - Top 5 Products by Revenue Leaderboard.
- **Enterprise Data Explorer:**
  - Filterable, searchable interface across Invoices, Customers & Accounts, and Inventory Health.
- **One-Click ERP Reset & Simulation:**
  - Seed and reseed synthetic yet realistic multi-month ERP transactions on demand.
- **Qualcomm AI Hub Roadmap Explorer:**
  - In-app interactive architecture guide explaining the Snapdragon NPU deployment strategy for competition evaluators.

---

## 🏗️ Architecture & System Design

To ensure zero unnecessary microservice overhead and optimal developer experience, the system utilizes a streamlined, decoupled architecture:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        User Web Interface                              │
│         React 18 + Vite + Tailwind CSS + Lucide Icons + Recharts       │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ HTTP / REST (/api/*)
┌────────────────────────────────────▼───────────────────────────────────┐
│                      FastAPI Backend Engine                            │
│  ├── /api/dashboard/*  (KPIs, 6-Month Trends, Top Products)            │
│  ├── /api/copilot/*    (Natural Language Query Intent Resolution)      │
│  └── /api/erp/*        (Invoices, Accounts, Inventory, Reseed)         │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   ▼                                 ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│       ERP Data Service Layer         │  │   Modular Inference Layer    │
│  ├── SQLAlchemy ORM                  │  │   ├── BaseInferenceProvider  │
│  └── SQLite Database                 │  │   ├── LocalAnalyticsProvider │
│      (Customers, Orders, Invoices,   │  │   │   (Default: Zero-Key)    │
│       Products, Inventory Ledgers)   │  │   ├── CloudLLMProvider       │
│                                      │  │   │   (Optional OpenAI/Cloud)│
│                                      │  │   └── QualcommAIHubAdapter   │
│                                      │  │       (Phase 2 NPU Bridge)   │
└──────────────────────────────────────┘  └──────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI (Python 3.11)** | Asynchronous, auto-generates OpenAPI/Swagger docs, high throughput, native Pydantic v2 validation. |
| **Database & ORM** | **SQLite + SQLAlchemy 2.0** | Zero-configuration local database, deterministic, ACID-compliant, ideal for on-device data sovereignty. |
| **Copilot Core** | **Modular Python Engine** | Abstract provider interface with high-precision deterministic analytics engine out-of-the-box. |
| **Frontend UI** | **React 18 + Vite** | Instant HMR, minimal bundle size, lightning-fast rendering. |
| **Styling & Icons** | **Tailwind CSS + Lucide** | High-tech Qualcomm/Snapdragon corporate dark-mode aesthetic. |
| **Visualizations** | **Recharts** | Declarative, responsive SVG charting for financial and operational metrics. |
| **Containerization**| **Docker + Compose** | Multi-stage build providing a single production container image. |

---

## 🔮 Qualcomm AI Hub Integration — Phase 2 (Active)

> **Note for Reviewers:**
> Phase 1 (this repo's default) runs entirely on the built-in deterministic analytics engine — zero external calls. Phase 2, below, is a real, runnable on-device NPU pipeline via `onnxruntime-genai` + QNN, implemented in `backend/app/providers/qualcomm_adapter.py`. It's off by default and only activates on a Snapdragon X Elite machine with the model bundle in place; everywhere else (including this repo's Render deployment) it transparently reports "not ready" and falls back to Phase 1.

### Running Phase 2 on a Snapdragon X Elite device

1. **Export the model via Qualcomm AI Hub** (run this on/for the target device — it compiles on Qualcomm's cloud device farm and can take a while):
   ```bash
   pip install qai_hub_models
   qai-hub configure --api_token <YOUR_QAI_HUB_TOKEN>

   python -m qai_hub_models.models.phi_3_5_mini_instruct.export \
       --device "Snapdragon X Elite CRD" \
       --skip-inferencing --skip-profiling \
       --output-dir genie_bundle
   ```
   This produces `genie_bundle/` containing `genai_config.json`, the tokenizer files, and the compiled QNN context binaries.

2. **Install the on-device runtime** on the Snapdragon machine:
   ```bash
   pip install -r backend/requirements-qualcomm.txt
   ```
   (This file is intentionally separate from `backend/requirements.txt` — it's Windows ARM64-specific and must never be installed in the Linux Docker/Render build.)

3. **Point the backend at the bundle and switch providers**:
   ```bash
   set INFERENCE_PROVIDER=qualcomm
   set QUALCOMM_MODEL_DIR=C:\path\to\genie_bundle
   uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
   ```

4. Ask the Copilot a question — `/api/copilot/query` now runs real autoregressive generation on the Hexagon NPU via `onnxruntime-genai`, grounded in the live ERP context, and the response's `inference_provider` field will read `qualcomm_npu (onnxruntime-genai + QNN, live)`.

**Data privacy:** in this mode, confidential business data (invoices, margins, customer records) never leaves the Snapdragon device — the ERP context is only ever sent to the local NPU process, not to any cloud API.

---

## 💻 Local Setup & Running

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11)
- **Node.js 18+** & **npm**
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/himanshudevatwal03-lgtm/ai-business-copilot.git
cd ai-business-copilot
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```
FastAPI interactive Swagger documentation is available at: `http://localhost:8000/docs`

### 3. Frontend Setup
In a new terminal window:
```bash
# Navigate to frontend
cd frontend

# Install Node packages
npm install

# Start Vite development server
npm run dev
```
Open your browser at: `http://localhost:5173`

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` in the project root if you wish to customize configuration:

```ini
# Project Settings
PROJECT_NAME="AI Business Copilot"
ENVIRONMENT="development"
DATABASE_URL="sqlite:///./copilot_erp.db"

# Inference Provider:
# "local"    -> Default high-accuracy local analytics (ZERO keys required)
# "cloud"    -> Optional OpenAI / cloud LLM completions
# "qualcomm" -> Phase 2 Snapdragon NPU integration adapter (see Phase 2 section above)
INFERENCE_PROVIDER="local"

# Only used when INFERENCE_PROVIDER="qualcomm" — path to the genie_bundle/
# directory produced by qai_hub_models export (see Phase 2 section above).
QUALCOMM_MODEL_DIR=""

# Optional Cloud API Key (only if INFERENCE_PROVIDER="cloud")
OPENAI_API_KEY=""
OPENAI_MODEL="gpt-4o-mini"
```

---

## 💬 Example Queries & Testing

You can ask any of the following natural-language questions in the web interface or via `POST /api/copilot/query`:

| Example Query | What the Copilot Does |
| :--- | :--- |
| **"What were the total sales this month?"** | Computes current month invoice totals, calculates MoM growth %, and displays monthly breakdown. |
| **"Which products are selling the most?"** | Ranks top 5 products by revenue and units sold, displaying a formatted comparison table. |
| **"Which customers have overdue payments?"** | Lists all delinquent accounts, days past due, and total outstanding debt requiring collections. |
| **"What are the major sales trends?"** | Analyzes 6-month revenue trajectory, order volume changes, and growth direction. |
| **"Summarize the current business situation."** | Delivers an executive briefing spanning sales growth, cash flow risk, low-stock warnings, and client status. |
| **"Which products are low in stock?"** | Flags SKUs below safety reorder threshold with exact deficit units. |

---

## 📊 Sample ERP Dataset

The project comes pre-configured with a realistic enterprise dataset seeded on startup:
- **20 Corporate Customers** across North America, Europe, and Asia Pacific with defined credit limits and account statuses.
- **12 Catalog Products** spanning Edge AI Hardware, IoT Sensors, Enterprise Software, and Accessories.
- **100+ Orders & Invoices** spanning the past 6 months with realistic payment statuses (Paid, Pending, Overdue).
- Standalone portable export available in `sample_data/erp_export.json`.

---

## 🧪 Testing & Verification

Run automated backend tests to verify database integrity and Copilot query responses:

```bash
cd backend
pytest -v
```

All tests verify:
- API health and system status.
- Dashboard KPI calculations and chronological trend ordering.
- Copilot natural-language intent classification and responses across all 5 core question scenarios.

---

## 🚢 Deployment Guide

### Option 1: Docker (Single Production Container)
The included multi-stage Dockerfile compiles the React frontend and packages it directly with FastAPI:

```bash
# Build and run with Docker Compose
docker compose up --build -d
```
Access the application at `http://localhost:8000`.

### Option 2: Unified Local Production Run
```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Run backend (FastAPI automatically serves frontend/dist)
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in any browser.

---

### Option 3: Render (Single Web Service)

[#option-3-render-single-web-service](#option-3-render-single-web-service)

Since the Dockerfile already produces a unified production image (frontend built and served by FastAPI), this repo deploys to Render as a single Docker-based Web Service:

1. Push the repo to GitHub (already done).
2. In Render, create a **New Web Service** → connect this repo → Environment: **Docker**.
3. Leave the build/start commands blank (the Dockerfile's `CMD` handles it).
4. Set environment variables under **Environment**: `INFERENCE_PROVIDER=local` (and `OPENAI_API_KEY` only if using `cloud`).
5. Render sets `PORT` automatically; Uvicorn in the Dockerfile binds `0.0.0.0:8000` — if Render's free tier requires honoring `$PORT`, override the start command to `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`.
6. Deploy — the same container serves both the API and the built React app from one URL.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
