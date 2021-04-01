import json
import os
import re
from pathlib import Path
from typing import List

from lxml.html import fromstring, tostring

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


def parse_post(element):
    """
    Extracts data from lxml's html element object.
    :param element: lxml html object
    """
    text_elements = element.xpath("//article//div[contains(@class, 'story-block story-block_type_text')]")
    text = " ".join(" ".join(t.xpath("./*/text()")) for t in text_elements)
    cleaned_text = clean(text)
    if len(cleaned_text) < MIN_CHARS:
        return None
    tags_elements = element.xpath("//article//div[contains(@class, 'story__tags')]/a")
    return {
        "id": element.attrib["data-story-id"],
        "data-story-long": element.attrib["data-story-long"],
        "rating": element.attrib.get("data-rating"),
        "meta-rating": element.attrib["data-meta-rating"],
        "author_id": element.attrib["data-author-id"],
        "comments": element.attrib["data-comments"],
        "ts": element.attrib["data-timestamp"],
        "author_name": element.xpath("//header//a[contains(@class, 'user__nick')]")[0].text_content().strip(),
        "title": element.xpath("//header//h2/a")[0].text_content().strip(),
        "tags": [te.text_content().strip() for te in tags_elements],
        "text": cleaned_text,
    }


def extract_articles(html: str) -> List[str]:
    """
    Extracts article tags which have data-author-id attribute. Articles without that tag are advertising posts which we
    are not interested in.
    :param html: content of html page as string
    :return: list of content of article tags as strings
    """
    tree = fromstring(html)
    articles = tree.xpath("//article[@data-author-id]")
    return [(tostring(a, encoding="unicode")) for a in articles]


def parse():
    """
    This function uses saved json files with raw posts data, parses it into json and saves into `save_dir_name` with
    corresponding name.
    """
    Path(output_dir).mkdir(exist_ok=True)
    files = os.listdir(dir_name)
    ids = set()
    res = []
    for file in files:
        with open(os.path.join(dir_name, file), "r", encoding="utf-8") as f:
            content = f.read()
        articles_raw = json.loads(content)
        for a in articles_raw:
            parsed = parse_post(fromstring(a))
            if parsed and parsed["id"] not in ids:
                ids.add(parsed["id"])
                res.append(parsed)
    with open(os.path.join(output_dir, "parsed.json"), "w") as output:
        output.write(json.dumps(res, sort_keys=True, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parse()
