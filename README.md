# TransCore NTCIP Assistant — Demo

A small Streamlit chat app that answers questions about the **NTCIP**
family of ITS standards, TransCore-branded for prospect demos. Backed
by Anthropic's Claude (Sonnet 4.6), with a hand-curated NTCIP overview
baked into the system prompt.

This is a demo — knowledge is a May 2026 snapshot and is not refreshed.

---

## Run locally

1. **Create a virtualenv and install dependencies.**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Set your Anthropic API key.** Copy the example secrets file and
   fill in your key:

   ```powershell
   Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
   # then edit .streamlit\secrets.toml and paste your key
   ```

3. **Run the app.**

   ```powershell
   streamlit run app.py
   ```

   Streamlit opens the app at <http://localhost:8501>.

---

## Deploy to Streamlit Community Cloud (free, public URL)

1. Create a GitHub repo for this project and push.

   ```powershell
   git init
   git add .
   git commit -m "Initial NTCIP demo"
   git branch -M main
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```

   `.streamlit/secrets.toml` is gitignored — your key won't be pushed.

2. Sign in at <https://share.streamlit.io> with the same GitHub account.
   Click **New app**, point at the repo and `app.py`.

3. In the app's **Settings → Secrets**, paste:

   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   # Optional shared-password gate:
   # DEMO_PASSWORD = "change-me"
   ```

4. Deploy. Streamlit returns a `https://<app-name>.streamlit.app` URL
   you can share with the prospect.

---

## Optional: shared-password gate

Anyone with the public Streamlit URL can hit the app and spend tokens.
For prospect-only access, add `DEMO_PASSWORD` to your secrets (either
locally or in the Streamlit Cloud secrets panel). When set, the app
shows a password prompt before the chat is reachable.

---

## Project layout

```
app.py                       Streamlit chat app
ntcip_context.py             Curated NTCIP overview (system prompt body)
requirements.txt             streamlit, anthropic
.streamlit/
  config.toml                Page theme
  secrets.toml.example       Template — copy to secrets.toml (gitignored)
.gitignore
README.md                    This file
```

---

## Cost notes

- Model: `claude-sonnet-4-6` (`$3 / $15` per 1M input / output tokens).
- The NTCIP overview (~3–4K tokens) is cached as part of the system
  prompt; the first request writes the cache, subsequent requests within
  ~5 minutes read it back at ~10% of input cost.
- `output_config.effort` is set to `"low"` and thinking is disabled —
  both keep latency and per-message cost down for a chat demo.
- For a low-volume prospect demo, expect total cost in the
  cents-to-low-dollars range.

---

## Limitations

- Static snapshot of the NTCIP standards list (May 2026). Not refreshed.
- No retrieval over the actual standards PDFs — answers come from the
  curated overview plus Claude's prior knowledge.
- No conversation persistence across browser sessions.
- No analytics or feedback capture.
