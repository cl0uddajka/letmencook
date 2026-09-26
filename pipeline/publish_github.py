"""Publish only market observations and validated feeds to the authorized data repo."""
import shutil
import subprocess
from pathlib import Path
from publish_prices import ROOT, publish

REPO = ROOT / 'build/github-market'
REMOTE = 'https://github.com/cl0uddajka/letmencook.git'


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True, encoding='utf-8').strip()


if __name__ == '__main__':
    import os
    os.environ['GIT_TERMINAL_PROMPT'] = '0'
    os.environ['GCM_INTERACTIVE'] = 'never'
    if not REPO.exists():
        subprocess.run(['git', 'clone', REMOTE, str(REPO)], check=True)
    if git('remote', 'get-url', 'origin') != REMOTE or git('branch', '--show-current') != 'main':
        raise SystemExit('Unexpected remote or branch; no publication.')
    if git('status', '--porcelain'):
        raise SystemExit('Data checkout has uncommitted changes; inspect before publication.')
    git('pull', '--ff-only', 'origin', 'main')
    publish(ROOT / 'data/market-prices/latest.json', ROOT / 'public/prices')
    target = REPO / 'data/market-prices/latest.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'data/market-prices/latest.json', target)
    shutil.copytree(ROOT / 'public/prices', REPO / 'public/prices', dirs_exist_ok=True)
    git('add', 'data/market-prices/latest.json', 'public/prices')
    if git('diff', '--cached', '--name-only'):
        git('commit', '-m', 'Update reviewed market observations and validated feed')
        git('push', 'origin', 'main')
    print('GitHub price feed is up to date.')
