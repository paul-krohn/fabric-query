from fabric.api import run, env
from fabric.decorators import runs_once
from boto.ec2 import connect_to_region
import json

aws_region = None
if 'default_region' in env.keys():
    aws_region = env.default_region

@runs_once
def region(arg_region):
    """
    Set the region global. For example: region:ap-southeast-1
    """
    global aws_region
    aws_region = arg_region


@runs_once
def query(value=None, tag="Name"):
    """
    query:tag=cluster_name,value=some_application
    """
    conn = connect_to_region(aws_region)
    query_filters = {
        "tag:%s" % tag: value
    }
    env.hosts = []
    # print json.dumps(query_filters, indent=4)
    query_instances = conn.get_all_instances(filters=query_filters)
    for reservation in query_instances:
        for instance in reservation.instances:
            # print instance.id
            env.hosts.append(instance.tags['Name'])
    env.hosts = sorted(env.hosts)


@runs_once
def print_hosts():
    """
    Print out the content of env.hosts; primarily for troubleshooting.
    """
    print json.dumps(env.hosts, indent=4, sort_keys=True)


def example_command(argument1="", argument2=""):
    run("ls %s %s" % (argument1, argument2))
