# Copyright (c) 2022 Praneeth Vadlapati

import os

from dotenv import load_dotenv
from IPython.display import display, Markdown
import pyperclip
import time
import random

def load_env():
    load_dotenv(override=True)  # bypass the cache and reload the variables
load_env()

data_folder = 'data_files'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)


def display_md(md_text):
    display(Markdown(md_text))

def print_progress(chr='.'):
    if chr == 0 and type(chr) == int:
        return
    if type(chr) == bool:
        chr = '.' if chr else ','
    print(chr, end='', flush=True)

def print_error(err=None, chr='!'):
    # print(err)
    print_progress(chr)

def extract_data(response, tag, absent_ok=False):
    if not tag:  # if tags are provided, extract data from tags
        raise Exception('No data format or tag provided to extract data from the response')
    response = str(response).strip()  # create a copy

    open_tag = f'<{tag}>'
    if open_tag not in response:
        if absent_ok:
            return response
        raise Exception(f'Tag "{tag}" not found in the response')
    start = response.rfind(open_tag) + len(open_tag)
    
    close_tag = f'</{tag}>'
    if close_tag in response[start:]:
        end = response.find(close_tag, start)
    else:
        end = len(response)
    response = response[start:end].strip()

    if '```csv' in response:
        response = response.replace('```csv', '```').strip()
    if '```' in response:
        response = response.split('```')[1].strip()
    return response


def get_lm_response(messages, max_retries=3):
    # Copy the last message to clipboard. Ask user to paste response using input()
    pyperclip.copy(messages[-1]['content'])
    print_progress('📋')  # indicate that the message is copied to clipboard
    print("Please paste the response from the language model and press Enter:")

    for attempt in range(max_retries):
        try:
            response = input()
            if response.strip() == "":
                raise ValueError("Empty response received.")
            return response
        except Exception as e:
            print_error(f"Error receiving input: {e}")
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    
    raise Exception("Failed to get a valid response after multiple attempts.")
