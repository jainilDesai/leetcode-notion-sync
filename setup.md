# 🚀 LeetCode → GitHub → Notion (Wrapper Edition)

This project is a lightweight wrapper around the original LeetHub v2 project (https://github.com/arunbhardwaj/LeetHub-2.0.git) with extra automation to sync solved LeetCode problems into a GitHub repo and a Notion database.

The wrapper provides:

- automatic commits when you solve problems on LeetCode
- structured commit messages containing Problem Title, Difficulty and Tags
- a GitHub Action that reads commits and updates a Notion database

---

## ⚡ Features

- ✅ Auto-commit solved problems from LeetCode to your GitHub repository
- ✅ Commit messages include Problem Title, Difficulty and Tags
- ✅ GitHub Action automatically syncs problems to your Notion database
- ✅ Notion table shows: Problem, Difficulty, Tags, Link, Solved status
- ✅ Fully automated workflow — you just solve problems

---

## 🛠️ Setup Guide (Step by step)

Below are the minimal steps required to get the wrapper working. Replace placeholder values (YOUR_TEMPLATE_LINK_HERE, YOUR_USERNAME, etc.) with your own.

### 1) Duplicate the Notion template

I provided a Notion template you can duplicate to create your personal tracker.

👉 Duplicate template: [YOUR_TEMPLATE_LINK_HERE](https://www.notion.so/26775205bf668059882bdee385eaa90d?v=26775205bf6681718892000c4b98b428&source)

After duplicating, note the Database ID (used later).

---

### 2) Get Notion credentials

1. Open Notion Integrations: https://www.notion.so/my-integrations and click **+ New integration**.
2. Copy the Integration Token and save it as `NOTION_TOKEN`.
3. Open the duplicated Notion page and copy the Database ID from the URL. Example:

   https://www.notion.so/username/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=yyyyyyyyyyyyyyyyyyyyyyyy

   The long `xxxxxxxx...` portion is your Database ID. Save it as `NOTION_DATABASE_ID`.

---

### 3) Install the extension (wrapper)

1. Clone this wrapper repository locally:

   ```bash
   git clone https://github.com/jainilDesai/leethubV2-wrapper.git
   cd leethubV2-wrapper
   ```

2. Load the extension in Chrome:

   - Open Chrome and navigate to `chrome://extensions/`
   - Enable Developer mode
   - Click "Load unpacked" and select the cloned folder

3. Connect to GitHub when prompted by the extension. Use this repo when connecting leetHub extension to github. Select "connect existing repo" on from the options then write "leetcode-notion-sync". Your extension should be connected with this repo now.
   When configured, commits for solved problems will look like:

`[LeetHub] Plus One | Difficulty: Easy | Tags: Array, Math`

---

### 4) Configure GitHub Actions for Notion sync

This repo includes a GitHub Action workflow at `.github/workflows/notion_sync.yml` that reads new commits and updates Notion.

To enable it on your GitHub repo:

1. Go to your repository on GitHub → Settings → Secrets and variables → Actions → New repository secret.
2. Add the following secrets:

   - `NOTION_TOKEN` = <your Notion integration token>
   - `NOTION_DATABASE_ID` = <your Notion database id>

3. Push a change (or solve a new problem) and the Action will run to update Notion.

---

## Demo & Screenshots

(Add screenshots or GIFs here)

- Example commit message: a screenshot or text sample
- GitHub Actions log showing a successful sync
- Notion table showing Problem, Difficulty, Tags

---

## Credits

- Base project: LeetHub v2 (https://github.com/arunbhardwaj/LeetHub-2.0.git)
- Wrapper & Notion automation: [JainilDesai](https://github.com/jainilDesai)

---

## Customization

- Change the commit message format: edit `getCommitMessage()` inside the extension source.
- Add more Notion fields or change the mapping: edit `scripts/update_notion.py`.

---

## Workflow recap

1. Solve a problem on LeetCode.
2. The extension creates a commit in your GitHub repo.
3. GitHub Action reads the commit and updates Notion.
4. Open your Notion database to review progress.

---

## Contributing

Fork the repo and open a PR if you want to improve formatting, add fields, or support additional features (languages, test results, tagging rules).

Happy coding — track your progress and iterate!
