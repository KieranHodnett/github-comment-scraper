#!/usr/bin/env python3
"""
Configuration Test Script
Tests your GitHub credentials and repository access before running the main scraper.
"""

import os
import sys
from dotenv import load_dotenv
from github import Github, GithubException


def test_github_connection():
    """Test GitHub authentication and repository access."""
    print("=" * 70)
    print("TESTING GITHUB CONFIGURATION")
    print("=" * 70)
    print()
    
    # Load environment variables
    load_dotenv()
    
    github_token = os.getenv('GITHUB_TOKEN')
    repo_owner = os.getenv('REPO_OWNER')
    repo_name = os.getenv('REPO_NAME')
    reviewer_username = os.getenv('REVIEWER_USERNAME')
    your_username = os.getenv('YOUR_USERNAME')
    
    # Check if variables are set
    print("1. Checking environment variables...")
    missing = []
    
    if not github_token:
        missing.append("GITHUB_TOKEN")
    else:
        print(f"   ✓ GITHUB_TOKEN: {github_token[:10]}...")
    
    if not repo_owner:
        missing.append("REPO_OWNER")
    else:
        print(f"   ✓ REPO_OWNER: {repo_owner}")
    
    if not repo_name:
        missing.append("REPO_NAME")
    else:
        print(f"   ✓ REPO_NAME: {repo_name}")
    
    if not reviewer_username:
        missing.append("REVIEWER_USERNAME")
    else:
        print(f"   ✓ REVIEWER_USERNAME: {reviewer_username}")
    
    if not your_username:
        missing.append("YOUR_USERNAME")
    else:
        print(f"   ✓ YOUR_USERNAME: {your_username}")
    
    if missing:
        print(f"\n   ✗ MISSING: {', '.join(missing)}")
        print("\nPlease add these to your .env file.")
        return False
    
    print()
    
    # Test GitHub authentication
    print("2. Testing GitHub authentication...")
    try:
        g = Github(github_token)
        user = g.get_user()
        print(f"   ✓ Authenticated as: {user.login}")
        print(f"   ✓ Name: {user.name or 'N/A'}")
        print(f"   ✓ Rate limit: {g.get_rate_limit().core.remaining}/{g.get_rate_limit().core.limit}")
    except GithubException as e:
        print(f"   ✗ Authentication failed: {e.data.get('message', str(e))}")
        print("\nPossible issues:")
        print("   - Token is invalid or expired")
        print("   - Token doesn't have required permissions")
        print("\nHow to fix:")
        print("   1. Go to: https://github.com/settings/tokens")
        print("   2. Generate a new token with 'repo' scope")
        print("   3. Update GITHUB_TOKEN in your .env file")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)}")
        return False
    
    print()
    
    # Test repository access
    print("3. Testing repository access...")
    full_repo_name = f"{repo_owner}/{repo_name}"
    print(f"   Attempting to access: {full_repo_name}")
    
    try:
        repo = g.get_repo(full_repo_name)
        print(f"   ✓ Repository found!")
        print(f"   ✓ Full name: {repo.full_name}")
        print(f"   ✓ Description: {repo.description or 'N/A'}")
        print(f"   ✓ Private: {repo.private}")
        print(f"   ✓ Default branch: {repo.default_branch}")
    except GithubException as e:
        if e.status == 404:
            print(f"   ✗ Repository not found (404)")
            print("\nPossible issues:")
            print(f"   - Repository '{full_repo_name}' doesn't exist")
            print("   - Repository name or owner is misspelled")
            print("   - Repository is private and token doesn't have access")
            print("\nHow to fix:")
            print("   1. Verify the repository exists on GitHub")
            print("   2. Check for typos in REPO_OWNER and REPO_NAME")
            print("   3. Ensure your token has access to private repos (if applicable)")
            print("\nTo find the correct values:")
            print("   - Go to the repository on GitHub")
            print(f"   - The URL looks like: https://github.com/OWNER/REPO")
            print(f"   - OWNER goes in REPO_OWNER")
            print(f"   - REPO goes in REPO_NAME")
        else:
            print(f"   ✗ Error accessing repository: {e.data.get('message', str(e))}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)}")
        return False
    
    print()
    
    # Test user existence
    print("4. Testing GitHub usernames...")
    
    # Test your username
    try:
        your_user = g.get_user(your_username)
        print(f"   ✓ YOUR_USERNAME ({your_username}) exists")
        print(f"     Name: {your_user.name or 'N/A'}")
    except GithubException as e:
        if e.status == 404:
            print(f"   ✗ YOUR_USERNAME ({your_username}) not found")
            print("     Please check the spelling (case-sensitive)")
        else:
            print(f"   ✗ Error: {e.data.get('message', str(e))}")
        return False
    
    # Test reviewer username
    try:
        reviewer_user = g.get_user(reviewer_username)
        print(f"   ✓ REVIEWER_USERNAME ({reviewer_username}) exists")
        print(f"     Name: {reviewer_user.name or 'N/A'}")
    except GithubException as e:
        if e.status == 404:
            print(f"   ✗ REVIEWER_USERNAME ({reviewer_username}) not found")
            print("     Please check the spelling (case-sensitive)")
        else:
            print(f"   ✗ Error: {e.data.get('message', str(e))}")
        return False
    
    print()
    
    # Test for PRs
    print("5. Testing for pull requests...")
    try:
        pulls = list(repo.get_pulls(state='all', sort='created', direction='desc'))
        total_pulls = len(pulls)
        your_pulls = [pr for pr in pulls if pr.user.login == your_username]
        
        print(f"   ✓ Total PRs in repository: {total_pulls}")
        print(f"   ✓ PRs by {your_username}: {len(your_pulls)}")
        
        if len(your_pulls) == 0:
            print(f"\n   ⚠ Warning: No PRs found by {your_username}")
            print("     The scraper will run but find no data.")
            print("\n     Possible reasons:")
            print(f"     - {your_username} hasn't created any PRs in this repo")
            print(f"     - YOUR_USERNAME is incorrect")
        else:
            print(f"\n   Recent PRs by {your_username}:")
            for i, pr in enumerate(your_pulls[:3], 1):
                print(f"     {i}. PR #{pr.number}: {pr.title} ({pr.state})")
            
            # Check for reviews from reviewer
            reviews_found = False
            for pr in your_pulls[:5]:  # Check first 5 PRs
                for review in pr.get_reviews():
                    if review.user.login == reviewer_username:
                        reviews_found = True
                        break
                if reviews_found:
                    break
            
            if reviews_found:
                print(f"\n   ✓ Found reviews from {reviewer_username}!")
            else:
                print(f"\n   ⚠ Warning: No reviews found from {reviewer_username} in recent PRs")
                print(f"     (Checked first 5 PRs)")
    except Exception as e:
        print(f"   ✗ Error checking PRs: {str(e)}")
        return False
    
    print()
    print("=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nYour configuration looks good. You can now run:")
    print("  python create_cache.py")
    print()
    return True


if __name__ == "__main__":
    try:
        success = test_github_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
