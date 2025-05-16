import json
from tqdm import tqdm
from pydantic import BaseModel, Field

class LocalizeCharProfileExcelConverter:
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
        en_data_model: dict[int, LocalizeCharProfileExcelEN] = {}
        for item_data in en_data:
            model = LocalizeCharProfileExcelEN.model_validate(item_data)
            en_data_model[model.character_id] = model

        # Convert to jp to english
        output_data_model = list[LocalizeCharProfileExcelJP]()
        fields = [
            ("status_message_en", "status_message_jp"),
            ("full_name_en", "full_name_jp"),
            ("family_name_en", "family_name_jp"),
            ("family_name_ruby_en", "family_name_ruby_jp"),
            ("personal_name_en", "personal_name_jp"),
            ("personal_name_ruby_en", "personal_name_ruby_jp"),
            ("school_year_en", "school_year_jp"),
            ("character_age_en", "character_age_jp"),
            ("birthday_en", "birthday_jp"),
            ("hobby_en", "hobby_jp"),
            ("weapon_name_en", "weapon_name_jp"),
            ("weapon_desc_en", "weapon_desc_jp"),
            ("profile_introduction_en", "profile_introduction_jp"),
            ("character_ssr_new_en", "character_ssr_new_jp"),
        ]
        for item_data in jp_data:
            jp_model = LocalizeCharProfileExcelJP.model_validate(item_data)
            en_model = en_data_model.get(jp_model.character_id)
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
        print("Successfully converted LocalizeCharProfileExcel.json")

    def jp_to_jp_convert(self):
        old_jp_data = {}
        new_jp_data = {}

        # Read JSON files
        with open(self.reference_path, "r", encoding="utf-8") as infile:
            old_jp_data = json.load(infile).get("DataList")
        with open(self.source_path, "r", encoding="utf-8") as infile:
            new_jp_data = json.load(infile).get("DataList")

        # Mapping the old data
        old_jp_data: dict[int, LocalizeCharProfileExcelJP] = {}
        for item_data in old_jp_data:
            model = LocalizeCharProfileExcelJP.model_validate(item_data)
            old_jp_data[model.character_id] = model

        # Convert to old to new
        output_data_model = list[LocalizeCharProfileExcelJP]()
        fields = [
            ("status_message_jp", "status_message_jp"),
            ("full_name_jp", "full_name_jp"),
            ("family_name_jp", "family_name_jp"),
            ("family_name_ruby_jp", "family_name_ruby_jp"),
            ("personal_name_jp", "personal_name_jp"),
            ("personal_name_ruby_jp", "personal_name_ruby_jp"),
            ("school_year_jp", "school_year_jp"),
            ("character_age_jp", "character_age_jp"),
            ("birthday_jp", "birthday_jp"),
            ("hobby_jp", "hobby_jp"),
            ("weapon_name_jp", "weapon_name_jp"),
            ("weapon_desc_jp", "weapon_desc_jp"),
            ("profile_introduction_jp", "profile_introduction_jp"),
            ("character_ssr_new_jp", "character_ssr_new_jp"),
        ]
        for item_data in new_jp_data:
            new_model = LocalizeCharProfileExcelJP.model_validate(item_data)
            old_model = old_jp_data.get(new_model.character_id)
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
        print("Successfully converted LocalizeCharProfileExcel.json")

