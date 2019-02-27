import requests
import json
import logging
import os, sys

def logger(logfile_name):
    file_handler = logging.FileHandler(filename=logfile_name)
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.INFO, 
        format='[%(asctime)s] %(levelname)s - %(message)s',
        handlers=handlers
    )

    logger = logging.getLogger('DISK_USAGE_LOG')
    return logger

def validate_environment_variables(needed_envs):
    for env in needed_envs:
        if env not in os.environ:
            logger.error("Could not find the needed environment variable '{}'".format(env))
            exit(1)

def slack_notify(message):
    headers = {
        "Content-type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL,
        "username": "Elasticsearch",
        "text": "{}".format(message)
    }
    with requests.Session() as s:
        slack_msg_response = s.post(SLACK_CUSTOM_INTEGRATION_URL + SLACK_TOKEN, headers=headers, json=payload)
        if slack_msg_response.status_code == 200:
            logger.info("Successfully notified in channel '{}'!".format(SLACK_CHANNEL))
        else:
            logger.error("Could not notify slack in channel '{}' due to a returned status code '{}'".format(SLACK_CHANNEL, slack_msg_response.status_code))

def get_disk_info(elasticsearch_url, elasticsearch_node_status_fs_uri, xpack_username, xpack_pass):
    disk_usage_struct = []

    with requests.Session() as s:
        logger.info("Getting disk metrics from remote elasticsearch...")
        response = s.get(elasticsearch_url + elasticsearch_node_status_fs_uri, auth=(xpack_username, xpack_pass))
        if response.status_code is not 200:
            logger.error("Could not get elasticsearch disk metrics due to a returned status code '{}'".format(response.status_code))
            slack_notify("Could not get elasticsearch disk metrics due to a returned status code '{}'".format(response.status_code))

        response_payload = response.json()
        for payload_index in response_payload:
            if payload_index == 'nodes':
                for node in response_payload[payload_index]:
                    node_name = response_payload[payload_index][node]['name']
                    node_host = response_payload[payload_index][node]['host']
                    node_region = response_payload[payload_index][node]['attributes']['region']
                    node_instance_configuration = response_payload[payload_index][node]['attributes']['instance_configuration']
                    for data in response_payload[payload_index][node]['fs']['data']:
                        node_fs_type = data['type']
                        node_fs_total_in_bytes = data['total_in_bytes']
                        node_fs_available_in_bytes = data['available_in_bytes']

                        node_disk_available = (node_fs_available_in_bytes * 100) / node_fs_total_in_bytes
                    disk_usage_struct.append(
                        {
                            node_name : {
                                "host": node_host,
                                "region": node_region,
                                "instance_configuration": node_instance_configuration,
                                "fs_type": node_fs_type,
                                "fs_disk_available_perc": round(node_disk_available, 2)
                            }
                        }
                    )
        return disk_usage_struct

def verify_disk_usage(disk_usage_struct):
    logger.info("Validating if available disk from remote elasticsearch trespassed threshold of {}%".format(ELASTICSEARCH_DISK_AVAILABLE_THRESHOLD))
    for node in disk_usage_struct:
        for instance in node:
            if node[instance]['fs_disk_available_perc'] <= ELASTICSEARCH_DISK_AVAILABLE_THRESHOLD:
                logger.info("Alarming Elasticsearch's node '{}' due to '{}' percent of available disk. The current threshold is '{}'".format(instance, node[instance]['fs_disk_available_perc'], ELASTICSEARCH_DISK_AVAILABLE_THRESHOLD))
                slack_notify("ES node '{}' have only '{}' percent of available disk".format(instance, node[instance]['fs_disk_available_perc']))

ELASTICSEARCH_URL = 'https://767de82bb33448f498e7a72913aeba94.sa-east-1.aws.found.io:9243/'
ELASTICSEARCH_NODE_STATUS_FS_URI = '_nodes/stats/fs'
ELASTICSEARCH_DISK_AVAILABLE_THRESHOLD = 30
SLACK_CUSTOM_INTEGRATION_URL = 'https://hooks.slack.com/services/T03S48U3S/B9PQFRTLG/'
SLACK_CHANNEL = '#pipeline_two'
SLACK_USERNAME = 'Elastisearch'
LOGFILE_NAME = '/tmp/es_disk.log'

logger = logger(LOGFILE_NAME)
validate_environment_variables(['XPACK_USERNAME','XPACK_PASSWORD','SLACK_TOKEN'])
SLACK_TOKEN = os.environ['SLACK_TOKEN']
disk_usage_struct = get_disk_info(ELASTICSEARCH_URL, ELASTICSEARCH_NODE_STATUS_FS_URI, os.environ['XPACK_USERNAME'], os.environ['XPACK_PASSWORD'])
verify_disk_usage(disk_usage_struct)
