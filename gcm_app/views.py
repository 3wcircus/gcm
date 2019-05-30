import json
import logging
from datetime import datetime

import requests
from django.shortcuts import render, redirect, get_object_or_404

from .models import StudentProject

logger = logging.getLogger(__name__)
student_commit_history = []  # This will hold all the commit information fetch at init and refresh


# Default landing page
def test(request):
    logger.info('Index')
    # Get commit history
    remote_repo = 'https://api.github.com/repos/tdude0175/WebPortfolio-ThomasPBrown/commits'
    remote_repo = 'https://api.github.com/repos/autumn-ragland/portfolio/commits'
    commit_history = requests.get(remote_repo)
    commit_history_arry = json.loads(commit_history.text)
    context = {'commit_history': commit_history_arry}

    print("LENGTH:", len(commit_history_arry))
    # print(datetime.strptime("2019-01-23T21:08:03Z", "yyyy-MM-ddTHH:mm:ssZ"))

    return render(request, 'gcm_app/test.html', context)


def query_commit_history_by_student(student_id):
    student_history = ""

    return student_history


def query_commit_history_by_date(startdate, enddate):
    date_history = ""

    return date_history


def get_commit_history(repo_uri):
    repo_history = []
    # Fetch the commit history

    # Build a student commit object

    return repo_history


def refresh_history():
    repo_activity = []
    # iterate all the URLs in the database and fetch commit history for each project
    repo_projects = StudentProject.objects.all()
    # Iterate through list and fetch commit history
    # for proj in repo_projects:

    return repo_activity
