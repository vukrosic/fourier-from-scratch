#!/bin/bash
# Runs the eight steps, then the checks. About 40 seconds on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
for step in step1_heat step2_waves step3_build step4_recipe step5_solve step6_spike step7_phone step8_today; do
  echo
  echo "=== $step.py"
  python3 $step.py
done
echo
python3 tests.py
