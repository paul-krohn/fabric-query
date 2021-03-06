### Installation ###

* create a virtualenv with python 2.7: ```virtualenv --python /usr/local/bin/python2.7 /some/where```
* activate it: ```. /some/where/bin/activate```
* install fabric and boto: ```pip install fabric boto```

### Usage ###

Invoke fabric with: ```fab -f /path/to/repo/fabfile.py ```
As an example, you can set the region, and a query:

```
fab -f /path/to/repo/fabfile.py region:us-west-2 query:tag=cluster_name,value=application-name example_command:/etc/sudoers.d,/etc/rsyslog.d
```

To simplify usage, create ~/.fabricrc, specifying the path to the fabfile, and the default region. See fabricrc-example.
