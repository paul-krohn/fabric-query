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
            # assumes the Name tag is the FQDN.
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
def next_cron_run_time(command_name=False, output=True, user='root'):
    """
    Get the next time a cron will run on a host.
    Assumes every-24-hour crons. Prints the time, in human-readable form.
    """

    # scrape the crontab for non-commented entries matching the command_name
    crontab_result = run("sudo crontab -l -u %s | grep '%s' | grep -v ^#" % (user, command_name),
                         warn_only=True,
                         quiet=True)
    if crontab_result.return_code is 0:
        # (cron_minute, cron_hour)\
        cron_parts = re.split(" +", crontab_result)
        cron_minute = int(cron_parts[0])
        cron_hour = int(cron_parts[1])
        # get the current UTC hour, minute; python type oddness requires secondary assignment
        current_gmtime = time.gmtime()
        current_hour = current_gmtime[3]
        current_minute = current_gmtime[4]
        # puts("current UTC time: %s:%s" % (current_hour, current_minute))

        next_run_offset = 0
        # cron hour is < current hour, therefore tomorrow
        if cron_hour < current_hour:
            next_run_offset = 86400
        elif cron_hour == current_hour:
            if cron_minute <= current_minute:
                # tomorrow, assuming it has already run
                next_run_offset = 86400

        next_run_base =  time.gmtime(int(time.time()) + next_run_offset)
        next_run_epoch_time = calendar.timegm(
            (next_run_base[0], next_run_base[1], next_run_base[2], cron_hour, cron_minute, 0))
        if output:
            puts("next run of %s at: %s" % (" ".join(cron_parts[5:len(cron_parts)]), time.strftime("%F %X", time.gmtime(next_run_epoch_time))))
        return next_run_epoch_time
    else:
        puts("no cron entry for %s matching %s" % (user, command_name))
