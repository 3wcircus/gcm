import json
import logging
from datetime import datetime

import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentProject

commit_history_arry = []

logger = logging.getLogger(__name__)
student_commit_history = []  # This will hold all the commit information fetch at init and refresh


# Default landing page
def test(request):
    logger.info('Index')
    # Get commit history
    # remote_repo = 'https://api.github.com/repos/tdude0175/WebPortfolio-ThomasPBrown/commits'
    # remote_repo = 'https://api.github.com/repos/autumn-ragland/portfolio/commits'
    # commit_history = requests.get(remote_repo)
    commit_history_arry = refresh_history(request)
    context = {'commit_history': commit_history_arry}

    # print("LENGTH:", len(commit_history_arry))
    # print(datetime.strptime("2019-01-23T21:08:03Z", "yyyy-MM-ddTHH:mm:ssZ"))
    query_commit_history_by_student(commit_history_arry, 'autumn-ragland')
    return render(request, 'gcm_app/test.html', context)


def query_commit_history_by_student(commit_list, student_id):
    student_history = ""
    # Build a student commit object
    # student_history = [x for x in commit_list if x['commit.author.name'] == student_id]
    for com in commit_list:
        for com2 in com:
            if (com2['commit']['author']['name']) == student_id:
                print(com2['commit']['author']['name'])
    return student_history


def query_commit_history_by_date(commit_list, startdate, enddate):
    date_history = []
    for com in commit_list:
        kount = 1
        for com2 in com:
            if kount > 3:
                break
            kount = kount + 1
            date_history.append(com2)

    return date_history


def get_commit_history(repo_uri):
    repo_history = []

    return repo_history


def refresh_history(request):
    repo_activity = []
    # iterate all the URLs in the database and fetch commit history for each project
    repo_projects = StudentProject.objects.all()
    # Iterate through list and fetch commit history
    # for proj in repo_projects:
    onlyone = True;
    for project in repo_projects:
        print(project.project_url)
        all_commits = requests.get(project.project_url)
        repo_activity.append(json.loads(all_commits.text))
    return repo_activity


def home(request):
    commit_history_arry = refresh_history(request)
    recent_commits = query_commit_history_by_date(commit_history_arry, "", "")
    context = {'commit_history': recent_commits}
    return render(request, 'gcm_app/by_date.html', context)
