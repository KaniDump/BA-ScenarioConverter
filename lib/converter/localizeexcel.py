from pydantic import BaseModel, Field
from lib.converter import excelhelper

class LocalizeExcelConverter:
    def __init__(self, reference_path, source_path, output_path):
        self.reference_path: str = reference_path
        self.source_path: str = source_path
        self.output_path: str = output_path
    
    def en_to_jp_convert(self):
        # Read JSON files
        en_data = excelhelper.read_excelt_json(self.reference_path)
        jp_data = excelhelper.read_excelt_json(self.source_path)

        # Mapping the english data
        en_data_model: dict[int, LocalizeExcelEN] = {}
        for item_data in en_data:
            model = LocalizeExcelEN.model_validate(item_data)
            en_data_model[model.key] = model

        # Convert to jp to english
        output_data_model = list[LocalizeExcelJP]()
        for item_data in jp_data:
            jp_model = LocalizeExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.key)
            if en_model:
                jp_model.jp = en_model.en
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        excelhelper.write_excelt_json(self.output_path, serializable_data)
        print("Successfully converted LocalizeExcel.json")

    def jp_to_jp_convert(self):
        # Read JSON files
        old_jp_data = excelhelper.read_excelt_json(self.reference_path)
        new_jp_data = excelhelper.read_excelt_json(self.source_path)

        # Mapping the old data
        old_jp_data: dict[int, LocalizeExcelJP] = {}
        for item_data in old_jp_data:
            model = LocalizeExcelJP.model_validate(item_data)
            old_jp_data[model.key] = model

        # Convert to old to new
        output_data_model = list[LocalizeExcelJP]()
        for item_data in new_jp_data:
            new_model = LocalizeExcelJP.model_validate(item_data)
            old_model = old_jp_data.get(new_model.key)
            if old_model:
                new_model.jp = old_model.jp
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        excelhelper.write_excelt_json(self.output_path, serializable_data)  
        print("Successfully converted LocalizeExcel.json")

class LocalizeExcelEN(BaseModel):
    key: int = Field(..., alias="Key")

    kr: str = Field(..., alias="Kr")
    jp: str = Field(..., alias="Jp")
    th: str = Field(..., alias="Th")
    tw: str = Field(..., alias="Tw")
    en: str = Field(..., alias="En")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class LocalizeExcelJP(BaseModel):
    key: int = Field(..., alias="Key")

    kr: str = Field(..., alias="Kr")
    jp: str = Field(..., alias="Jp")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
