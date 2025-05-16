# Blue Archive Scenario Script Converter
A desktop UI application to streamline localization workflows for Blue Archive scenario scripts. The converter supports:

- EN → JP: Overwrite Japanese script fields with English translations.
- JP → JP: Migrate old-format Japanese scripts to a new JSON schema.

🚀 Features
- One‑click conversion of individual JSON files.
- Batch processing: select an entire folder and convert every supported Excel‑exported JSON.
- Wide coverage: handles scenario scripts plus dozens of other localization tables (dialogs, skills, gacha shop, character profiles, etc.).
- Data‑safe: preserves untranslated fields; skips entries when no translation is present.

📦 Installation
1. Clone the repo:

```bash
git clone https://github.com/your‑org/blue‑archive‑script‑converter.git
cd blue‑archive‑script‑converter
```

2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS  
.venv\Scripts\activate.bat     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the UI launcher:
```bash
python launcher.py
```