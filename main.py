import json
import re
import sys
import html

FILENAME = "reddit.json" # change this if your file name is different

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# load JSON file safely
try:
    with open(FILENAME, "r", encoding="utf-8") as f:
        raw_json = f.read()

    # remove control characters that break json parsing
    raw_json = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", raw_json)
    data = json.loads(raw_json)

except FileNotFoundError:
    print(f"❌ Error: '{FILENAME}' not found. Make sure you renamed your file correctly.")
    sys.exit()

except json.JSONDecodeError:
    print(f"❌ Error: '{FILENAME}' is not valid JSON.")
    sys.exit()

print(
    "What kind of Reddit JSON did you load?\n\n"
    "1 → Subreddit / community feed\n"
    "2 → Single post (full thread)\n"
    "3 → User profile / history\n"
    "4 → Comments only\n"
)

choice = input("Enter number: ").strip()
clean_blocks = []

def extract_comments(children, parent_author="Unknown", depth=1):
    # walk the comment tree recursively
    for child in children:
        if child.get("kind") != "t1":
            continue

        comment = child["data"]
        body = comment.get("body", "")

        # skip removed or empty comments
        if body in ("[deleted]", "[removed]", ""):
            continue

        author = comment.get("author", "unknown")
        prefix = ">" * depth

        # add post context when available
        context = ""
        if depth == 1 and comment.get("link_title"):
            context = (
                f" [Context: {comment.get('subreddit_name_prefixed')} | "
                f"Post: {comment.get('link_title')}]"
            )

        clean_blocks.append(
            f"{prefix} Author: {author} (Replying to {parent_author}){context}\n"
            f"{prefix} Score: {comment.get('score')}\n"
            f"{prefix} {clean_text(body)}"
        )

        replies = comment.get("replies")
        if isinstance(replies, dict):
            extract_comments(
                replies.get("data", {}).get("children", []),
                parent_author=author,
                depth=depth + 1
            )

# option 1: subreddit feed
if choice == "1":
    if isinstance(data, list):
        print("❌ This looks like a single post file. Use option 2 or 4.")
        sys.exit()

    posts = data.get("data", {}).get("children", [])
    for item in posts:
        if item.get("kind") != "t3":
            continue

        post = item["data"]
        content = post.get("selftext") or f"URL: {post.get('url', '')}"

        clean_blocks.append(
            f"POST\n"
            f"Title: {post.get('title')}\n"
            f"Author: {post.get('author')}\n"
            f"Score: {post.get('score')}\n\n"
            f"{clean_text(content)}"
        )

# option 2: full post with comments
elif choice == "2":
    if not isinstance(data, list):
        print("❌ This does not appear to be a single post JSON.")
        sys.exit()

    post = data[0]["data"]["children"][0]["data"]
    clean_blocks.append(
        f"SOURCE: Reddit Post\n"
        f"Title: {post.get('title')}\n"
        f"Author: {post.get('author')}\n"
        f"Score: {post.get('score')}\n\n"
        f"{clean_text(post.get('selftext', ''))}"
    )

    extract_comments(data[1]["data"]["children"], parent_author=post.get("author", "OP"))

# option 3: user profile
elif choice == "3":
    if isinstance(data, list):
        print("❌ Profiles use feed-style JSON, not single-post JSON.")
        sys.exit()

    print("\np → Posts | c → Comments | b → Both")
    sub_choice = input("Select: ").lower().strip()

    for item in data.get("data", {}).get("children", []):
        kind = item.get("kind")
        entry = item["data"]
        subreddit = entry.get("subreddit_name_prefixed", "r/unknown")

        if kind == "t3" and sub_choice in ("p", "b"):
            clean_blocks.append(
                f"--- USER POST [{subreddit}] ---\n"
                f"Title: {entry.get('title')}\n"
                f"Score: {entry.get('score')}\n\n"
                f"{clean_text(entry.get('selftext') or entry.get('url'))}"
            )

        elif kind == "t1" and sub_choice in ("c", "b"):
            clean_blocks.append(
                f"> USER COMMENT [{subreddit}]\n"
                f"> In Thread: {entry.get('link_title')}\n"
                f"> Score: {entry.get('score')}\n"
                f"> {clean_text(entry.get('body'))}"
            )

# option 4: comments only
elif choice == "4":
    if isinstance(data, list):
        extract_comments(data[1]["data"]["children"])
    else:
        extract_comments(data.get("data", {}).get("children", []))
else:
    print("❌ Invalid choice.")
    sys.exit()

# output results
if not clean_blocks:
    print("\n⚠️ No usable content extracted.")
    sys.exit()

output_text = "\n\n---\n\n".join(clean_blocks)
print(f"\n✅ Extracted {len(clean_blocks)} blocks.")
print("1 → Print to terminal\n2 → Save to 'cleaned.txt'")

if input("Enter 1 or 2: ").strip() == "2":
    with open("cleaned.txt", "w", encoding="utf-8") as f:
        f.write(output_text)
    print("📂 Saved to 'cleaned.txt'")
else:
    print("\n" + output_text)
