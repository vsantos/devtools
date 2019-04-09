# devtools
A set of tools and automated scripts to achieve IT tasks

## Bulk Update in Dynamo

`scripts/bulk_change_dynamo_items.py`

A script which will scan a dynamodb's table based on query to a posterior bulk change in it's results

Requirements:
- python 3.3+
- `~/.aws/credentials` with the `[default]` value as the script credentials
- `pip3 install -r requirements/bulk_change_dynamo_items.txt`


Caution: This script must be edited with the needed CONSTANT VARIABLES needed values

```
# To run just
$ python3 scripts/bulk_change_dynamo_items.py
```

## Kluster

`scripts/kluster`

A script which will change your current k8s context (cluster) and if a token is associated with that cluster it will copy into the clipboard and open a browser page with k8s default's Dashboard

Requirements:
- bash 4.3+
- `jq` 2.0 +
- `kubectl` + `kubectx`
- `xdg-open`
- `x-clip`
- python 2.x +

```
# To run just
$ ./kluster CLUSTER-ENV
```

## Bulk S3 backup

`scripts/bulk_s3_backup`

A script which will:
  1) Get all items from a bucket
  2) Filter all items which matches a certain pattern: `${S3_REMOTE_TO_LOCAL_BACKUP_FILE_PATTERN}`
  3) Backup all items from bucket locally (just in case, even if does not matches the pattern)
  4) Move remote files (which matched the pattern) to a remote s3 backup directory

## Elastic Search - Disk Usage

`script/elasticsearch_disk_usage.py`

A script which will connect using REST in a remote cloud elasticsearch and retrieve disk usage data, checking the user's threshold and alarming if needed in a Slack channel. The following environment variables are needed: `XPACK_USER`, `XPACK_PASSWORD` and `SLACK_TOKEN`. Other configuration such as the threshold it self or the slack channel can be achieved editing the script directly in the `CONSTANT` session.

Obs: It can be also be used as a AWS python lambda. Requests module must be imported as boto for achieving this goal.

## Kubernetes - Istio Envoy Routing CRDs Backup

`script/istio_envoy_crds_backup`

A script which will:
  1) Given a namespace the script will get a copy for the following CRDs: services, virtualservices and destinationrules
  2) Compress it in a single `tar.gz` backup file
