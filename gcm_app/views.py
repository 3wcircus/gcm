import json
import logging

import pytz
import requests


from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from .models import StudentProject
from datetime import *
from dateutil.tz import *

# commit_history_arry = array()  # TODO: Does this really need to be global?

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# student_commit_history = []  # This will hold all the commit information fetch at init and refresh


# Scratch view just used for testing crap
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


# This function takes a list of github commits in JSON and filters the list based on the user name passed in
def query_commit_history_by_student(commit_list, student_id):
    student_history = ""
    # Build a student commit object
    # FIXME: Could not get this filter method to work so just used brute force below
    # student_history = [x for x in commit_list if x['commit.author.name'] == student_id]
    for com in commit_list:
        for com2 in com:
            if (com2['commit']['author']['name']) == student_id:
                print(com2['commit']['author']['name'])
    return student_history


# This function takes a list of github commits in JSON and filters the list based on the dates passed in
# TODO: Actually filter by dates in commit messages. Atm just returns
def query_commit_history_by_date(commit_list, startdate, enddate):
    date_history = []
    for com in commit_list:
        kount = 1
        for com2 in com:
            if kount > 3:
                break
            kount = kount + 1
            utc = datetime.strptime(com2['commit']['author']['date'], '%Y-%m-%dT%H:%M:%Sz')
            from_zone = tzutc()
            # to_zone = tzlocal()
            to_zone = pytz.timezone('America/Chicago')
            # Tell the datetime object that it's in UTC time zone since
            # datetime objects are 'naive' by default
            utc = utc.replace(tzinfo=from_zone)

            # Convert time zone
            central = utc.astimezone(to_zone)
            commit_date = central.strftime('%a, %d %b %Y %I:%M%p')
            # logger.warning('DATE: ' + str(commit_date))
            filtered_list = {
                'commit_user': com2['commit']['author']['name'],
                'commit_url': com2['html_url'],
                'commit_date': commit_date,
                'commit_msg': com2['commit']['message']
            }
            date_history.append(filtered_list)

    return date_history


def get_commit_history(repo_uri):
    repo_history = []

    return repo_history


def refresh_history(request):
    repo_activity = []
    # iterate all the URLs in the database and fetch commit history for each project
    # repo_projects = StudentProject.objects.all()
    repo_projects = StudentProject.objects.filter(project_name='Passion')
    # Iterate through list and fetch commit history
    # for proj in repo_projects:
    onlyone = False
    logger.debug('Fetching commit history...')
    for project in repo_projects:
        # print(project.project_url)

        all_commits = requests.get(project.project_url, auth=('kevin-codecrew', 'F1sh@B0ne'))
        if all_commits.status_code == 200:
            # print('Success!')
            repo_activity.append(json.loads(all_commits.text))
        else:
            print('Not Found. '+str(all_commits.status_code))

        if onlyone:
            break
    return repo_activity


def home(request):
    recent_commits = query_commit_history_by_date(refresh_history(request), "", "")
    context = {'commit_history': recent_commits}
    return render(request, 'gcm_app/by_date.html', context)
