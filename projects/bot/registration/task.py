import csv


class Chat:
    def __init__(self, id, fullname, language_code):
        self.id = id
        self.fullname = fullname
        self.language_code = language_code

    def get_attrs_as_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "language_code": self.language_code
        }


class Task:
    def __init__(self, chat_id, name, created_at):
        self.chat_id = chat_id
        self.name = name
        self.created_at = created_at

    def get_attrs_as_dict(self):
        return {
            "chat_id": self.chat_id,
            "name": self.name,
            "created_at": self.created_at
        }


class Save:
    def __init__(self, full_name, phone, age, language, course):
        self.full_name = full_name
        self.phone = phone
        self.age = age
        self.language = language
        self.course = course

    def get_save_info_csv(self):

        # with open(file_path, "a", encoding="utf8", newline="\n") as f:

        return {
            "Fullname": self.full_name,
            "Phone": self.phone,
            "Age": self.age,
            "Language": self.language,
            "Course": self.course
        }
