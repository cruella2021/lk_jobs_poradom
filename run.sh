#!/bin/sh
export IP_HOST_1C='192.168.111.204'
export LOGIN_1C='web'
export PASSWORD_1C='passwd0'
export IP_HOST_DB='192.168.111.133'
export USER_DB='poradomdb_userr'
export PASSWORD_DB='ht6Bnc39Oirbv'
export NAME_DB='poradomdbb'
######SSH
export IP_HOST_SSH='192.168.111.133'
export USER_SSH='bisoft'
export PASSWORD_SSH='jKbd9ejQ5xCm'
export LOCAL_STORAGE_IAMGE='/home/pi/git/lk_jobs_poradom/images/'
export REMOTE_STORAGE_IAMGE='/var/www/sporadom/httpdocs/web/uploads/'

python3 run_jobs.py
