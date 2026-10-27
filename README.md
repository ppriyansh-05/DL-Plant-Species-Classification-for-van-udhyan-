# Van Udyan Plant AI — Urban Biodiversity Deep Learning Platform

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/frontend-React_19_+_Vite-61DAFB.svg)](https://vitejs.dev/)
[![Tailwind CSS v4](https://img.shields.io/badge/styling-Tailwind_CSS_v4-38B2AC.svg)](https://tailwindcss.com/)
[![License: CC BY-NC](https://img.shields.io/badge/License-CC_BY--NC-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Partner: RSWF Pune](https://img.shields.io/badge/Partner-RSWF_Pune-green.svg)](https://www.rswf.org/)

A full-stack, nature-themed, bento-grid urban biodiversity web application powered by **FastAPI** on the backend and **React + Vite + TypeScript + Tailwind CSS** on the frontend. The platform performs real-time in-situ plant species classification across 15 native urban tree species cataloged at the **Van Udyan bio-reserve (RSWF Pune, Maharashtra)** using a fine-tuned **EfficientNetB0** deep learning model.

---

## 🌿 Key Features

- **Premium Dark Nature Aesthetic**: Translucent forest green glassmorphic bento cards (`rgba(20,60,42,0.55)`), delicate gold-to-green gradient typography (*Playfair Display* & *Poppins*), and interactive parallax drifting leaves.
- **Real-Time Neural Inference**: Sub-100ms forward inference using preprocessed 224×224 RGB inputs fed to an authentic EfficientNetB0 neural network. Zero fallback hallucinations.
- **Top-3 Prediction Trace & Animated Confidence Ring**: Dynamic SVG circular gauge colored by confidence threshold (Green ≥70%, Amber 40–70%, Red <40%) with honest low-confidence warnings below 40%.
- **RSWF Pune Zone Distribution**: Direct mapping of species across Van Udyan Zones 1, 2, and 3.
- **Interactive Botanical Catalog**: Filterable and searchable 15-species grid with deep botanical modal profiles (family, foliage, phenology, and ecological role).
- **Empirical Benchmarking Dashboard**: Interactive dark-mode Recharts displaying verified evaluation splits (Held-out Test vs. Van Udyan In-Situ Benchmark) upholding strict academic transparency.
- **Mobile First & Camera Ready**: Responsive touch UI supporting native camera capture (`capture="environment"`) for field walks.

---

## 🏗️ Architecture & Project Structure

```text
├── backend/                    # FastAPI ASGI Backend Service
│   ├── config.py               # Taxonomy, zone mapping & storage configuration
│   ├── inference.py            # Model loading, PIL preprocessing & Top-K prediction
│   ├── main.py                 # REST API endpoints (/api/predict, /api/species, etc.)
│   ├── model_loader.py         # Keras archive sanitizer & Supabase storage fallback
│   ├── requirements.txt        # Backend Python dependencies
│   └── test_smoke.py           # Strict backend smoke test suite
├── frontend/                   # Modern React 19 + TypeScript + Vite SPA
│   ├── src/
│   │   ├── assets/             # Botanical SVGs & hero leaf illustrations
│   │   ├── components/         # Bento features, Hero, Uploader, ConfidenceRing, Charts
│   │   ├── lib/api.ts          # Typed REST API client
│   │   ├── App.tsx             # Root container with code-split routes
│   │   └── index.css           # Custom glassmorphic tokens & dark gradients
│   ├── package.json
│   └── vite.config.ts          # Vite build configuration with API proxy
├── app/                        # (Legacy) Streamlit application preserved intact
├── best_van_udyan_top15.keras  # Trained EfficientNetB0 Keras model weights
├── class_mapping.json          # Index-to-species class dictionary (15 classes)
├── evaluation_summary.json     # Verified empirical benchmark & test metrics
├── render.yaml                 # Multi-service Render deployment blueprint
└── .env.example                # Documented environment variables
```

---

## 🚀 Local Development Setup

### 1. Prerequisites
- **Python**: 3.10+
- **Node.js**: v18+ (tested on Node v24)
- **Model weights**: Ensure `best_van_udyan_top15.keras` is in the project root.

### 2. Backend Setup (FastAPI)
```bash
# In project root
python -m pip install -r backend/requirements.txt

# Run backend smoke test
python backend/test_smoke.py

# Launch FastAPI development server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The FastAPI backend and interactive OpenAPI documentation will be accessible at:
- API Base: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`
- Health Diagnostic: `http://127.0.0.1:8000/api/health`

### 3. Frontend Setup (React + Vite)
```bash
cd frontend
npm install

# Build check
npm run build

# Launch Vite development server
npm run dev
```
The React web application will open at:
- Web App: `http://127.0.0.1:5173`

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/predict` | Multipart image upload (JPG/PNG/WEBP, max 8MB). Returns `{ top_k: [...], inference_ms }`. |
| `GET` | `/api/species` | Returns list of all 15 species with botanical family, Marathi names, and zones. |
| `GET` | `/api/metrics` | Serves verified empirical metrics from `evaluation_summary.json`. |
| `GET` | `/api/health` | Returns health status, model loading diagnostics, and version info. |
| `GET` | `/api/samples` | Lists authentic Van Udyan field benchmark photos for instant one-click testing. |

---

## 🌐 Deployment on Render

The repository includes an updated `render.yaml` configuring two interconnected services:
1. **`van-udyan-backend`**: Python Web Service executing `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
2. **`van-udyan-frontend`**: Static Site building `frontend/` (`npm run build`) and serving `frontend/dist`.

### Deployment Steps:
1. Connect your repository to [Render Dashboard](https://dashboard.render.com/).
2. Select **Blueprints** and choose `render.yaml`.
3. In the Render environment settings, configure the following secrets if downloading model weights from Supabase:
   - `SUPABASE_URL`: Your project URL (e.g., `https://xyz.supabase.co`)
   - `SUPABASE_KEY`: Your service role or anon key
   - `VITE_API_URL`: `https://van-udyan-backend.onrender.com`

---

## 📝 Changelog (Streamlit to Modern Full-Stack Web App)

- **Backend Overhaul**: Migrated monolithic Streamlit scripts into a modular FastAPI service with strict Pydantic/type validation, 8MB payload guards, and CORS configuration.
- **Model Loading Isolation**: Pre-loads the EfficientNetB0 Keras model once at server lifespan startup; added zipfile sanitization to prevent version mismatch errors across Keras 3 releases.
- **Pinterest-Inspired Bento UI**: Implemented dark forest green background (`#06140E` to `#0F2A1E`), translucent cards with inner glows, serif display headlines with gold-to-green text gradients, and interactive parallax botanical leaves.
- **Enhanced Mobile Photography**: Added native camera integration (`capture="environment"`), drag-and-drop file ingestion, and one-click benchmark field sample selector.
- **Academic Transparency Dashboard**: Integrated dark-mode Recharts displaying empirical held-out test (23.78%) and field benchmark top-3 (33.33%) metrics without pseudo-predictions.
