import csv
import os


def write_row_to_csv(file_path, header, row):
    with open(file_path, "a", newline="\n", encoding="utf8") as f:
        csv_writer = csv.DictWriter(f, header)
        if os.path.getsize(file_path) == 0:
            csv_writer.writeheader()
        csv_writer.writerow(row)
    print("Row add successfully.")


def get_language_code_by_chat_id(chat_id, file_path):
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        langs = [
            row.get("language_code")
            for row in csv_reader
            if int(row.get("id")) == chat_id
        ]
        if langs:
            return langs[-1]
        else:
            return "uz"


def is_exist_chat_id(chat_id):
    with open("students.csv") as f:
        csv_reader = csv.DictReader(f)
        return chat_id in [int(row.get("chat_id")) for row in csv_reader]


def get_fullname(first_name, last_name):
    return f"{first_name} {last_name}" if last_name else first_name


def reader_row_in_csv(file_path, chat_id):
    lst = []
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        for i in csv_reader:
            if i.get("chat_id") == str(chat_id):
                lst.append(f"{i.get('name')}")

    return lst
