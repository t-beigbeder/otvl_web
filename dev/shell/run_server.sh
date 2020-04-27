#!/usr/bin/env bash
. $HOME/tools/venv/otvl_web/bin/activate
cmd_dir=`dirname $0`
if [ "`echo $cmd_dir | cut -c1`" != "/" ] ; then
    cmd_dir="`pwd`/$cmd_dir"
fi
base_dir=`echo $cmd_dir | sed -e s=/dev/shell==`
PYTHONPATH=${base_dir}/server/code/python
export PYTHONPATH
cd $base_dir/server
python -m otvl_web.server -c /home/guest/git/otvl_blog/data/tests/test_server_qgg.yml