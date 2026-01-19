#!/usr/bin/env python3
"""
STEP 1: Create Comments Cache
==============================
Scrapes GitHub PR review comments and saves them to comments_cache.json.

Usage:
    python create_cache.py

Requirements:
    - .env file with GitHub credentials configured
    - See env.template for required variables

Output:
    - comments_cache.json: Structured comment data for analysis

Run this once, then use analyze_only.py for AI analysis.
"""

import os
import sys
import json
from dotenv import load_dotenv
from scraper import PRCommentScraper


def main():
    """Scrape comments and save as JSON cache."""
    print("=" * 70)
    print("CREATE COMMENTS CACHE")
    print("=" * 70)
    print()
    
    # Load environment
    load_dotenv()
    
    required_vars = {
        'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
        'REPO_OWNER': os.getenv('REPO_OWNER'),
        'REPO_NAME': os.getenv('REPO_NAME'),
        'REVIEWER_USERNAME': os.getenv('REVIEWER_USERNAME'),
        'YOUR_USERNAME': os.getenv('YOUR_USERNAME'),
    }
    
    missing = [key for key, value in required_vars.items() if not value]
    
    if missing:
        print("ERROR: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        sys.exit(1)
    
    # Scrape comments
    print("Scraping GitHub comments...\n")
    
    scraper = PRCommentScraper(
        github_token=required_vars['GITHUB_TOKEN'],
        repo_owner=required_vars['REPO_OWNER'],
        repo_name=required_vars['REPO_NAME']
    )
    
    comments_data = scraper.scrape_all_comments(
        author_username=required_vars['YOUR_USERNAME'],
        reviewer_username=required_vars['REVIEWER_USERNAME']
    )
    
    # Save as JSON
    cache_file = "comments_cache.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(comments_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Cache created: {cache_file}")
    print(f"✓ Total comments: {comments_data['metadata']['total_comments']}")
    print(f"\nYou can now run: python analyze_only.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
