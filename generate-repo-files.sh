#!/bin/bash
set -e

usage () {
  echo "usage: $(basename "$0") version repository enabled platform PlatformName"
  echo
  echo "version examples: 8.8, 9.0, current"
  echo "reposity examples: release, rc, daily"
  echo "enabled values: 0, 1"
  echo "platform examples: el7, el8, amzn2, fc32"
  echo "PlatformName examples: Enterprise Linux 7, Amazon Linux 2"
  exit
}

TEMPLATEDIR=$(dirname "$0")

if [ $# -lt 5 ]; then
    usage
fi

VERSION=(${1//./ })
if (( ${VERSION[1]} % 2 )); then
    VERSION='current'
else
    VERSION=$1
fi
shift
REPO=$1
REPO_NAME=${REPO^}
shift
ENABLED=$1
shift
PLATFORM=$1
shift
PLATFORM_NAME=$@

if [ $ENABLED -ne 0 -a $ENABLED -ne 1 ]; then
    usage
fi

if [ $REPO = 'release' ]; then
    YUM_REPO='htcondor'
else
    YUM_REPO="htcondor-$REPO"
fi

if [[ ! -e $TEMPLATEDIR/repo.template ]]; then
    echo "Error: repo.template does not exist!" >&2
    exit
fi

sed "
    s/<yumrepo>/$YUM_REPO/
    s/<Platform-Name>/$PLATFORM_NAME/
    s/<platform>/$PLATFORM/
    s/<version>/$VERSION/
    s/<repo>/$REPO/
    s/<Repo-Name>/$REPO_NAME/
    s/<Enabled>/$ENABLED/
" "$TEMPLATEDIR/repo.template" > "$YUM_REPO.repo"

echo "Wrote: $YUM_REPO.repo"
