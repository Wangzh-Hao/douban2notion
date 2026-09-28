import os
import shutil
import time


def move_and_rename_file(media_type):
    source_path = os.path.join("./OUT_FOLDER", "notion.svg")
    artifact_root = os.getenv(
        "NOTIONHUB_ARTIFACT_ROOT",
        os.path.abspath("OUT_FOLDER"),
    )
    target_dir = os.path.join(artifact_root, media_type)
    os.makedirs(target_dir, exist_ok=True)
    filename = f"{int(time.time())}.svg"
    shutil.move(source_path, os.path.join(target_dir, filename))
    return filename


def is_heatmap_embed_url(url, media_type):
    """Recognize legacy, broken-transition, and current heatmap embeds."""
    if "heatmap" in url:
        return True
    if not url.startswith("https://raw.githubusercontent.com/"):
        return False
    return f"/.notionhub-artifacts/douban/{media_type}/" in url


def build_heatmap_url(repository, media_type, filename):
    branch = os.getenv("ARTIFACT_BRANCH", "heatmap-artifacts")
    relative_root = os.getenv(
        "NOTIONHUB_ARTIFACT_PATH",
        "OUT_FOLDER",
    ).strip("/")
    return (
        f"https://raw.githubusercontent.com/{repository}/{branch}/"
        f"{relative_root}/{media_type}/{filename}"
    )
