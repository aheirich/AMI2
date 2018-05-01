# Feature Store
The FeatureStore is a process that buffers data over time and provides a wrapper around the Redis publish-subscribe interface.

class FeatureStore: takes commands from the GraphManager.
These commands can direct the FeatureStore to open a buffer to accumulate data over time, and can indicate that a particular output or outputs should be provided to a particular client.
Clients acquire data by subscribing to channels from the global Redis.

The FeatureStore is responsible for publishing the results of worker computations that have been stored in the global Redis.


