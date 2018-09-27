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