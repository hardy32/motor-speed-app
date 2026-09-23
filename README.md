# Motor Speed Predictor — Deployment Guide

This folder turns your notebook's Random Forest model into a shareable web app.

## Files

- `train_model.py` — trains the model and saves it as `model.joblib`
- `app.py` — the Streamlit dashboard people will use
- `requirements.txt` — the Python packages needed to run it
- `model.joblib` — **already trained and included**, on your real dataset

I trained this already so you have a working model right now: Random Forest,
20 trees, depth capped at 14, tested on a held-out 20% split.
**Test R² = 0.9991, MSE = 0.00088** — essentially as accurate as the
uncapped 100-tree version from your notebook (R² = 0.9999), but as a ~30 MB
file instead of ~2 GB, which is what actually makes it deployable.

## Step 1: Run it locally first

`model.joblib` is already included, so you can skip straight to launching
the app. (Only retrain with `train_model.py` if you get new data later —
you'd need `temperature_data.csv` in this folder for that, and note it can
take 3-5 minutes to train.)

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Launch the app:
   ```
   streamlit run app.py
   ```
   Your browser will open automatically at `http://localhost:8501` — try entering some values and predicting.

## Step 2: Deploy it for free (Streamlit Community Cloud)

Once it works locally, this is the simplest possible way to put it on the internet:

1. Create a free GitHub account if you don't have one, and create a new repository.
2. Upload these files to that repository: `app.py`, `requirements.txt`, `model.joblib`
   (you do **not** need to upload `temperature_data.csv` or `train_model.py` — the app only needs the trained model file).
3. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
4. Click "New app," pick your repository, and set the main file to `app.py`.
5. Click "Deploy." In a minute or two you'll get a public URL you can share with anyone.

That's it — no servers to manage, no Docker, no cloud console.

## When you'd need something more than this

- **If other software needs to call the model automatically** (not a human typing into a form) → you'd want a REST API instead (FastAPI/Flask), which I can build with you next.
- **If you're processing large files on a schedule** → a batch script instead of a web app is more appropriate.
- **If prediction volume gets large or you need enterprise security** → cloud platforms (AWS SageMaker, GCP Vertex AI, Azure ML) give more control, at the cost of more setup.

For now, Streamlit Community Cloud is the right-sized solution: minimal setup, free, and it directly matches what you asked for (a dashboard someone can type into).
