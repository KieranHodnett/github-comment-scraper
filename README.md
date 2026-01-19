# GitHub PR Review Comment Analyzer

Scrape GitHub PR review comments and use Claude AI to generate a personalized code review style guide.

## 🎯 What It Does

1. **Scrapes** review comments from a specific reviewer on your PRs
2. **Analyzes** patterns using Claude AI
3. **Generates** a personalized style guide with themes, principles, and examples

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy the template and add your credentials:
```bash
cp env.template .env
```

Edit `.env` with your values:
```bash
GITHUB_TOKEN=your_github_token          # Get at: https://github.com/settings/tokens (needs 'repo' scope)
ANTHROPIC_API_KEY=your_anthropic_key    # Get at: https://console.anthropic.com/
REPO_OWNER=repository_owner
REPO_NAME=repository_name
REVIEWER_USERNAME=reviewer_github_username
YOUR_USERNAME=your_github_username
```

### 3. Test Configuration (Recommended)
```bash
python test_config.py
```
This validates your settings before scraping.

### 4. Scrape Comments
```bash
python create_cache.py
```
Creates `comments_cache.json` with all review comments.

### 5. Analyze with AI
```bash
python analyze_only.py
```
Generates `style_guide.txt` with insights and patterns.

## 📁 Project Structure

```
githubCommentScraper/
├── create_cache.py      # Step 1: Scrape GitHub comments
├── analyze_only.py      # Step 2: Analyze with Claude AI
├── scraper.py           # GitHub API logic
├── analyzer.py          # Claude AI integration
├── test_config.py       # Configuration validator
├── requirements.txt     # Dependencies
├── .env                 # Your config (create from template)
└── env.template         # Configuration template
```

## 🔑 Getting API Keys

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select the **`repo`** scope
4. Generate and copy to `.env`

### Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up/sign in
3. Create a new API key
4. Copy to `.env`

## 📤 Workflow

```bash
# One-time: scrape and cache comments
python create_cache.py

# Run analysis (can run multiple times without re-scraping)
python analyze_only.py
```

**Benefits:**
- ✅ Scrape once, analyze multiple times
- ✅ No rate limit issues from repeated scraping
- ✅ Faster analysis iterations
- ✅ Experiment with different prompts

## 📊 Output Files

### `comments_cache.json`
Structured data with all scraped comments (cached for reuse).

### `style_guide.txt`
AI-generated analysis including:
- Overview of reviewer's style
- Key themes and categories
- Core review principles with examples
- Common patterns and anti-patterns
- Communication style analysis
- Actionable pre-submission checklist

## 🛠️ Troubleshooting

### Run the diagnostic tool:
```bash
python test_config.py
```

### Common Issues

**"Repository not found (404)"**
- Verify `REPO_OWNER` and `REPO_NAME` are correct
- Check your token has access to the repository
- Repository URL should be: `https://github.com/REPO_OWNER/REPO_NAME`

**"No comments found"**
- Verify usernames are exact (case-sensitive)
- Check that PRs exist where you're the author with reviews from that user

**"Model not found"**
- The default model is `claude-sonnet-4-20250514`
- If needed, override in `.env`: `CLAUDE_MODEL=your-model-name`

**Authentication errors**
- Ensure GitHub token has `repo` scope
- Verify Anthropic API key is valid
- Check for extra spaces in `.env`

## 🎨 Customization

### Change Claude Model
Add to your `.env`:
```bash
CLAUDE_MODEL=claude-sonnet-4-20250514
```

### Modify Analysis Prompt
Edit `analyzer.py` → `_create_analysis_prompt()` method to customize the analysis focus.

### Filter PRs
Modify `scraper.py` → `fetch_my_pull_requests()` to add date ranges or state filters.

## 🤝 Contributing

Feel free to fork, modify, and adapt to your needs! This tool is designed to be flexible and extensible.

## 📄 License

MIT License - use and modify as needed.

---

**Built with:** PyGithub • Anthropic Claude • Python
