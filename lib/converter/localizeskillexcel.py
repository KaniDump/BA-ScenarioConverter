import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class LocalizeSkillExcelConverter:
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
        en_data_model: dict[int, LocalizeSkillExcelEN] = {}
        for item_data in en_data:
            model = LocalizeSkillExcelEN.model_validate(item_data)
            en_data_model[model.key] = model

        # Convert to jp to english
        output_data_model = list[LocalizeSkillExcelJP]()
        for item_data in jp_data:
            jp_model = LocalizeSkillExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.key)
            if en_model:
                jp_model.name_jp = en_model.name_en
                jp_model.description_jp = en_model.description_en
                jp_model.skill_invoke_localize_jp = en_model.skill_invoke_localize_en
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted LocalizeSkillExcel.json")
    
    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Mapping the old data
        old_jp_data: dict[int, LocalizeSkillExcelJP] = {}
        for item_data in old_jp_data:
            model = LocalizeSkillExcelJP.model_validate(item_data)
            old_jp_data[model.key] = model

        # Convert to old to new
        output_data_model = list[LocalizeSkillExcelJP]()
        for item_data in new_jp_data:
            new_model = LocalizeSkillExcelJP.model_validate(item_data)
            old_model = old_jp_data.get(new_model.key)
            if old_model:
                new_model.name_jp = old_model.name_jp
                new_model.description_jp = old_model.description_jp
                new_model.skill_invoke_localize_jp = old_model.skill_invoke_localize_jp
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted LocalizeSkillExcel.json")

class LocalizeSkillExcelEN(BaseModel):
    key: int = Field(..., alias="Key")

    name_kr: str = Field(..., alias="NameKr")
    description_kr: str = Field(..., alias="DescriptionKr")
    skill_invoke_localize_kr: str = Field(..., alias="SkillInvokeLocalizeKr")
    name_jp: str = Field(..., alias="NameJp")
    description_jp: str = Field(..., alias="DescriptionJp")
    skill_invoke_localize_jp: str = Field(..., alias="SkillInvokeLocalizeJp")
    name_th: str = Field(..., alias="NameTh")
    description_th: str = Field(..., alias="DescriptionTh")
    skill_invoke_localize_th: str = Field(..., alias="SkillInvokeLocalizeTh")
    name_tw: str = Field(..., alias="NameTw")
    description_tw: str = Field(..., alias="DescriptionTw")
    skill_invoke_localize_tw: str = Field(..., alias="SkillInvokeLocalizeTw")
    name_en: str = Field(..., alias="NameEn")
    description_en: str = Field(..., alias="DescriptionEn")
    skill_invoke_localize_en: str = Field(..., alias="SkillInvokeLocalizeEn")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class LocalizeSkillExcelJP(BaseModel):
    key: int = Field(..., alias="Key")

    name_kr: str = Field(..., alias="NameKr")
    description_kr: str = Field(..., alias="DescriptionKr")
    skill_invoke_localize_kr: str = Field(..., alias="SkillInvokeLocalizeKr")
    name_jp: str = Field(..., alias="NameJp")
    description_jp: str = Field(..., alias="DescriptionJp")
    skill_invoke_localize_jp: str = Field(..., alias="SkillInvokeLocalizeJp")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
