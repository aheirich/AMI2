# Graph Manager

The GraphManager maintains the current execution graph and makes it available to workers through the global store.

class GraphManager: listens for graph modification requests from clients.
It approves or denies each request so the client can raise an error if appropriate.
After modifying the graph the GraphManager optimizes it before writing to the global store.

The GraphManager ensures that clients are subscribed the right channels in order to receive the information they have requested.

In a small system their is one instance of the GraphManager.
In a larger system with many clients the GraphManager is replicated (not distributed).
Locks are used to allow concurrent modification of the graph by different clients.

