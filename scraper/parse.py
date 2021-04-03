import json
import os
import re
from csv import DictWriter
from pathlib import Path

from lxml.html import fromstring
from tqdm import tqdm

MIN_CHARS = 2000

dir_name = "results"
output_dir = "parsed"


def clean(s):
    """
    Cleans given string from non-relevant information: links, punctuation, etc.
    :param s: raw string
    :return: cleaned string
    """
    s = re.sub(r"https\S+", " ", s)
    s = re.sub(r"^\s+|\n|\r|\t|\s+$", " ", s)
    s = re.sub(r"[^\w\s\d]", " ", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.lower().strip()


def parse_post(el):
    """
    Extracts data from lxml's html element object.
    :param el: lxml html element object
    """
    text_elements = el.xpath("//article//div[contains(@class, 'story-block story-block_type_text')]")
    text = " ".join(" ".join(t.xpath("./*/text()")) for t in text_elements)
    cleaned_text = clean(text)
    if len(cleaned_text) < MIN_CHARS:
        return None
    tags_elements = el.xpath("//article//div[contains(@class, 'story__tags')]/a")
    return {
        "id": el.attrib["data-story-id"],
        "data-story-long": el.attrib["data-story-long"],
        "rating": el.attrib.get("data-rating"),
        "meta-rating": el.attrib["data-meta-rating"],
        "author_id": el.attrib["data-author-id"],
        "comments": el.attrib["data-comments"],
        "ts": el.attrib["data-timestamp"],
        "author_name": el.xpath("//header//a[contains(@class, 'user__nick')]")[0].text_content().strip(),
        "title": el.xpath("//header//h2/a")[0].text_content().replace("\xc2\xa0", " ").replace("\xa0", " ").strip(),
        "tags": [te.text_content().strip() for te in tags_elements],
        "text": cleaned_text,
    }


def parse():
    """
    This function uses saved json files with raw posts data, parses it into json and saves into `save_dir_name` with
    corresponding name.
    """
    Path(output_dir).mkdir(exist_ok=True)
    files = os.listdir(dir_name)
    ids = set()  # Save ids in set in order to not allow duplicates in output file
    res = []
    for file in tqdm(files):
        with open(os.path.join(dir_name, file), "r", encoding="utf-8") as f:
            content = f.read()
        articles_raw = json.loads(content)
        for a in articles_raw:
            parsed = parse_post(fromstring(a))
            if parsed and parsed["id"] not in ids:
                ids.add(parsed["id"])
                res.append(parsed)
    with open(os.path.join(output_dir, "parsed.csv"), "w", encoding="utf-8") as output:
        writer = DictWriter(output, fieldnames=res[0].keys())
        writer.writeheader()
        writer.writerows(res)


if __name__ == "__main__":
    parse()
