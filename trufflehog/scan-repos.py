''' scan all the repos with trufflehog '''
import datetime
import os
import json
import boto3

excludes_file = "excludes.txt"
rules_file = "regexes-aws-only.json"
log_dir = "logs"
repos_dir = "trufflehog-repos"

today = datetime.date.today()
log_date = f'{today:%Y-%m-%d}'

truffle_cmd = "nice -19 trufflehog \
                  --regex \
                  --entropy=False \
                  -x " + excludes_file + "\
                  --rules " + rules_file + "\
                  --json"

def truffle_run_all():
    ''' Run TrufflHog on each repo '''
    # TODO: this relies on the 'get-all-the-repos.sh script having been run. Could
    # incorporate that functionality into this one'
    repos = os.listdir(repos_dir)

    findings = []
    discovered_keys = set()
    for r in repos:
        # Run trufflehog against each repo
        print("Running truffleHog against " + r)
        output = os.popen(truffle_cmd + " " + repos_dir + "/" + r ).read()

        # The trufflehog output has each line containing a json string. We need to
        # massage this so that all lines combined can be written out as valid json.
        lines = output.splitlines()
        for l in lines:
            findings.append(json.loads(l))
            for f in findings:
                discovered_keys.add(f['stringsFound'][0])

    # Log the Trufflehog findings for future grep-ing
    with open('logs/truffle-log-' + log_date + '.json', 'w') as outfile:
        json.dump(findings, outfile)

    # Return just the discovered keys
    return(list(discovered_keys))


def get_iam_users():
    ''' Get the AWS IAM users '''
    # Create IAM client
    iam = boto3.client('iam')

    print("Fetching IAM users")
    response = iam.list_users()
    user_data = response["Users"]
    users_list = []
    for u in user_data:
        users_list.append(u['UserName'])

    return users_list


def get_user_keys():
    ''' Get the Access Keys for each user '''
    # Create IAM client
    iam = boto3.client('iam')

    users = get_iam_users()

    print("Fetching Access Keys for all users")
    access_key_metadata = []
    for u in users:
        # List access keys through the pagination interface.
        paginator = iam.get_paginator('list_access_keys')
        for response in paginator.paginate(UserName=u):
            access_key_metadata.append(response['AccessKeyMetadata'])

    user_key_dict = {}
    for data in access_key_metadata:
        if data: # some users don't have keys
            for d in data: # some users have multiple keys
                user_key_dict[d['UserName']] = []
            for d in data: # to handle multiple keys, we need extra loop here
                user_key_dict[d['UserName']].append((data[0]['AccessKeyId']))

    return (user_key_dict)


def check_for_active_compromised(truffle_keys,user_keys):
    ''' Compare TruffleHog discovered keys to active AWS keys '''
    print("Comparing active keys to see if they've been compromised")

    compromised_active_keys = set()

    for key, value in user_keys.items():
        for v in value:
            if v in truffle_keys:
                print(v + " belonging to " + key + " is compromised")
                compromised_active_keys.add(v)

    return list(compromised_active_keys)



truffle_keys = truffle_run_all()
user_keys = get_user_keys()

# # DEBUG: forcing an active key to show up as discoverd by TruffleHog
# truffle_keys = []
# truffle_keys.append('')

compromised_keys = check_for_active_compromised(truffle_keys, user_keys)
print("COMPROMISED ACTIVE KEYS:", compromised_keys)
