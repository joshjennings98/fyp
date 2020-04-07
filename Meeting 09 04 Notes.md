# Notes

* Paper gals dowsn't use gaussian, it uses uniform. 
* That does/doesn't fix it.
* All my networks are inline with the graph schema ones.
  * I hadn't randomly seeded them correctly
* Made all the other graph types (except barrier so far)
* Extreme realxed is terrible (as expected)
  * Depends on whether messages are sent before or after it receives a spike
  * E.g. if on epoch one, all neurons spike then some neurons receive messages before itis their turn to send messages causing the t to increase.
  * Especially true of fully connected where the time difference increments by one for every neurons, so n1 has time difference of 1, and n100 receives time difference of 100
  * Can't be solved using waiting for fanin since unlike GALS, neurons don't always fire so it would hang