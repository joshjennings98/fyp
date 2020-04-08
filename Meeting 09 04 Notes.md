# Notes

* Made all the other graph types
  * Extreme realxed is terrible (as expected)
    * Depends on whether messages are sent before or after it receives a spike
    * E.g. if on epoch one, all neurons spike then some neurons receive messages before itis their turn to send messages causing the t to increase.
    * Especially true of fully connected where the time difference increments by one for every neurons, so n1 has time difference of 1, and n100 receives time difference of 100
    * Can't be solved using waiting for fanin since unlike GALS, neurons don't always fire so it would hang
  * Barrier acts as the clocked one does (from the looks of it). It seems to work
* All my networks are inline with the graph schema ones.
  * I hadn't randomly seeded them correctly
* Problems are to do with the random numbers and how they affect I.
  * Can replicate the behavior of the unseeded ones in matlab by keeping I constant
  * Leads me to belive it is an issue with I in the poets ones
  * Possibly random number generators?
  * Also, the I is randomly updated each time whereas the poets ones use the same seed (I think) every time they generate the new random I. Need to investigate
* Started work on the quality checker
  * Can't replciate the matlab results in python
  * Gonna scrape all the stuff from matlab to use in the XML
  * My theory is that it will still be broken due to the random number thing
* Need the IP for the POETS computer