import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class LocalizeErrorExcelConverter:
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
        en_data_model: dict[int, LocalizeErrorExcelEN] = {}
        for item_data in en_data:
            model = LocalizeErrorExcelEN.model_validate(item_data)
            en_data_model[model.key] = model

        # Convert to jp to english
        output_data_model = list[LocalizeErrorExcelJP]()
        for item_data in jp_data:
            jp_model = LocalizeErrorExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.key)
            if en_model:
                jp_model.jp = en_model.en
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted LocalizeErrorExcel.json")
    
    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Mapping the old data
        old_jp_data: dict[int, LocalizeErrorExcelJP] = {}
        for item_data in old_jp_data:
            model = LocalizeErrorExcelJP.model_validate(item_data)
            old_jp_data[model.key] = model

        # Convert to old to new
        output_data_model = list[LocalizeErrorExcelJP]()
        for item_data in new_jp_data:
            new_model = LocalizeErrorExcelJP.model_validate(item_data)
            old_model = old_jp_data.get(new_model.key)
            if old_model:
                new_model.jp = old_model.jp
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted LocalizeErrorExcel.json")

class LocalizeErrorExcelEN(BaseModel):
    key: int = Field(..., alias="Key")
    error_level: str = Field(..., alias="ErrorLevel")

    kr: str = Field(..., alias="Kr")
    jp: str = Field(..., alias="Jp")
    th: str = Field(..., alias="Th")
    tw: str = Field(..., alias="Tw")
    en: str = Field(..., alias="En")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class LocalizeErrorExcelJP(BaseModel):
    key: int = Field(..., alias="Key")
    error_level: str = Field(..., alias="ErrorLevel")
    
    kr: str = Field(..., alias="Kr")
    jp: str = Field(..., alias="Jp")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