class LocalizeCharProfileExcelEN(BaseModel):
    character_id: int = Field(..., alias="CharacterId")

    status_message_kr: str = Field(..., alias="StatusMessageKr")
    status_message_jp: str = Field(..., alias="StatusMessageJp")
    status_message_th: str = Field(..., alias="StatusMessageTh")
    status_message_tw: str = Field(..., alias="StatusMessageTw")
    status_message_en: str = Field(..., alias="StatusMessageEn")

    full_name_kr: str = Field(..., alias="FullNameKr")
    full_name_jp: str = Field(..., alias="FullNameJp")
    full_name_th: str = Field(..., alias="FullNameTh")
    full_name_tw: str = Field(..., alias="FullNameTw")
    full_name_en: str = Field(..., alias="FullNameEn")

    family_name_kr: str = Field(..., alias="FamilyNameKr")
    family_name_ruby_kr: str = Field(..., alias="FamilyNameRubyKr")
    personal_name_kr: str = Field(..., alias="PersonalNameKr")
    personal_name_ruby_kr: str = Field(..., alias="PersonalNameRubyKr")

    family_name_jp: str = Field(..., alias="FamilyNameJp")
    family_name_ruby_jp: str = Field(..., alias="FamilyNameRubyJp")
    personal_name_jp: str = Field(..., alias="PersonalNameJp")
    personal_name_ruby_jp: str = Field(..., alias="PersonalNameRubyJp")

    family_name_th: str = Field(..., alias="FamilyNameTh")
    family_name_ruby_th: str = Field(..., alias="FamilyNameRubyTh")
    personal_name_th: str = Field(..., alias="PersonalNameTh")
    personal_name_ruby_th: str = Field(..., alias="PersonalNameRubyTh")

    family_name_tw: str = Field(..., alias="FamilyNameTw")
    family_name_ruby_tw: str = Field(..., alias="FamilyNameRubyTw")
    personal_name_tw: str = Field(..., alias="PersonalNameTw")
    personal_name_ruby_tw: str = Field(..., alias="PersonalNameRubyTw")

    family_name_en: str = Field(..., alias="FamilyNameEn")
    family_name_ruby_en: str = Field(..., alias="FamilyNameRubyEn")
    personal_name_en: str = Field(..., alias="PersonalNameEn")
    personal_name_ruby_en: str = Field(..., alias="PersonalNameRubyEn")

    school_year_kr: str = Field(..., alias="SchoolYearKr")
    school_year_jp: str = Field(..., alias="SchoolYearJp")
    school_year_th: str = Field(..., alias="SchoolYearTh")
    school_year_tw: str = Field(..., alias="SchoolYearTw")
    school_year_en: str = Field(..., alias="SchoolYearEn")

    character_age_kr: str = Field(..., alias="CharacterAgeKr")
    character_age_jp: str = Field(..., alias="CharacterAgeJp")
    character_age_th: str = Field(..., alias="CharacterAgeTh")
    character_age_tw: str = Field(..., alias="CharacterAgeTw")
    character_age_en: str = Field(..., alias="CharacterAgeEn")

    birthday: str = Field(..., alias="BirthDay")
    birthday_kr: str = Field(..., alias="BirthdayKr")
    birthday_jp: str = Field(..., alias="BirthdayJp")
    birthday_th: str = Field(..., alias="BirthdayTh")
    birthday_tw: str = Field(..., alias="BirthdayTw")
    birthday_en: str = Field(..., alias="BirthdayEn")

    char_height_kr: str = Field(..., alias="CharHeightKr")
    char_height_jp: str = Field(..., alias="CharHeightJp")
    char_height_th: str = Field(..., alias="CharHeightTh")
    char_height_tw: str = Field(..., alias="CharHeightTw")
    char_height_en: str = Field(..., alias="CharHeightEn")

    designer_name_kr: str = Field(..., alias="DesignerNameKr")
    designer_name_jp: str = Field(..., alias="DesignerNameJp")
    designer_name_th: str = Field(..., alias="DesignerNameTh")
    designer_name_tw: str = Field(..., alias="DesignerNameTw")
    designer_name_en: str = Field(..., alias="DesignerNameEn")

    illustrator_name_kr: str = Field(..., alias="IllustratorNameKr")
    illustrator_name_jp: str = Field(..., alias="IllustratorNameJp")
    illustrator_name_th: str = Field(..., alias="IllustratorNameTh")
    illustrator_name_tw: str = Field(..., alias="IllustratorNameTw")
    illustrator_name_en: str = Field(..., alias="IllustratorNameEn")

    character_voice_kr: str = Field(..., alias="CharacterVoiceKr")
    character_voice_jp: str = Field(..., alias="CharacterVoiceJp")
    character_voice_th: str = Field(..., alias="CharacterVoiceTh")
    character_voice_tw: str = Field(..., alias="CharacterVoiceTw")
    character_voice_en: str = Field(..., alias="CharacterVoiceEn")

    kr_character_voice_kr: str = Field(..., alias="KRCharacterVoiceKr")
    kr_character_voice_th: str = Field(..., alias="KRCharacterVoiceTh")
    kr_character_voice_tw: str = Field(..., alias="KRCharacterVoiceTw")
    kr_character_voice_en: str = Field(..., alias="KRCharacterVoiceEn")

    hobby_kr: str = Field(..., alias="HobbyKr")
    hobby_jp: str = Field(..., alias="HobbyJp")
    hobby_th: str = Field(..., alias="HobbyTh")
    hobby_tw: str = Field(..., alias="HobbyTw")
    hobby_en: str = Field(..., alias="HobbyEn")

    weapon_name_kr: str = Field(..., alias="WeaponNameKr")
    weapon_desc_kr: str = Field(..., alias="WeaponDescKr")
    weapon_name_jp: str = Field(..., alias="WeaponNameJp")
    weapon_desc_jp: str = Field(..., alias="WeaponDescJp")
    weapon_name_th: str = Field(..., alias="WeaponNameTh")
    weapon_desc_th: str = Field(..., alias="WeaponDescTh")
    weapon_name_tw: str = Field(..., alias="WeaponNameTw")
    weapon_desc_tw: str = Field(..., alias="WeaponDescTw")
    weapon_name_en: str = Field(..., alias="WeaponNameEn")
    weapon_desc_en: str = Field(..., alias="WeaponDescEn")

    profile_introduction_kr: str = Field(..., alias="ProfileIntroductionKr")
    profile_introduction_jp: str = Field(..., alias="ProfileIntroductionJp")
    profile_introduction_th: str = Field(..., alias="ProfileIntroductionTh")
    profile_introduction_tw: str = Field(..., alias="ProfileIntroductionTw")
    profile_introduction_en: str = Field(..., alias="ProfileIntroductionEn")

    character_ssr_new_kr: str = Field(..., alias="CharacterSSRNewKr")
    character_ssr_new_jp: str = Field(..., alias="CharacterSSRNewJp")
    character_ssr_new_th: str = Field(..., alias="CharacterSSRNewTh")
    character_ssr_new_tw: str = Field(..., alias="CharacterSSRNewTw")
    character_ssr_new_en: str = Field(..., alias="CharacterSSRNewEn")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True

