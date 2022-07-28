import os
import argparse
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore


def input_verification():
    url_start = "https://"
    print("Please, input url, saved tabs or 'exit'")
    input_command = str(input())
    if input_command == "exit":
        return {"type": "command", "value": "exit"}
    if input_command == "back":
        return {"type": "command", "value": "back"}
    if os.path.exists(os.path.join(path, input_command)):
        return {"type": "path", "value": os.path.join(path, input_command)}

    if input_command.count(".") == 0:
        print("Incorrect URL")
        return input_verification()

    if input_command.startswith(url_start):
        return {"type": "url", "value": input_command.strip()}
    else:
        return {"type": "url", "value": url_start + input_command.strip()}


def return_tabs_file_name(url_value):
    if url_value:
        if url_value.startswith("https://"):
            return url_value.replace("https://", "")[: url_value.replace("https://", "").index(".")]
        elif url_value.startswith("https://www."):
            return url_value.replace("https://www.", "")[: url_value.replace("https://www.", "").index(".")]


def save_tab(url, content, path_to_folder):
    f_name = return_tabs_file_name(url)
    path_to = os.path.join(path_to_folder, f_name)
    # if not os.path.exists(path_to):
    #     with open(path_to, "wt", encoding="utf-8") as file:
    #         file.write(content)
    with open(path_to, "wt", encoding="utf-8") as file:
        file.write(content)
    return path_to


def open_tabs(input_value):
    with open(input_value["value"], "rt", encoding="utf-8") as file:
        content = file.read()
        print(content)


def print_site_content(page):
    a_tags = page.find_all("a")
    for content in a_tags:
        content.string = "".join([Fore.BLUE, content.get_text(), Fore.RESET])

    return page


def open_url(input_value):
    r = requests.get(input_value["value"])

    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        content = print_site_content(soup).get_text()
        save_tab(input_value["value"], content, path)
        print(content)

    else:
        print(f"error - {r.status_code}.")


def program(input_v, visited_p, last_input=None):
    input_value = input_v

    while input_value["value"] != "exit":

        if input_value["type"] == "url":
            open_url(input_value)
            if last_input:
                visited_p.append({"type": "path", "value": os.path.join(path, return_tabs_file_name(last_input["value"]))})

        if input_value["type"] == "command" and input_value["value"] == "back":
            if len(visited_p) != 0:
                new_input = visited_p.pop()
                open_tabs(new_input)
                return program(input_verification(), visited_p, last_input)

        if input_value["type"] == "path":
            open_tabs(input_value)
            return program(input_verification(), visited_p, last_input)

        last_input = input_value
        return program(input_verification(), visited_p, last_input)


parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?", default=None)
args = parser.parse_args()
path = args.path


if not os.path.exists(path):
    # print("path is not exist")
    os.mkdir(path)
else:
    print("path is exist")

visited_pages = deque()
value = input_verification()

program(value, visited_pages)
