mkdir -p trufflehog-repos
cd trufflehog-repos

CNTX='orgs'
NAME=''
PAGE=1
URL="https://api.github.com/$CNTX/$NAME/repos?type=private&access_token=$GITHUB_API_TOKEN&page=$PAGE&per_page=100"
echo $URL
curl ${URL}  |
  grep -e 'git_url*' |
  cut -d \" -f 4 |
  sed "s/git:\/\/github.com\//git@github.com:/g" |
  xargs -L1 git clone
