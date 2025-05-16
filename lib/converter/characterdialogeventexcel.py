import json
from tqdm import tqdm
from typing import List
from collections import defaultdict, deque
from pydantic import BaseModel, Field

class CharacterDialogEventExcelConverter:
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

        # Build lookup of EN models by CostumeUniqueId
        old_lookup: dict[int, deque[CharacterDialogEventExcelEN]] = defaultdict(deque)
        for rec in en_data:
            gid = rec.get("CostumeUniqueId")
            if gid is None:
                continue
            model = CharacterDialogEventExcelEN.model_validate(rec)
            old_lookup[gid].append(model)

        # Iterate JP entries and merge matching EN text
        output_data_model: list[CharacterDialogEventExcelJP] = []
        for rec in jp_data:
            gid = rec.get("CostumeUniqueId")
            jp_model = CharacterDialogEventExcelJP.model_validate(rec)
            queue = old_lookup.get(gid)
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
        print("Successfully converted CharacterDialogEventExcel.json")

    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Build lookup of old models by CostumeUniqueId
        en_lookup: dict[int, deque[CharacterDialogEventExcelJP]] = defaultdict(deque)
        for rec in old_jp_data:
            gid = rec.get("CostumeUniqueId")
            if gid is None:
                continue
            model = CharacterDialogEventExcelJP.model_validate(rec)
            en_lookup[gid].append(model)

        # Iterate new entries and merge matching old text
        output_data_model: list[CharacterDialogEventExcelJP] = []
        for rec in new_jp_data:
            gid = rec.get("CostumeUniqueId")
            new_model = CharacterDialogEventExcelJP.model_validate(rec)
            queue = en_lookup.get(gid)
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
        print("Successfully converted CharacterDialogEventExcel.json")

class CharacterDialogEventExcelEN(BaseModel):
    costume_unique_id: int = Field(..., alias="CostumeUniqueId")
    original_character_id: int = Field(..., alias="OriginalCharacterId")
    display_order: int = Field(..., alias="DisplayOrder")
    event_id: int = Field(..., alias="EventID")
    production_step: str = Field(..., alias="ProductionStep")
    dialog_category: str = Field(..., alias="DialogCategory")
    dialog_condition: str = Field(..., alias="DialogCondition")
    dialog_condition_detail: str = Field(..., alias="DialogConditionDetail")
    dialog_condition_detail_value: int = Field(..., alias="DialogConditionDetailValue")
    group_id: int = Field(..., alias="GroupId")
    dialog_type: str = Field(..., alias="DialogType")
    action_name: str = Field(..., alias="ActionName")
    duration: int = Field(..., alias="Duration")
    duration_kr: int = Field(..., alias="DurationKr")
    animation_name: str = Field(..., alias="AnimationName")

    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")
    localize_th: str = Field(..., alias="LocalizeTH")
    localize_tw: str = Field(..., alias="LocalizeTW")
    localize_en: str = Field(..., alias="LocalizeEN")

    voice_id: List[int] = Field(default_factory=list, alias="VoiceId")
    collection_visible: bool = Field(..., alias="CollectionVisible")
    cv_collection_type: str = Field(..., alias="CVCollectionType")
    cv_unlock_scenario_type: str = Field(..., alias="CVUnlockScenarioType")
    unlock_event_season: int = Field(..., alias="UnlockEventSeason")
    scenario_group_id: int = Field(..., alias="ScenarioGroupId")
    localize_cv_group: str = Field(None, alias="LocalizeCVGroup")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class CharacterDialogEventExcelJP(BaseModel):
    costume_unique_id: int = Field(..., alias="CostumeUniqueId")
    original_character_id: int = Field(..., alias="OriginalCharacterId")
    display_order: int = Field(..., alias="DisplayOrder")
    event_id: int = Field(..., alias="EventID")
    production_step: str = Field(..., alias="ProductionStep")
    dialog_category: str = Field(..., alias="DialogCategory")
    dialog_condition: str = Field(..., alias="DialogCondition")
    dialog_condition_detail: str = Field(..., alias="DialogConditionDetail")
    dialog_condition_detail_value: int = Field(..., alias="DialogConditionDetailValue")
    group_id: int = Field(..., alias="GroupId")
    dialog_type: str = Field(..., alias="DialogType")
    action_name: str = Field(..., alias="ActionName")
    duration: int = Field(..., alias="Duration")
    animation_name: str = Field(..., alias="AnimationName")

    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")

    voice_id: List[int] = Field(default_factory=list, alias="VoiceId")
    collection_visible: bool = Field(..., alias="CollectionVisible")
    cv_collection_type: str = Field(..., alias="CVCollectionType")
    cv_unlock_scenario_type: str = Field(..., alias="CVUnlockScenarioType")
    unlock_event_season: int = Field(..., alias="UnlockEventSeason")
    scenario_group_id: int = Field(..., alias="ScenarioGroupId")
    localize_cv_group: str = Field(None, alias="LocalizeCVGroup")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
