import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class LocalizeGachaShopExcelConverter:
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

        # Mapping the english data
        en_data_model: dict[int, LocalizeGachaShopExcelEN] = {}
        for item_data in en_data:
            model = LocalizeGachaShopExcelEN.model_validate(item_data)
            en_data_model[model.gacha_shop_id] = model

        # Convert to jp to english
        output_data_model = list[LocalizeGachaShopExcelJP]()
        fields = [
            ("tab_name_en", "tab_name_jp"),
            ("title_name_en", "title_name_jp"),
            ("subtitle_en", "subtitle_jp"),
            ("gacha_description_en", "gacha_description_jp"),
        ]
        for item_data in jp_data:
            jp_model = LocalizeGachaShopExcelJP.model_validate(item_data)
            jp_id = jp_model.gacha_shop_id
            prefixed_id = int(f"900{jp_id}")
            candidates = [prefixed_id, jp_id]
            
            en_model = None
            for cid in candidates:
                candidate = en_data_model.get(cid)
                if candidate:
                    if any(getattr(candidate, en_attr) for en_attr, _ in fields):
                        en_model = candidate
                        break
            if en_model:
                for en_attr, jp_attr in fields:
                    if (val := getattr(en_model, en_attr, None)):
                        setattr(jp_model, jp_attr, val)
            output_data_model.append(jp_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        datalist = {"DataList": serializable_data}
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(datalist, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted LocalizeGachaShopExcel.json")

    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile).get("DataList")
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile).get("DataList")

        # Mapping the old data
        old_jp_data: dict[int, LocalizeGachaShopExcelJP] = {}
        for item_data in old_jp_data:
            model = LocalizeGachaShopExcelJP.model_validate(item_data)
            old_jp_data[model.gacha_shop_id] = model

        # Convert to old to new
        output_data_model = list[LocalizeGachaShopExcelJP]()
        fields = [
            ("tab_name_jp", "tab_name_jp"),
            ("title_name_jp", "title_name_jp"),
            ("subtitle_jp", "subtitle_jp"),
            ("gacha_description_jp", "gacha_description_jp"),
        ]
        for item_data in new_jp_data:
            new_model = LocalizeGachaShopExcelJP.model_validate(item_data)
            prefixed_id = int(f"900{new_model.gacha_shop_id}")
            candidates = [prefixed_id, new_model.gacha_shop_id]
            
            old_model = None
            for cid in candidates:
                candidate = old_jp_data.get(cid)
                if candidate:
                    if any(getattr(candidate, old_attr) for old_attr, _ in fields):
                        old_model = candidate
                        break
            if old_model:
                for old_attr, new_attr in fields:
                    if (val := getattr(old_model, old_attr, None)):
                        setattr(new_model, new_attr, val)
            output_data_model.append(new_model)

        serializable_data = [
            jp_rec.model_dump(by_alias=True)
            for jp_rec in output_data_model
        ]
        datalist = {"DataList": serializable_data}
        with open(self.output_path, "w", encoding="utf-8") as outfile:
            json.dump(datalist, outfile, ensure_ascii=False, indent=2)
        print("Successfully converted LocalizeGachaShopExcel.json")

class LocalizeGachaShopExcelEN(BaseModel):
    gacha_shop_id: int = Field(..., alias="GachaShopId")

    tab_name_kr: str = Field(..., alias="TabNameKr")
    tab_name_jp: str = Field(..., alias="TabNameJp")
    tab_name_th: str = Field(..., alias="TabNameTh")
    tab_name_tw: str = Field(..., alias="TabNameTw")
    tab_name_en: str = Field(..., alias="TabNameEn")

    title_name_kr: str = Field(..., alias="TitleNameKr")
    title_name_jp: str = Field(..., alias="TitleNameJp")
    title_name_th: str = Field(..., alias="TitleNameTh")
    title_name_tw: str = Field(..., alias="TitleNameTw")
    title_name_en: str = Field(..., alias="TitleNameEn")

    subtitle_kr: str = Field(..., alias="SubTitleKr")
    subtitle_jp: str = Field(..., alias="SubTitleJp")
    subtitle_th: str = Field(..., alias="SubTitleTh")
    subtitle_tw: str = Field(..., alias="SubTitleTw")
    subtitle_en: str = Field(..., alias="SubTitleEn")
    
    gacha_description_kr: str = Field(..., alias="GachaDescriptionKr")
    gacha_description_jp: str = Field(..., alias="GachaDescriptionJp")
    gacha_description_th: str = Field(..., alias="GachaDescriptionTh")
    gacha_description_tw: str = Field(..., alias="GachaDescriptionTw")
    gacha_description_en: str = Field(..., alias="GachaDescriptionEn")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class LocalizeGachaShopExcelJP(BaseModel):
    gacha_shop_id: int = Field(..., alias="GachaShopId")

    tab_name_kr: str = Field(..., alias="TabNameKr")
    tab_name_jp: str = Field(..., alias="TabNameJp")

    title_name_kr: str = Field(..., alias="TitleNameKr")
    title_name_jp: str = Field(..., alias="TitleNameJp")

    subtitle_kr: str = Field(..., alias="SubTitleKr")
    subtitle_jp: str = Field(..., alias="SubTitleJp")
    
    gacha_description_kr: str = Field(..., alias="GachaDescriptionKr")
    gacha_description_jp: str = Field(..., alias="GachaDescriptionJp")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
