import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class TutorialCharacterDialogExcelConverter:
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
        en_data_model: dict[int, TutorialCharacterDialogExcelEN] = {}
        for item_data in en_data:
            model = TutorialCharacterDialogExcelEN.model_validate(item_data)
            en_data_model[model.voice_id] = model

        # Convert to jp to english
        output_data_model = list[TutorialCharacterDialogExcelJP]()
        for item_data in jp_data:
            jp_model = TutorialCharacterDialogExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.voice_id)
            if en_model:
                jp_model.localize_jp = en_model.localize_en
            output_data_model.append(jp_model)

        serializable_data = [
                jp_rec.model_dump(by_alias=True)
                for jp_rec in output_data_model
            ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted TutorialCharacterDialogExcel.json")
    
    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile)
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile)

        # Mapping the old data
        old_data_model: dict[int, TutorialCharacterDialogExcelJP] = {}
        for item_data in old_jp_data:
            model = TutorialCharacterDialogExcelJP.model_validate(item_data)
            old_data_model[model.voice_id] = model

        # Convert to old to new
        output_data_model = list[TutorialCharacterDialogExcelJP]()
        for item_data in new_jp_data:
            new_model = TutorialCharacterDialogExcelJP.model_validate(item_data)
            old_model = old_data_model.get(new_model.voice_id)
            if old_model:
                new_model.localize_jp = old_model.localize_jp
            output_data_model.append(new_model)

        serializable_data = [
                jp_rec.model_dump(by_alias=True)
                for jp_rec in output_data_model
            ]
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(serializable_data, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted TutorialCharacterDialogExcel.json")

class TutorialCharacterDialogExcelEN(BaseModel):
    talk_id: int = Field(..., alias="TalkId")

    animation_name: str = Field(..., alias="AnimationName")
    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")
    localize_th: str = Field(..., alias="LocalizeTH")
    localize_tw: str = Field(..., alias="LocalizeTW")
    localize_en: str = Field(..., alias="LocalizeEN")

    voice_id: int = Field(..., alias="VoiceId")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class TutorialCharacterDialogExcelJP(BaseModel):
    talk_id: int = Field(..., alias="TalkId")

    animation_name: str = Field(..., alias="AnimationName")
    localize_kr: str = Field(..., alias="LocalizeKR")
    localize_jp: str = Field(..., alias="LocalizeJP")

    voice_id: int = Field(..., alias="VoiceId")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
