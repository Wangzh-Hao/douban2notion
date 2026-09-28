import argparse
import os
from douban2notion.notion_helper import NotionHelper
from douban2notion.heatmap_utils import build_heatmap_url, move_and_rename_file
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    options = parser.parse_args()
    type = options.type
    if type not in {"movie", "book"}:
        raise ValueError("免费版只支持 movie 和 book 热力图")
    notion_helper = NotionHelper(type)
    filename = move_and_rename_file(type)
    if filename:
        repository = os.environ["REPOSITORY"]
        heatmap_url = build_heatmap_url(repository, type, filename)
        if notion_helper.heatmap_block_id:
            notion_helper.update_heatmap(
                block_id=notion_helper.heatmap_block_id, url=heatmap_url
            )
if __name__ == "__main__":
    main()
