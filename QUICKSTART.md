# Quick Start Guide

Get started in 5 minutes!

## 📦 Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create config file
cp env.template .env

# 3. Edit .env with your credentials
# - GITHUB_TOKEN: https://github.com/settings/tokens (needs 'repo' scope)
# - ANTHROPIC_API_KEY: https://console.anthropic.com/
# - Fill in: REPO_OWNER, REPO_NAME, REVIEWER_USERNAME, YOUR_USERNAME
```

## ✅ Verify Setup

```bash
python test_config.py
```

This checks:
- ✓ GitHub authentication
- ✓ Repository access
- ✓ Usernames exist
- ✓ PRs found

## 🚀 Run

```bash
# Step 1: Scrape comments from GitHub
python create_cache.py

# Step 2: Analyze with Claude AI
python analyze_only.py
```

## 📄 Output

- **`comments_cache.json`** - Scraped data (cached for reuse)
- **`style_guide.txt`** - AI-generated insights and patterns

## 💡 Tips

- Run `create_cache.py` once to scrape
- Run `analyze_only.py` multiple times without re-scraping
- Keeps GitHub API rate limits low
- Faster analysis iterations

## 🔍 Example `.env`

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
REPO_OWNER=facebook
REPO_NAME=react
REVIEWER_USERNAME=gaearon
YOUR_USERNAME=myusername
```

---

**Need help?** Run `python test_config.py` to diagnose issues.
