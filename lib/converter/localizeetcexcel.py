from pydantic import BaseModel, Field
from lib.converter import excelhelper

class LocalizeEtcExcelConverter:
    def __init__(self, reference_path, source_path, output_path):
        self.reference_path: str = reference_path
        self.source_path: str = source_path
        self.output_path: str = output_path
    
    def en_to_jp_convert(self):
        # Read JSON files
        en_data = excelhelper.read_excelt_json(self.reference_path)
        jp_data = excelhelper.read_excelt_json(self.source_path)

        # Mapping the english data
        en_data_model: dict[int, LocalizeEtcExcelEN] = {}
        for item_data in en_data:
            model = LocalizeEtcExcelEN.model_validate(item_data)
            en_data_model[model.key] = model

        # Convert to jp to english
        output_data_model = list[LocalizeEtcExcelJP]()
        for item_data in jp_data:
            jp_model = LocalizeEtcExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.key)
            if en_model:
                jp_model.name_jp = en_model.name_en
                jp_model.description_jp = en_model.description_en
            output_data_model.append(jp_model)

        serializable_data = [
                jp_rec.model_dump(by_alias=True)
                for jp_rec in output_data_model
            ]
        excelhelper.write_excelt_json(self.output_path, serializable_data)
        print("Successfully converted LocalizeEtcExcel.json")
    
    def jp_to_jp_convert(self):
        # Read JSON files
        old_jp_data = excelhelper.read_excelt_json(self.reference_path)
        new_jp_data = excelhelper.read_excelt_json(self.source_path)

        # Mapping the old data
        old_jp_data_: dict[int, LocalizeEtcExcelJP] = {}
        for item_data in old_jp_data:
            model = LocalizeEtcExcelJP.model_validate(item_data)
            old_jp_data_[model.key] = model

        # Convert to old to new
        output_data_model = list[LocalizeEtcExcelJP]()
        for item_data in new_jp_data:
            new_model = LocalizeEtcExcelJP.model_validate(item_data)
            old_model = old_jp_data_.get(new_model.key)
            if old_model:
                new_model.name_jp = old_model.name_jp
                new_model.description_jp = old_model.description_jp
            output_data_model.append(new_model)

        serializable_data = [
                jp_rec.model_dump(by_alias=True)
                for jp_rec in output_data_model
            ]
        excelhelper.write_excelt_json(self.output_path, serializable_data)
        print("Successfully converted LocalizeEtcExcel.json")

class LocalizeEtcExcelEN(BaseModel):
    key: int = Field(..., alias="Key")

    name_kr: str = Field(..., alias="NameKr")
    description_kr: str = Field(..., alias="DescriptionKr")
    name_jp: str = Field(..., alias="NameJp")
    description_jp: str = Field(..., alias="DescriptionJp")
    name_th: str = Field(..., alias="NameTh")
    description_th: str = Field(..., alias="DescriptionTh")
    name_tw: str = Field(..., alias="NameTw")
    description_tw: str = Field(..., alias="DescriptionTw")
    name_en: str = Field(..., alias="NameEn")
    description_en: str = Field(..., alias="DescriptionEn")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class LocalizeEtcExcelJP(BaseModel):
    key: int = Field(..., alias="Key")

    name_kr: str = Field(..., alias="NameKr")
    description_kr: str = Field(..., alias="DescriptionKr")
    name_jp: str = Field(..., alias="NameJp")
    description_jp: str = Field(..., alias="DescriptionJp")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
