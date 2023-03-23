#!/usr/bin/env python3
#
# Export the climbing routes from the website of the Orsay climbing club to a JSON file.

from functools import partial
from itertools import chain
import re
import sys

import requests
import bs4
import pandas as pd


URL = "http://escalade.orsay.free.fr/matos/Index_voies.php"


def get_flag(flag: str, string: str) -> bool:
    """Given a flag from a string, returns a boolean indicating whether the flag appears negated or not in it.
    It is tailored to the specific case of climbing routes descriptions written in French.

    :param flag: The flag to search for in the string.
    :param string: The string to search in.
    :return: A boolean indicating whether the flag appears negated or not in the string.
    """
    if flag not in string.lower():
        return False

    # 'droite' (resp. 'gauche') is sometimes abbreviated as 'D.' (resp 'G.')
    # the '.' prevents modifiers from being detected with their associated flag
    # only remove the '.' if it is NOT followed by a (space and) capital letter (as it may mark the end of a sentence)
    string = re.sub(r"\b(D|G)\b\.(?! [A-Z])", r"\1", string)

    # handle strings with parentheses
    for s in re.findall(r"\([^)]*\)", string):
        if flag in s.lower():
            return get_flag(flag, s[1:-1])

    string = re.sub(r"\([^)]*\)", "", string)

    modifiers = {
        'positive': {'avec'},
        'negative': {'sans', 'ni', 'pas d'},
        # when the flag is used to describe the location of something else
        'location': {'à'}
    }

    match = re.search(
        f"(?:.*)({'|'.join(chain(*modifiers.values()))})(?=[^.]*{flag})", 
        string, re.IGNORECASE
    )

    if match is None:
        return True

    exclude = chain.from_iterable(modifiers[key] for key in modifiers 
                                  if key != 'positive')
    return match.group(1).lower() not in exclude


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output filename>")
        exit(1)
    fname = sys.argv[1]

    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text, "lxml")

    table = soup.select_one("#matosTable > table")
    df = pd.read_html(str(table), header=0, parse_dates=['Date'])[0]

    df["Départ assis"] = df["Commentaire"].astype(
        str).apply(partial(get_flag, "départ assis"))
    df["Module"] = df["Commentaire"].astype(
        str).apply(partial(get_flag, "module"))
    df["Arête"] = df["Commentaire"].astype(
        str).apply(partial(get_flag, "arête"))
    df["Dièdre"] = df["Commentaire"].astype(
        str).apply(partial(get_flag, "dièdre"))

    # set encoding explicitly to avoid escaping unicode characters
    with open(fname, "w", encoding="utf-8") as file:
        df.to_json(file, orient="records", indent=4, force_ascii=False)
