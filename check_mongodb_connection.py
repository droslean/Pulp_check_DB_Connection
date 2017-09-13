#!/bin/python3
import subprocess
import sys
import os
import json
import pprint


def test_connection(hostname, username, password):
    try:
        return subprocess.check_output("sshpass -p " + password +
                                       " ssh " + hostname +
                                       " -l " + username + " uname -a",
                                       shell=True).decode("utf-8")

    except subprocess.CalledProcessError as rc:
        print("RC: %d " % rc.returncode)
        sys.exit(rc.returncode)


def restart_qpidd():
    try:
        return subprocess.check_output("sshpass -p " + password +
                                       " ssh " + hostname +
                                       " -l " + username +
                                       " service qpidd restart",
                                       shell=True).decode("utf-8")

    except subprocess.CalledProcessError as rc:
        print("qpidd restart failed with rc: %d " % rc.returncode)
        sys.exit(rc.returncode)


def restart_pulp_celerybeat():
    try:
        return subprocess.check_output("sshpass -p " + password +
                                       " ssh " + hostname +
                                       " -l " + username +
                                       " service pulp_celerybeat restart",
                                       shell=True).decode("utf-8")

    except subprocess.CalledProcessError as rc:
        print("pulp_celerybeat restart failed with rc: %d " % rc.returncode)
        sys.exit(rc.returncode)


def restart_pulp_resource_manager():
    try:
        return subprocess.check_output("sshpass -p " + password +
                                       " ssh " + hostname +
                                       " -l " + username +
                                       " service pulp_resource_manager \
                                       restart",
                                       shell=True).decode("utf-8")

    except subprocess.CalledProcessError as rc:
        print("pulp_resource_manager restart failed with rc: %d "
              % rc.returncode)
        sys.exit(rc.returncode)


def restart_httpd():
    try:
        return subprocess.check_output("sshpass -p " + password +
                                       " ssh " + hostname +
                                       " -l " + username +
                                       " service httpd restart",
                                       shell=True).decode("utf-8")

    except subprocess.CalledProcessError as rc:
        print("httpd restart failed with rc: %d " % rc.returncode)
        sys.exit(rc.returncode)


# Check mongoDB authentication by using the PULP API
def check_mongodb_authentication():
    try:
        return subprocess.check_output("curl -k -X GET https://" + hostname +
                                       ":" + port + "/pulp/api/v2/status/",
                                       shell=True).decode("utf-8")

    except subprocess.CalledProcessError as rc:
        print("mongodb_authentication failed with rc: %d " % rc.returncode)
        sys.exit(rc.returncode)


if __name__ == '__main__':
    global hostname, username, password
    try:
        hostname = os.environ['SSH_HOSTNAME']
        port = os.environ['API_PORT']
        username = os.environ['SSH_USERNAME']
        password = os.environ['SSH_PASSWORD']

    except KeyError:
        print("Could't find required variables")
        sys.exit(1)

    info = test_connection(
        hostname, username, password)
    print(info)

    # Restart qpidd
    print("Restarting qpidd...")
    print(restart_qpidd())

    # Restart pulp_celerybeat
    print("Restarting pulp_celerybeat...")
    print(restart_pulp_celerybeat())

    # Restart pulp_resource_manager
    print("Restarting pulp_resource_manager...")
    print(restart_pulp_resource_manager())

    # Restart httpd
    print("Restarting httpd...")
    print(restart_httpd())

    # Check MongoDB authentication using PULP API
    try:
        curl_results = json.loads(check_mongodb_authentication())
        pprint.pprint(curl_results)
        is_connected = curl_results['database_connection']['connected']
    except json.decoder.JSONDecodeError:
        print("Coulnd't parse JSON data.")
        sys.exit(1)

    print(is_connected)
    if is_connected:
        print("Connected to Database")
        sys.exit()
    else:
        print("Not connected")
        sys.exit(1)
