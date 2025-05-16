import json
from tqdm import tqdm
from typing import List
from collections import defaultdict, deque
from pydantic import BaseModel, Field

class CharacterVoiceSubtitleExcelConverter:
    def __init__(self, reference_path, source_path, output_path):
        self.reference_path: str = reference_path
        self.source_path: str = source_path
        self.output_path: str = output_path
    
    def en_to_jp_convert(self):
        en_data = {}
        jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            en_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            jp_data = json.load(infile)

        # Build lookup of EN models by LocalizeCVGroup
        en_lookup: dict[int, deque[CharacterVoiceSubtitleExcelEN]] = defaultdict(deque)
        for rec in en_data:
            gid = rec.get("LocalizeCVGroup")
            if gid is None:
                continue
            model = CharacterVoiceSubtitleExcelEN.model_validate(rec)
            en_lookup[gid].append(model)

        # Iterate JP entries and merge matching EN text
        output_data_model: list[CharacterVoiceSubtitleExcelJP] = []
        for rec in jp_data:
            gid = rec.get("LocalizeCVGroup")
            jp_model = CharacterVoiceSubtitleExcelJP.model_validate(rec)
            queue = en_lookup.get(gid)
            if queue:
                en_model = queue.popleft()
                if (txt := getattr(en_model, "localize_en", None)):
                    jp_model.localize_jp = txt
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted CharacterVoiceSubtitleExcel.json")
    
    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Build lookup of new models by LocalizeCVGroup
        old_lookup: dict[int, deque[CharacterVoiceSubtitleExcelJP]] = defaultdict(deque)
        for rec in old_jp_data:
            gid = rec.get("LocalizeCVGroup")
            if gid is None:
                continue
            model = CharacterVoiceSubtitleExcelJP.model_validate(rec)
            old_lookup[gid].append(model)

        # Iterate new entries and merge matching old text
        output_data_model: list[CharacterVoiceSubtitleExcelJP] = []
        for rec in new_jp_data:
            gid = rec.get("LocalizeCVGroup")
            new_model = CharacterVoiceSubtitleExcelJP.model_validate(rec)
            queue = old_lookup.get(gid)
            if queue:
                old_model = queue.popleft()
                if (txt := getattr(old_model, "localize_jp", None)):
                    new_model.localize_jp = txt
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted CharacterVoiceSubtitleExcel.json")

class CharacterVoiceSubtitleExcelEN(BaseModel):
    localize_cv_group: str = Field(..., alias="LocalizeCVGroup")
    character_voice_group_id: int = Field(..., alias="CharacterVoiceGroupId")
    tlm_id: str = Field(..., alias="TLMID")
    duration: int = Field(..., alias="Duration")
    duration_kr: int = Field(..., alias="DurationKr")
    separate: bool = Field(..., alias="Separate")
    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")
    localize_th: str = Field(..., alias="LocalizeTH")
    localize_tw: str = Field(..., alias="LocalizeTW")
    localize_en: str = Field(..., alias="LocalizeEN")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class CharacterVoiceSubtitleExcelJP(BaseModel):
    localize_cv_group: str = Field(..., alias="LocalizeCVGroup")
    character_voice_group_id: int = Field(..., alias="CharacterVoiceGroupId")
    duration: int = Field(..., alias="Duration")
    separate: bool = Field(..., alias="Separate")
    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
