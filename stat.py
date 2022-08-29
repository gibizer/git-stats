import argparse
import collections
import sys

import git


def main(repo_path, search_term, branch):
    commits = 0
    added = 0
    removed = 0
    authors = collections.Counter()

    repo = git.Repo(repo_path)
    for commit in repo.iter_commits(branch):
        if search_term in commit.message:
            commits += 1
            authors[commit.author.name] += 1
            if commit.author.name != commit.committer.name:
                authors[commit.committer.name] += 1

            # TODO: add Co-authored-by

            added += commit.stats.total['insertions']
            removed += commit.stats.total['deletions']
            sys.stdout.write('+')
            sys.stdout.flush()
        else:
            sys.stdout.write('.')
    print()
    print('repo: %s search term: %s' % (repo_path, search_term))
    print('-' * 20)
    print('commits: %d' % commits)
    print()
    print('%d insertions %d deletions' % (added, removed))
    print()
    print('author, number of commits')
    print('-' * 20)
    print('%s' % '\n'.join(
        '%s, %d' % item for item in authors.items()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate git stats')
    parser.add_argument('--repo', dest='repo',
                        help='Path of the git repository')
    parser.add_argument('--filter', dest='filter',
                        help='Filter the commits by a substring in the commit '
                             'message')
    parser.add_argument('--branch', dest='branch', default='master',
                        help='The branch to search on. Defaulted to master')
    args = parser.parse_args()
    main(args.repo, args.filter, args.branch)
