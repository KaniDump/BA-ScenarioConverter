# Blue Archive Scenario Script Converter
A desktop UI application to streamline localization workflows for Blue Archive scenario scripts. The converter supports:

- EN → JP: Overwrite Japanese script fields with English translations.
- JP → JP: Migrate old-format Japanese scripts to a new and updated data.

Only Compatible with 1.82 Global and 1.61 Japan.

## 🚀 Features
- One‑click conversion of individual JSON files.
- Batch processing: select an entire folder and convert every supported Excel‑exported JSON.
- Wide coverage: handles scenario scripts plus dozens of other localization tables (dialogs, skills, gacha shop, character profiles, etc.).
- Data‑safe: preserves untranslated fields; skips entries when no translation is present.

## 💾 Supported Excel:
- LocalizeCharProfileExcelTable
- LocalizeErrorExcel
- LocalizeEtcExcel
- LocalizeExcel
- LocalizeSkillExcel
- LocalizeGachaShopExcel
- TutorialCharacterDialogExcel
- AcademyMessangerExcel
- CharacterDialogFieldExcelTable
- CharacterDialogEventExcel
- CharacterDialogExcel
- CharacterDialogSubtitleExcel
- CharacterVoiceSubtitleExcel
- ScenarioCharacterNameExcel
- ScenarioScriptExcel
  
## 📦 Installation
- Go to the [releases page](https://github.com/ArkanDash/BA-ScenarioConverter/releases/) and download the latest version for your platform.

## 🛠 Building
1. Clone the repo:

```bash
git clone https://github.com/ArkanDash/BA-ScenarioConverter.git
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

4. Build/Run the application:
    - Run the application:
        ```bash
        python main.py
        ```

    - Build the executable:
        ```bash
        pyinstaller --onefile --name BA-ScenarioConverter main.py
        ```