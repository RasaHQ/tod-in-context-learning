#!/bin/bash

version=$1
current_dir=$2

cd version_${version}
poetry run rasa run actions &
action_pid=$!

sleep 5

for dir in ../e2e_tests/*/; do
    dirname=$(basename $dir)
    poetry run rasa test e2e ${dir} -m models | grep "failed," > ${current_dir}/test_results/version_${version}_${dirname}.txt
done

kill $action_pid
cd ${current_dir}
