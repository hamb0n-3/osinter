#!/bin/bash

osinter_dir="$( realpath "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")"
echo -e "[+] OSINTER dir: $osinter_dir\n"

echo "[+] Checking code formatting with ruff"
echo "======================================="
ruff format "$osinter_dir" || exit 1
echo

echo "[+] Linting with ruff"
echo "======================="
ruff check "$osinter_dir" || exit 1
echo

if [ "${1}x" != "x" ] ; then
  MODULES=`echo ${1} | sed -e 's/,/ /g'`
  for MODULE in ${MODULES} ; do
    echo "[+] Testing ${MODULE} with pytest"
    pytest --exitfirst --disable-warnings --log-cli-level=ERROR "$osinter_dir" --cov=osinter/test/test_step_2/test_cli.py --cov-report="term-missing" --cov-config="$osinter_dir/test/coverage.cfg" -k ${MODULE}
  done
else
  echo "[+] Testing all modules with pytest"
  pytest --exitfirst --disable-warnings --log-cli-level=ERROR "$osinter_dir" --cov=osinter/test/test_step_2/test_cli.py --cov-report="term-missing" --cov-config="$osinter_dir/test/coverage.cfg"
fi
