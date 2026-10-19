# Van Udyan Plant AI — Deployment Guide: Render + Supabase

This guide outlines the exact, step-by-step procedure to deploy the **Van Udyan Plant AI** web application to **Render** connected with **Supabase Storage** for secure model management.

---

## 1. Architecture Overview

- **Frontend & Web Layer**: Python Streamlit interface providing responsive prediction cards, real-time confidence scores, low-confidence warnings, and empirical metrics audit.
- **Model Storage**: **Supabase Storage** (Private or Public Bucket named `models`) housing the trained Keras model (`best_van_udyan_top15.keras`).
- **Web Hosting**: **Render Web Service** (Free tier, auto-reloading upon push to `origin/main`).
- **Security & Secrets**: No passwords, database URLs, or Supabase service-role keys are hardcoded in git. All connections are initialized server-side via environment variables.
- **Graceful Fallback**: If the model is not found or credentials are not yet entered, the web application runs in interactive demonstration mode without crashing.

---

## 2. Step 1: Set Up Supabase Storage for the Model

Because deep learning weights (`best_van_udyan_top15.keras`, ~20–50 MB) must not be committed to GitHub, we host the artifact in Supabase Storage.

1. **Log in to Supabase**: Navigate to [https://supabase.com/dashboard](https://supabase.com/dashboard) and create or open your project.
2. **Create Storage Bucket**:
   - In the left sidebar, click **Storage**.
   - Click **New Bucket**.
   - Bucket Name: `models`
   - Privacy: You can keep **Public bucket: OFF** for security (the app retrieves via authenticated server-side API) or **ON** if you prefer public URL downloads.
   - Click **Save**.
3. **Upload the Model**:
   - Open the `models` bucket.
   - Click **Upload File** and select your trained model: `best_van_udyan_top15.keras` (downloaded from your Google Colab session).
   - Ensure the filename in the bucket is exactly `best_van_udyan_top15.keras`.
4. **Copy API Credentials**:
   - In the left sidebar, click **Project Settings** (gear icon) -> **API**.
   - Note down:
     - **Project URL** (e.g., `https://xyzprojectref.supabase.co`)
     - **API Keys**: Copy the `anon` / `public` key (or `service_role` key if using a private bucket).

---

## 3. Step 2: Deploy to Render

1. **Log in to Render**: Navigate to [https://dashboard.render.com/](https://dashboard.render.com/).
2. **Create New Web Service**:
   - Click **New +** -> **Web Service**.
   - Connect your GitHub repository:
     `https://github.com/ppriyansh-05/DL-Plant-Species-Classification-for-van-udhyan-`
3. **Configure Service Settings**:
   - **Name**: `van-udyan-plant-ai`
   - **Region**: Choose closest to you (e.g., Singapore or Oregon)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (root of repo)
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false
     ```
   - **Instance Type**: `Free`
4. **Add Environment Variables**:
   Under **Environment Variables**, add the following key-value pairs:
   | Key | Value |
   | :--- | :--- |
   | `PYTHON_VERSION` | `3.10.12` |
   | `SUPABASE_URL` | *Your Supabase Project URL* |
   | `SUPABASE_KEY` | *Your Supabase anon or service-role key* |
   | `SUPABASE_BUCKET` | `models` |
   | `SUPABASE_MODEL_PATH` | `best_van_udyan_top15.keras` |
5. **Deploy**:
   - Click **Create Web Service**.
   - Render will clone the repository, install dependencies, and launch Streamlit on the assigned URL (`https://van-udyan-plant-ai.onrender.com`).

---

## 4. Local Smoke-Test Command

To test the application on your local machine before pushing or deploying:

```bash
# 1. Activate your virtual environment
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/Mac

# 2. Run the smoke test suite
python scripts/smoke_test_app.py

# 3. Launch the Streamlit web server
streamlit run app/main.py
```

The app will open automatically in your browser at `http://localhost:8501`.
