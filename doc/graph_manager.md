# Graph Manager

The GraphManager is a process that maintains the current execution graph and makes it available to workers through the global store.

class GraphManager: listens for graph modification requests from clients.
It approves or denies each request so the client can raise an error if appropriate.
After modifying the graph the GraphManager optimizes it before writing to the global store.

In a small system the GraphManager is a singleton process.
In a larger system with many clients the GraphManager is replicated (not distributed).
Locks are used to allow concurrent modification of the graph by different clients.

When a client requests a graph modification the GraphManager forwards this information to the FeatureStore.
The FeatureStore will subscribe the client to the relevant output channel.


