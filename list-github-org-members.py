import os
import requests
import json
import csv

github_token = os.environ.get('GITHUB_API_TOKEN')
github_org = os.environ.get('GITHUB_ORG')
output_file = "github_users.csv"

url_get_all_members = 'https://api.github.com/orgs/' + github_org + \
    '/members?access_token=' + github_token + \
    '&page=1&per_page=100'

response = requests.get(url_get_all_members)
users_list = response.json()

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel', delimiter=' ')

    for u in users_list:
        url_get_user = 'https://api.github.com/users/' + str(u['login']) + \
            '?access_token=' + github_token
        response = requests.get(url_get_user)
        user_data = response.json()

        writer.writerow([user_data['login'] + ',' + str(user_data['email'])])
