import os
from pathlib import Path
from lib.converter.localizecharprofileexceltable import LocalizeCharProfileExcelConverter
from lib.converter.localizeerrorexcel import LocalizeErrorExcelConverter
from lib.converter.localizeetcexcel import LocalizeEtcExcelConverter
from lib.converter.localizeexcel import LocalizeExcelConverter
from lib.converter.localizeskillexcel import LocalizeSkillExcelConverter
from lib.converter.localizegachashopexcel import LocalizeGachaShopExcelConverter
from lib.converter.tutorialcharacterdialogexcel import TutorialCharacterDialogExcelConverter
from lib.converter.academymessangerexceltable import AcademyMessangerExcelTableConverter
from lib.converter.characterdialogfieldexcelexcel import CharacterDialogFieldExcelConverter
from lib.converter.characterdialogeventexcel import CharacterDialogEventExcelConverter
from lib.converter.characterdialogexcel import CharacterDialogExcelConverter
from lib.converter.characterdialogsubtitleexcel import CharacterDialogSubtitleExcelConverter
from lib.converter.charactervoicesubtitleexcel import CharacterVoiceSubtitleExcelConverter
from lib.converter.scenariocharacternameexcel import ScenarioCharacterNameExcelConverter
from lib.converter.scanarioscriptexcel import ScenarioScriptExcelConverter

_CONVERTERS: dict[str, type] = {
    "AcademyMessanger1ExcelTable": AcademyMessangerExcelTableConverter,
    "AcademyMessanger2ExcelTable": AcademyMessangerExcelTableConverter,
    "AcademyMessanger3ExcelTable": AcademyMessangerExcelTableConverter,
    "AcademyMessanger4ExcelTable": AcademyMessangerExcelTableConverter,
    "AcademyMessangerExcelTable": AcademyMessangerExcelTableConverter,
    "CharacterDialogEventExcel": CharacterDialogEventExcelConverter,
    "CharacterDialogExcel": CharacterDialogExcelConverter,
    "CharacterDialogFieldExcelTable": CharacterDialogFieldExcelConverter,
    "CharacterDialogSubtitleExcel": CharacterDialogSubtitleExcelConverter,
    "CharacterVoiceSubtitleExcel": CharacterVoiceSubtitleExcelConverter,
    "LocalizeCharProfileExcelTable": LocalizeCharProfileExcelConverter,
    "LocalizeErrorExcel": LocalizeErrorExcelConverter,
    "LocalizeEtcExcel": LocalizeEtcExcelConverter,
    "LocalizeExcel": LocalizeExcelConverter,
    "LocalizeGachaShopExcel": LocalizeGachaShopExcelConverter, # jp
    "LocalizeGachaShopExcelTable": LocalizeGachaShopExcelConverter, # global
    "LocalizeSkillExcel": LocalizeSkillExcelConverter,
    "ScenarioCharacterNameExcel": ScenarioCharacterNameExcelConverter,
    "ScenarioScriptExcel": ScenarioScriptExcelConverter,
    "TutorialCharacterDialogExcel": TutorialCharacterDialogExcelConverter,
}

def en_to_jp_data_conversion(
        reference_file_path: Path,
        input_file_path: Path,
        output_file_path: Path
    ) -> bool:
    stem = reference_file_path.stem
    converter_cls = _CONVERTERS.get(stem)
    if not converter_cls:
        print(f"❌ No converter for {stem}")
        return False
    try:
        converter = converter_cls(reference_file_path, input_file_path, output_file_path)
        converter.en_to_jp_convert()
        return True
    except Exception as e:
        print(f"Error during EN to JP data conversion of '{reference_file_path}': {e}")
        return False
    
def jp_to_jp_data_conversion(
        reference_file_path: Path,
        input_file_path: Path,
        output_file_path: Path
    ) -> bool:
    stem = reference_file_path.stem
    converter_cls = _CONVERTERS.get(stem)
    if not converter_cls:
        print(f"❌ No converter for {stem}")
        return False
    try:
        converter = converter_cls(reference_file_path, input_file_path, output_file_path)
        converter.jp_to_jp_convert()
        return True
    except Exception as e:
        print(f"Error during JP to JP data conversion of '{reference_file_path}': {e}")
        return False

def convert_single_en_to_jp(filename: str, en_script_folder: str, jp_script_folder: str, output_folder: str) -> bool:
    """
    Converts a single EN script to JP.
    """
    print(f"Converting EN to JP: {filename}")
    reference_file_path = Path(en_script_folder) / filename
    source_file_path = Path(jp_script_folder) / filename
    output_file_path = Path(output_folder) / filename

    return en_to_jp_data_conversion(reference_file_path, source_file_path, output_file_path)
    # if reference_file_path.exists() and source_file_path.exists():
    #     return en_to_jp_data_conversion(reference_file_path, source_file_path, output_file_path)
    # else:
    #     print(f"Error: Source file {source_file_path} not found for EN to JP conversion.")
    #     return False

def convert_single_jp_to_jp(filename: str, old_jp_folder: str, new_jp_folder: str, output_folder: str) -> bool:
    """
    Converts a single JP script (old to new format/structure).
    """
    print(f"Converting JP to JP: {filename}")
    reference_file_path = Path(old_jp_folder) / filename
    source_file_path = Path(new_jp_folder) / filename
    output_file_path = Path(output_folder) / filename

    if reference_file_path.exists() and source_file_path.exists():
        return jp_to_jp_data_conversion(reference_file_path, source_file_path, output_file_path)
    else:
        print(f"Error: Source file {source_file_path} not found for JP to JP conversion.")
        return False

def ensure_dir_exists(dir_path: Path):
    """Ensures that a directory exists, creating it if necessary."""
    dir_path.mkdir(parents=True, exist_ok=True)