class LocalizeCharProfileExcelJP(BaseModel):
    character_id: int = Field(..., alias="CharacterId")

    status_message_kr: str = Field(..., alias="StatusMessageKr")
    status_message_jp: str = Field(..., alias="StatusMessageJp")

    full_name_kr: str = Field(..., alias="FullNameKr")
    full_name_jp: str = Field(..., alias="FullNameJp")

    family_name_kr: str = Field(..., alias="FamilyNameKr")
    family_name_ruby_kr: str = Field(..., alias="FamilyNameRubyKr")
    personal_name_kr: str = Field(..., alias="PersonalNameKr")
    personal_name_ruby_kr: str = Field(..., alias="PersonalNameRubyKr")

    family_name_jp: str = Field(..., alias="FamilyNameJp")
    family_name_ruby_jp: str = Field(..., alias="FamilyNameRubyJp")
    personal_name_jp: str = Field(..., alias="PersonalNameJp")
    personal_name_ruby_jp: str = Field(..., alias="PersonalNameRubyJp")

    school_year_kr: str = Field(..., alias="SchoolYearKr")
    school_year_jp: str = Field(..., alias="SchoolYearJp")

    character_age_kr: str = Field(..., alias="CharacterAgeKr")
    character_age_jp: str = Field(..., alias="CharacterAgeJp")

    birthday: str = Field(..., alias="BirthDay")
    birthday_kr: str = Field(..., alias="BirthdayKr")
    birthday_jp: str = Field(..., alias="BirthdayJp")

    char_height_kr: str = Field(..., alias="CharHeightKr")
    char_height_jp: str = Field(..., alias="CharHeightJp")

    designer_name_kr: str = Field(..., alias="DesignerNameKr")
    designer_name_jp: str = Field(..., alias="DesignerNameJp")

    illustrator_name_kr: str = Field(..., alias="IllustratorNameKr")
    illustrator_name_jp: str = Field(..., alias="IllustratorNameJp")

    character_voice_kr: str = Field(..., alias="CharacterVoiceKr")
    character_voice_jp: str = Field(..., alias="CharacterVoiceJp")

    hobby_kr: str = Field(..., alias="HobbyKr")
    hobby_jp: str = Field(..., alias="HobbyJp")

    weapon_name_kr: str = Field(..., alias="WeaponNameKr")
    weapon_desc_kr: str = Field(..., alias="WeaponDescKr")
    weapon_name_jp: str = Field(..., alias="WeaponNameJp")
    weapon_desc_jp: str = Field(..., alias="WeaponDescJp")

    profile_introduction_kr: str = Field(..., alias="ProfileIntroductionKr")
    profile_introduction_jp: str = Field(..., alias="ProfileIntroductionJp")

    character_ssr_new_kr: str = Field(..., alias="CharacterSSRNewKr")
    character_ssr_new_jp: str = Field(..., alias="CharacterSSRNewJp")

    class Config:
        validate_by_name = True
        str_strip_whitespace = True
        use_enum_values = True
