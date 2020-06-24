# Script for auto running network tests (part 1)

# run  'screen -S snn_test' before this so it doesn't die

# set times here
now=$(date +%s)
startTime=$(date -d '06/01/2020 12:00:00' +%s)
timeoutTime=$(date -d '06/01/2020 19:50:00' +%s)

sleep $(( $startTime - $now )) # wait till start time

timeout $(( $timeoutTime - $startTime )) sh tests.sh # kill if taking longer than expected

