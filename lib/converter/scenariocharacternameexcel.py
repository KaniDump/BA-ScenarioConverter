import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class ScenarioCharacterNameExcelConverter:
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

        # Mapping the english data
        en_data_model: dict[int, ScenarioCharacterNameExcelEN] = {}
        for item_data in en_data:
            model = ScenarioCharacterNameExcelEN.model_validate(item_data)
            en_data_model[model.character_name] = model

        # Convert to jp to english
        output_data_model = list[ScenarioCharacterNameExcelJP]()
        fields = [
            ("name_en", "name_jp"),
            ("nickname_en", "nickname_jp"),
        ]
        for item_data in jp_data:
            jp_model = ScenarioCharacterNameExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.character_name)
            for en_attr, jp_attr in fields:
                if (val := getattr(en_model, en_attr, None)):
                    setattr(jp_model, jp_attr, val)
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted ScenarioCharacterNameExcel.json")
    
    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Mapping the old data
        en_data_model: dict[int, ScenarioCharacterNameExcelJP] = {}
        for item_data in old_jp_data:
            model = ScenarioCharacterNameExcelJP.model_validate(item_data)
            en_data_model[model.character_name] = model

        # Convert to old to new
        output_data_model = list[ScenarioCharacterNameExcelJP]()
        fields = [
            ("name_jp", "name_jp"),
            ("nickname_jp", "nickname_jp"),
        ]
        for item_data in new_jp_data:
            new_model = ScenarioCharacterNameExcelJP.model_validate(item_data)
            old_model = en_data_model.get(new_model.character_name)
            for old_attr, new_attr in fields:
                if (val := getattr(old_model, old_attr, None)):
                    setattr(new_model, new_attr, val)
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted ScenarioCharacterNameExcel.json")

class ScenarioCharacterNameExcelEN(BaseModel):
    character_name: int = Field(..., alias="CharacterName")
    production_step: str = Field(..., alias="ProductionStep")

    name_kr: str = Field(..., alias="NameKR")
    nickname_kr: str = Field(..., alias="NicknameKR")

    name_jp: str = Field(..., alias="NameJP")
    nickname_jp: str = Field(..., alias="NicknameJP")

    name_th: str = Field(..., alias="NameTH")
    nickname_th: str = Field(..., alias="NicknameTH")

    name_tw: str = Field(..., alias="NameTW")
    nickname_tw: str = Field(..., alias="NicknameTW")

    name_en: str = Field(..., alias="NameEN")
    nickname_en: str = Field(..., alias="NicknameEN")

    shape: str = Field(..., alias="Shape")
    spine_prefab_name: str = Field(..., alias="SpinePrefabName")
    small_portrait: str = Field(..., alias="SmallPortrait")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class ScenarioCharacterNameExcelJP(BaseModel):
    character_name: int = Field(..., alias="CharacterName")
    production_step: str = Field(..., alias="ProductionStep")

    name_kr: str = Field(..., alias="NameKR")
    nickname_kr: str = Field(..., alias="NicknameKR")

    name_jp: str = Field(..., alias="NameJP")
    nickname_jp: str = Field(..., alias="NicknameJP")

    shape: str = Field(..., alias="Shape")
    spine_prefab_name: str = Field(..., alias="SpinePrefabName")
    small_portrait: str = Field(..., alias="SmallPortrait")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
