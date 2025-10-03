import os
import re
import json
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
CHANGED_FILES = os.getenv("CHANGED_FILES", "")
COMMIT_MESSAGE = os.getenv("COMMIT_MESSAGE", "")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def extract_slug(path: str) -> str:
    filename = os.path.basename(path)
    dirname = os.path.basename(os.path.dirname(path))
    candidate = dirname if dirname and dirname != "." else os.path.splitext(filename)[0]

    candidate = re.sub(r"^\d+[\.\-_\s]*", "", candidate)
    slug = candidate.lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug

def title_from_slug(slug: str) -> str:
    small = {"a","an","the","of","and","to","in","on","for","with","by","or"}
    words = slug.split("-")
    titled = []
    for i, w in enumerate(words):
        if i > 0 and w in small:
            titled.append(w)
        else:
            titled.append(w.capitalize())
    return " ".join(titled)

def parse_commit_message():
    pattern = r"\[LeetHub\]\s+(.*?)\s+\|\s+Difficulty:\s+(\w+)\s+\|\s+Tags:\s+(.*)"
    match = re.search(pattern, COMMIT_MESSAGE)
    if match:
        title = match.group(1).strip()
        difficulty = match.group(2).strip()
        tags = match.group(3).strip()
        return title, difficulty, tags
    else:
        return None, None, None

def notion_query_by_slug(slug: str):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Slug",
            "rich_text": {"equals": slug}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    data = res.json()
    return data.get("results", [])

def notion_update_page(page_id: str, difficulty: str, tags: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Solved": {"checkbox": True},
            "Difficulty": {"select": {"name": difficulty}},
            "Type": {"multi_select": [{"name": tag.strip()} for tag in tags.split(",")]}
        }
    }
    res = requests.patch(url, headers=headers, json=payload)
    res.raise_for_status()

def notion_create_page(slug: str, title: str, difficulty: str, tags: str):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Problem": {"title": [{"text": {"content": title}}]},
            "Solved": {"checkbox": True},
            "Slug": {"rich_text": [{"text": {"content": slug}}]},
            "Link": {"url": f"https://leetcode.com/problems/{slug}/"},
            "Difficulty": {"select": {"name": difficulty}},
            "Type": {"multi_select": [{"name": tag.strip()} for tag in tags.split(",")]}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code >= 400:
        print("❌ Create error:", res.text)
    res.raise_for_status()

def main():
    if not NOTION_TOKEN or not NOTION_DATABASE_ID or not COMMIT_MESSAGE:
        raise SystemExit("❌ Missing necessary env variables")

    changed = [x.strip() for x in CHANGED_FILES.splitlines() if x.strip()]

    interesting_exts = {".py", ".cpp", ".cc", ".c", ".java", ".js", ".ts", ".go", ".rs", ".kt", ".swift", ".rb", ".md"}
    skip_files = {"readme.md", "notes.md"}

    files = []
    for path in changed:
        ext = os.path.splitext(path)[1].lower()
        base = os.path.basename(path).lower()
        if ext in interesting_exts and base not in skip_files:
            files.append(path)

    slugs = set()
    for f in files:
        slug = extract_slug(f)
        if slug:
            slugs.add(slug)

    if not slugs:
        print("No relevant changes detected; nothing to sync.")
        return

    title, difficulty, tags = parse_commit_message()
    if not title or not difficulty or not tags:
        print("❌ Could not parse commit message.")
        return

    for slug in sorted(slugs):
        try:
            existing = notion_query_by_slug(slug)
            if existing:
                page_id = existing[0]["id"]
                notion_update_page(page_id, difficulty, tags)
                print(f"✅ Updated: {title} ({slug})")
            else:
                notion_create_page(slug, title, difficulty, tags)
                print(f"🆕 Created: {title} ({slug})")
        except requests.HTTPError as e:
            print(f"❌ Notion API error for {slug}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {slug}: {e}")

if __name__ == "__main__":
    main()