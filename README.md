# crispy-eureka

Random utility scripts:

### list all ec2 instances by VPC. Useful if you have a ton of VPCs and want to
check if some are not being utilized

```
python3 ./ec2-instances-by-vpc.py
```


### list github organization members. Useful if you want to share a list of active
users to make sure they're still employed by the Org

```
python3 ./list-github-org-members.py
```

### louder - my headphones are always too quiet so I force it louder

```
python3 ./louder.py
```

### nmapper - just a little Nmap starter to quick scan a network where you might want to do something with the output


```
python3 ./nmapper.py
```

### trufflehog - just a wrapper around trufflehog. looks for AWS keys only, checks
if those keys are still active in your AWS account.

```
cd trufflhog
./get-all-repos.sh
python3 ./scan-repos.py
```
