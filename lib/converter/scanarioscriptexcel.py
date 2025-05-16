import json
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict, deque
from pydantic import BaseModel, Field

class ScenarioScriptExcelConverter:
    def __init__(self, reference_path: Path, source_path: Path, output_path: Path):
        self.reference_path: Path = reference_path
        self.source_path: Path = source_path
        self.output_path: Path = output_path
    
    def en_to_jp_convert(self):
        en_data = {}
        jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            en_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            jp_data = json.load(infile)

        # Build lookup of EN models by GroupId
        en_lookup: dict[int, deque[ScenarioScriptExcelEN]] = defaultdict(deque)
        for rec in en_data:
            gid = rec.get("GroupId")
            if gid is None:
                continue
            model = ScenarioScriptExcelEN.model_validate(rec)
            en_lookup[gid].append(model)

        # Iterate JP entries and merge matching EN text
        output_data_model: list[ScenarioScriptExcelJP] = []
        for rec in jp_data:
            gid = rec.get("GroupId")
            jp_model = ScenarioScriptExcelJP.model_validate(rec)
            queue = en_lookup.get(gid)
            if queue:
                en_model = queue.popleft()
                if (txt := getattr(en_model, "text_en", None)):
                    jp_model.text_jp = txt
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted ScenarioScriptExcel.json")
    
    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Build lookup of old models by GroupId
        old_lookup: dict[int, deque[ScenarioScriptExcelJP]] = defaultdict(deque)
        for rec in old_jp_data:
            gid = rec.get("GroupId")
            if gid is None:
                continue
            model = ScenarioScriptExcelJP.model_validate(rec)
            old_lookup[gid].append(model)

        # Iterate new entries and merge matching old text
        output_data_model: list[ScenarioScriptExcelJP] = []
        for rec in new_jp_data:
            gid = rec.get("GroupId")
            new_model = ScenarioScriptExcelJP.model_validate(rec)
            queue = old_lookup.get(gid)
            if queue:
                old_model = queue.popleft()
                if (txt := getattr(old_model, "text_jp", None)):
                    new_model.text_jp = txt
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted ScenarioScriptExcel.json")

class ScenarioScriptExcelEN(BaseModel):
    group_id: int = Field(..., alias="GroupId")
    selection_group: int = Field(..., alias="SelectionGroup")
    bgm_id: int = Field(..., alias="BGMId")
    sound: str = Field(..., alias="Sound")
    transition: int = Field(..., alias="Transition")
    bg_name: int = Field(..., alias="BGName")
    bg_effect: int = Field(..., alias="BGEffect")
    popup_file_name: str = Field(..., alias="PopupFileName")
    script_kr: str = Field(..., alias="ScriptKr")
    text_jp: str = Field(..., alias="TextJp")
    text_th: str = Field(..., alias="TextTh")
    text_tw: str = Field(..., alias="TextTw")
    text_en: str = Field(..., alias="TextEn")
    voice_id: int = Field(..., alias="VoiceId")
    teen_mode: bool = Field(..., alias="TeenMode")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class ScenarioScriptExcelJP(BaseModel):
    group_id: int = Field(..., alias="GroupId")
    selection_group: int = Field(..., alias="SelectionGroup")
    bgm_id: int = Field(..., alias="BGMId")
    sound: str = Field(..., alias="Sound")
    transition: int = Field(..., alias="Transition")
    bg_name: int = Field(..., alias="BGName")
    bg_effect: int = Field(..., alias="BGEffect")
    popup_file_name: str = Field(..., alias="PopupFileName")
    script_kr: str = Field(..., alias="ScriptKr")
    text_jp: str = Field(..., alias="TextJp")
    voice_id: int = Field(..., alias="VoiceId")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True