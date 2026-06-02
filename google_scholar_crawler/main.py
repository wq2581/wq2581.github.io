"""Fetch Google Scholar statistics and write JSON files that the homepage
shields.io badges read (citations / h-index / i10-index).

The Scholar ID defaults to the value below, but can be overridden with the
``GOOGLE_SCHOLAR_ID`` repository secret / environment variable.
"""

import json
import os
from datetime import datetime

from scholarly import scholarly

# Google Scholar profile ID (the `user=` value in the profile URL).
SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID", "AJXeD2wAAAAJ")


def main() -> None:
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

    author["updated"] = str(datetime.now())
    author["publications"] = {p["author_pub_id"]: p for p in author["publications"]}

    os.makedirs("results", exist_ok=True)

    # Full dump – the homepage badges query $.citedby / $.hindex / $.i10index.
    with open("results/gs_data.json", "w", encoding="utf-8") as f:
        json.dump(author, f, ensure_ascii=False)

    # Endpoint badge for the citation count (shields.io schema).
    shieldsio = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author.get("citedby", 0)),
    }
    with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
        json.dump(shieldsio, f, ensure_ascii=False)

    print(
        "citedby={citedby}  h-index={hindex}  i10-index={i10index}".format(
            citedby=author.get("citedby"),
            hindex=author.get("hindex"),
            i10index=author.get("i10index"),
        )
    )


if __name__ == "__main__":
    main()
