# Reddit Context Cleaner 🧹🤖

**Reddit Context Cleaner** is a high-performance Python utility that transforms messy, metadata-heavy Reddit JSON files into clean, structured Markdown. It is specifically optimized for feeding long conversation threads into LLMs (like ChatGPT, Claude, and Gemini) without wasting tokens on JSON syntax or unnecessary whitespace.

## ✨ Why use this?

| Feature | Description |
| :--- | :--- |
| **Token Efficiency** | Strips out 90%+ of useless JSON bloat. |
| **Recursive Threading** | Captures deep "replies to replies" that standard copy-pasting misses. |
| **Branching Logic** | Uses Markdown `>` nesting and "Replying to" tags so the AI understands the conversation flow perfectly. |
| **Entity Cleaning** | Automatically fixes HTML artifacts like `&gt;` and `&amp;`. |

---

## 🚀 Getting Your Data
You don't need a Reddit API key or developer account.

1.  **Open Reddit:** Go to any post, subreddit feed, or user profile.
2.  **The Shortcut:** Add `.json` to the very end of the URL.
    * *Example:* `reddit.com/r/science/comments/abc/` → `reddit.com/r/science/comments/abc/.json`
3.  **Save:** Press `Ctrl + S` (or `Cmd + S`) to save the page as `reddit.json` in the same folder as this script.

---

## 🛠️ How to Use

You require **Python 3.x** (Standard library only; no `pip install` needed).

### 1. Quick Start (Installation)
1. **Create the Script:** Open your code editor (VS Code, Replit, or Notepad), create a new file named `main.py`, and paste the script code(you will find it in the file "main.py" in this repo) into it.
2. **Prepare the Data:** Place your downloaded `reddit.json` in the **same folder** as `main.py`.
3. **Run the Program:**
   * **Terminal/VS Code:** Type `python main.py`
   * **Replit:** Hit the green **Run** button.



### 2. Choose Your Mode
The script will detect your file type and offer four modes:
* **Mode 1 (Subreddit):** Grabs all post titles and bodies from a community feed.
* **Mode 2 (Single Post):** Extracts the main post and the **entire** recursive comment tree.
* **Mode 3 (User Profile):** Filter a user's history by Posts, Comments, or Both.
* **Mode 4 (Comments Only):** Strips away post bodies and just gives you the raw discussion threads.

### 3. Output
Choose to either print the result to your terminal or save it to `cleaned.txt` for easy drag-and-drop into an AI chat.

---

## 🤖 Recommended LLM Prompt

Copy and paste the block below into your AI (ChatGPT, Claude, Gemini). This ensures the LLM understands the hierarchy, metadata, and context logic perfectly.

```text
**System Instructions:**
I am providing a cleaned Reddit dataset formatted for high token efficiency and logical tracking. Please process the data according to these rules:

1. **Hierarchy Tracking:** The symbol ">" represents a top-level comment. Multi-level symbols (e.g., ">>", ">>>") represent nested replies. Maintain this parent-child relationship during analysis.
2. **Metadata Anchor:** Each block includes Author, Score, and "Replying to". Use the Score to weight the importance of arguments and "Replying to" to verify the conversation flow.
3. **Context Awareness:** If a block contains "[Context: Subreddit | Post]", treat it as a distinct discussion topic to avoid cross-contamination of ideas.
4. **Task:** Analyze the provided threads to identify core arguments, sentiment shifts, and consensus points.

**User Request:** [INSERT YOUR SPECIFIC REQUEST HERE, e.g., "Summarize the top 3 most controversial opinions and why they were debated."]

---
[PASTE DATA FROM CLEANED.TXT HERE]
```

---

## ❓ Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **File Not Found** | Ensure the JSON file is named exactly `reddit.json` and is in the same folder as `main.py`. |
| **Invalid JSON** | Reddit might be throttling you. If the file contains "Too Many Requests," wait 60 seconds and try the `.json` URL again. |
| **Encoding Errors** | Ensure you are running Python 3.10 or higher for the best UTF-8 support. |
