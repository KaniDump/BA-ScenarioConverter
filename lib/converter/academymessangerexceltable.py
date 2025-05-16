import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class AcademyMessangerExcelTableConverter:
    def __init__(self, reference_path, source_path, output_path):
        self.reference_path: str = reference_path
        self.source_path: str = source_path
        self.output_path: str = output_path
    
    def en_to_jp_convert(self):
        en_data = {}
        jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            en_data = json.load(infile).get("DataList")
        with open(self.source_path, "r", encoding="utf-8") as infile:
            jp_data = json.load(infile).get("DataList")

        # Mapping the old data
        en_data_model: dict[int, AcademyMessangerExcelTableEN] = {}
        for item_data in en_data:
            model = AcademyMessangerExcelTableEN.model_validate(item_data)
            en_data_model[model.id] = model

        # Convert to old to new
        output_data_model = list[AcademyMessangerExcelTableJP]()
        for item_data in jp_data:
            jp_model = AcademyMessangerExcelTableJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.id)
            if en_model:
                jp_model.message_jp = en_model.message_en
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        datalist = {"DataList": serializable_data}
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(datalist, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted AcademyMessangerExcelTable.json")

    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile).get("DataList")
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile).get("DataList")

        # Mapping the english data
        old_jp_data_model: dict[int, AcademyMessangerExcelTableJP] = {}
        for item_data in old_jp_data:
            model = AcademyMessangerExcelTableJP.model_validate(item_data)
            old_jp_data_model[model.id] = model

        # Convert to jp to english
        output_data_model = list[AcademyMessangerExcelTableJP]()
        for item_data in new_jp_data:
            new_jp_model = AcademyMessangerExcelTableJP.model_validate(item_data)
            old_jp_model = old_jp_data_model.get(new_jp_model.id)
            if old_jp_model:
                new_jp_model.message_jp = old_jp_model.message_jp
            output_data_model.append(new_jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        datalist = {"DataList": serializable_data}
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(datalist, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted AcademyMessangerExcelTable.json")

class AcademyMessangerExcelTableEN(BaseModel):
    message_group_id: int = Field(..., alias="MessageGroupId")
    id: int = Field(..., alias="Id")
    character_id: int = Field(..., alias="CharacterId")

    message_condition: str = Field(..., alias="MessageCondition")

    condition_value: int = Field(..., alias="ConditionValue")
    precondintion_group_id: int = Field(..., alias="PreConditionGroupId")
    precondintion_favor_schedule_id: int = Field(..., alias="PreConditionFavorScheduleId")
    favor_schedule_id: int = Field(..., alias="FavorScheduleId")
    next_group_id: int = Field(..., alias="NextGroupId")
    feedback_time: int = Field(..., alias="FeedbackTimeMillisec")

    message_type: str = Field(..., alias="MessageType")
    image_path: str = Field(..., alias="ImagePath")
    message_kr: str = Field(..., alias="MessageKR")
    message_jp: str = Field(..., alias="MessageJP")
    message_th: str = Field(..., alias="MessageTH")
    message_tw: str = Field(..., alias="MessageTW")
    message_en: str = Field(..., alias="MessageEN")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class AcademyMessangerExcelTableJP(BaseModel):
    message_group_id: int = Field(..., alias="MessageGroupId")
    id: int = Field(..., alias="Id")
    character_id: int = Field(..., alias="CharacterId")

    message_condition: str = Field(..., alias="MessageCondition")

    condition_value: int = Field(..., alias="ConditionValue")
    precondintion_group_id: int = Field(..., alias="PreConditionGroupId")
    precondintion_favor_schedule_id: int = Field(..., alias="PreConditionFavorScheduleId")
    favor_schedule_id: int = Field(..., alias="FavorScheduleId")
    next_group_id: int = Field(..., alias="NextGroupId")
    feedback_time: int = Field(..., alias="FeedbackTimeMillisec")

    message_type: str = Field(..., alias="MessageType")
    image_path: str = Field(..., alias="ImagePath")
    message_kr: str = Field(..., alias="MessageKR")
    message_jp: str = Field(..., alias="MessageJP")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
