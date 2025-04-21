import os
import re
import csv
import random
import time
import pdfplumber as plm


def get_comp_year(metadata):
    """
    Args:
        metadata (string): String value of metadata for a given key.

    Returns:
        Competition year if exists.
    """
    match = re.search(r"\b\d{4}\b", metadata)

    if match:
        comp_year = match.group()
        return comp_year
    else:
        return None


def convert_location(location):
    """
    Args:
        location (string): Location of competition.

    Returns:
        Reformated location of compeition.
    """
    if location in ["michigan", "mi"]:
        return "mi"
    elif location in ["lincoln", "ne"]:
        return "ne"
    else:
        return "north"


def get_comp_location(metadata):
    """
    Args:
        metadata (string): String value of metadata for a given key.

    Returns:
        Competition location if exists.
    """
    match = re.search(r"michigan|lincoln|north|mi|canada|ne", metadata.lower())

    if match:
        comp_location = convert_location(match.group())
        return comp_location
    else:
        return None


def get_comp_metadata(pdf):
    """
    Args:
        pdf (PDF): PDF object from pdfplumber.

    Returns:
        Metadata from competition.

    EX:
        fase_location_year_type
    """
    keys = ["Title", "Subject", "Keywords"]
    metadata = pdf.metadata

    comp_year = None
    comp_type = None
    comp_location = None

    for key in keys:
        if key in pdf.metadata:
            if comp_year is None:
                comp_year = get_comp_year(metadata[key])
            if comp_type is None:
                if re.search(r"electric|ev", metadata[key].lower()):
                    comp_type = "ev"
            if comp_location is None:
                comp_location = get_comp_location(metadata[key])
            if (
                comp_year is not None
                and comp_type is not None
                and comp_location is not None
            ):
                break
    if comp_type is None:
        comp_type = "ice"
    if comp_year is None:
        comp_year = "null"
    if comp_location is None:
        comp_location = "null"

    pdf.close()
    return f"fsae_{comp_location}_{comp_year}_{comp_type}"


def get_event_page_range(pdf):
    """
    Args:
        pdf (PDF): PDF object from pdfplumber.

    Returns:
        events (Dict): Dictionary of events for given competition
        with corresponding page range. Each key in dictionary is an
        event. Each value in dictionary is the final page containing data
        for repsective event.

    EX:
        events["Overall"] = 3, meaning page 1-3 contains overall results.
    """
    pages = pdf.pages
    events = {}

    for page_number, page in enumerate(pages, start=1):
        words = page.extract_words()
        for i, word in enumerate(words):
            if word["text"].lower() == "results" and i > 0:
                if words[i - 1]["text"].lower() == "event":
                    event = words[i - 2]["text"]
                    events[event] = page_number
                    break
                else:
                    event = words[i - 1]["text"]
                    events[event] = page_number
                    break
            elif (
                word["text"].lower() == "information"
                and words[i - 1]["text"].lower() == "team"
                and i > 0
            ):
                event = words[i - 1]["text"]
                events[event] = page_number
                break
            elif (
                word["text"].lower() == "score"
                and words[i - 1]["text"].lower() == "laps"
                and i > 0
            ):
                event = f"{words[i - 2]["text"]} {word["text"]}"
                events[event] = page_number
                break
            elif (
                word["text"].lower() == "laptimes"
                and words[i - 2]["text"].lower() == "endurance"
                and i > 0
            ):
                event = f"{words[i - 2]["text"]} {word["text"]}"
                events[event] = page_number
                break
    pdf.close()
    return events


def write_csv(pdf):
    event_list = get_event_page_range(pdf)
    start_page = 0

    for event, end_page in event_list.items():
        curr_page = start_page

        while curr_page < end_page and curr_page < len(pdf.pages):
            page_index = curr_page
            tables = pdf.pages[page_index].extract_tables()
            for table in tables:
                for row in table:
                    row.append(event)
            curr_page += 1

        start_page = end_page

    pdf.close()


pdf = plm.open("pdf/fsae_2024_results.pdf")

write_csv(pdf)
