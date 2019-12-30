import json
import logging

import pytz
import requests

from django.shortcuts import render, redirect, get_object_or_404

from .models import StudentProject
from datetime import *
from dateutil.tz import *

# Setup logging
logger = logging.getLogger(__name__)
# FIXME: logging levels do not seem 2 b working
logger.setLevel(logging.DEBUG)


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


# TODO: Use this or remove it
def get_commit_history(repo_uri):
    repo_history = []

    return repo_history


# This function will refresh the full commit history of all repository entries in the cfg database
def refresh_history(request, cfilter):
    print('Search Filter: '+str(cfilter))

    repo_activity = []
    last_three_commits = []
    cfilter_type='' # Hold string representation of filter type
    if cfilter == 0:
        print("No search filter")
        cfilter_type = 'All'
        repo_projects_raw = StudentProject.objects.all().order_by('project_student_name', 'project_name')
    elif cfilter == 1:
        print('search filter = 1')
        cfilter_type = 'Passion Project'
        repo_projects_raw = StudentProject.objects.filter(project_name='Passion').order_by('project_student_name',
                                                                                           'project_name')
    elif cfilter == 2:
        print('search filter = 2')
        cfilter_type = 'Dev Portfolio Project'
        repo_projects_raw = StudentProject.objects.filter(project_name='Portfolio').order_by('project_student_name',
                                                                                             'project_name')
    elif cfilter == 3:
        print('search filter = 3')
        cfilter_type = 'Other Project'
        repo_projects_raw = StudentProject.objects.filter(project_name='Other').order_by('project_student_name',
                                                                                            'project_name')
    else:
        print('Invalid filter option: ' + str(cfilter))
        repo_projects_raw = StudentProject.objects.all().order_by('project_student_name', 'project_name')

    # Iterate through list and fetch commit history
    onlyone = False  # debug flag to only return one result
    logger.debug('Fetching commit history...')
    print("number of projects: " + str(len(repo_projects_raw)))
    for project in repo_projects_raw:
        repo_activity = []
        print(project.project_url)
        # FIXME: This shouldnt be here
        all_commits = requests.get(project.project_url, auth=('kevin-codecrew', 'F1sh@B0ne'))
        if all_commits.status_code == 200:
            repo_activity.append(json.loads(all_commits.text))
        else:
            print('Not Found. ' + str(all_commits.status_code))

        # if onlyone:
        #     break

        for com in repo_activity:
            kount = 1
            for com2 in com:
                if kount > 3:
                    break
                kount = kount + 1
                utc = datetime.strptime(com2['commit']['author']['date'], '%Y-%m-%dT%H:%M:%Sz')
                from_zone = tzutc()
                to_zone = pytz.timezone('America/Chicago')
                # Tell the datetime object that it's in UTC time zone since
                # datetime objects are 'naive' by default
                utc = utc.replace(tzinfo=from_zone)

                # Convert time zone
                central = utc.astimezone(to_zone)
                commit_date = central.strftime('%a, %d %b %Y %I:%M%p')
                # logger.warning('DATE: ' + str(commit_date))
                filtered_list = {
                    # 'commit_user': com2['commit']['author']['name'],
                    'commit_user': project.project_student_name,
                    'commit_url': com2['html_url'],
                    'commit_date': commit_date,
                    'commit_msg': com2['commit']['message'],
                    'commit_type': cfilter_type
                }
                last_three_commits.append(filtered_list)
                # print(filtered_list)
    return last_three_commits


def home(request):
    recent_commits = refresh_history(request, 0)
    context = {'commit_history': recent_commits}
    return render(request, 'gcm_app/index.html', context)


def index(request):
    recent_commits = refresh_history(request, 0)
    context = {'commit_history': recent_commits}
    return render(request, 'gcm_app/index.html', context)


def sindex(request, soption):
    recent_commits = refresh_history(request, soption)
    context = {'commit_history': recent_commits}
    return render(request, 'gcm_app/index.html', context)
