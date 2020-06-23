import csv
import os
import stat

accounts = {} # dict of dict, {account{"long_name": "", "number": "", "short_name": ""}}

# adjust these variables as needed
adfs_host = 'adfs.nuskin.com'
region = 'us-west-2'
role = 'global-admin'  # do not include the account short name
input_file = 'aws-accounts.csv'

with open(input_file) as csv_file:
    rows = csv.reader(csv_file)
    for row in rows:
        accounts[row[0]] = {
            'long_name': row[0],
            'number': row[1],
            'short_name': row[2]
        }

with open('auto-login.sh', 'w') as accounts_script:
    accounts_script.write('#!/bin/bash' + '\n')
    for account in accounts:
        accounts_script.write(f'echo {accounts[account]["long_name"]}')
        accounts_script.write('\n')
        accounts_script.write(f'aws-adfs login --no-sspi --adfs-host={adfs_host} --session-duration 32400 --role-arn arn:aws:iam::{accounts[account]["number"]}:role/{accounts[account]["short_name"]}-{role} --region {region} --profile {accounts[account]["short_name"]}')
        accounts_script.write('\n\n')
        with open (f'{accounts[account]["short_name"]}.sh', 'w') as account_script:
            account_script.write(
                '#!/bin/bash' + '\n' + f'aws-adfs login --no-sspi --adfs-host={adfs_host} --session-duration 32400 --role-arn arn:aws:iam::{accounts[account]["number"]}:role/{accounts[account]["short_name"]}-{role} --region {region}'
            )
        os.chmod(f'{accounts[account]["short_name"]}.sh', os.stat(f'{accounts[account]["short_name"]}.sh').st_mode | stat.S_IEXEC)  # make file executable
os.chmod('auto-login.sh', os.stat('auto-login.sh').st_mode | stat.S_IEXEC)  # make file executable
