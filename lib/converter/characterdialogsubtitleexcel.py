from pydantic import BaseModel, Field
from lib.converter import excelhelper

class CharacterDialogSubtitleExcelConverter:
    def __init__(self, reference_path, source_path, output_path):
        self.reference_path: str = reference_path
        self.source_path: str = source_path
        self.output_path: str = output_path
    
    def en_to_jp_convert(self):
        # Read JSON files
        en_data = excelhelper.read_excelt_json(self.reference_path)
        jp_data = excelhelper.read_excelt_json(self.source_path)

        # Mapping the english data
        en_data_model: dict[int, CharacterDialogSubtitleExcelEN] = {}
        for item_data in en_data:
            model = CharacterDialogSubtitleExcelEN.model_validate(item_data)
            en_data_model[model.localize_cv_group] = model

        # Convert to jp to english
        output_data_model = list[CharacterDialogSubtitleExcelJP]()
        fields = [
            ("localize_en", "localize_jp"),
        ]
        for item_data in jp_data:
            jp_model = CharacterDialogSubtitleExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.localize_cv_group)
            for en_attr, jp_attr in fields:
                if (val := getattr(en_model, en_attr, None)):
                    setattr(jp_model, jp_attr, val)
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        excelhelper.write_excelt_json(self.output_path, serializable_data)
        print("Successfully converted CharacterDialogSubtitleExcel.json")
    
    def jp_to_jp_convert(self):
        # Read JSON files
        old_jp_data = excelhelper.read_excelt_json(self.reference_path)
        new_jp_data = excelhelper.read_excelt_json(self.source_path)

        # Mapping the old data
        jp_data_model: dict[int, CharacterDialogSubtitleExcelJP] = {}
        for item_data in old_jp_data:
            model = CharacterDialogSubtitleExcelJP.model_validate(item_data)
            jp_data_model[model.localize_cv_group] = model

        # Convert to old to new
        output_data_model = list[CharacterDialogSubtitleExcelJP]()
        fields = [
            ("localize_jp", "localize_jp"),
        ]
        for item_data in new_jp_data:
            new_model = CharacterDialogSubtitleExcelJP.model_validate(item_data)
            old_model = jp_data_model.get(new_model.localize_cv_group)
            for old_attr, new_attr in fields:
                if (val := getattr(old_model, old_attr, None)):
                    setattr(new_model, new_attr, val)
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        excelhelper.write_excelt_json(self.output_path, serializable_data)
        print("Successfully converted CharacterDialogSubtitleExcel.json")

class CharacterDialogSubtitleExcelEN(BaseModel):
    localize_cv_group: str = Field(..., alias="LocalizeCVGroup")
    character_id: int = Field(..., alias="CharacterId")
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

class CharacterDialogSubtitleExcelJP(BaseModel):
    localize_cv_group: str = Field(..., alias="LocalizeCVGroup")
    character_id: int = Field(..., alias="CharacterId")
    duration: int = Field(..., alias="Duration")
    separate: bool = Field(..., alias="Separate")
    
    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
