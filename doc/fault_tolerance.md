# Fault tolerance

Robust to failures in processes, cluster nodes, recover from crash.

All component behavior is based on state.
Components write volatile state to the control store whenever it changes.
This must be done atomically before acting on the state change.

Assume the stores are resilient and always available.
When a component starts up it checks the control store to see if it previously crashed.
If previous state exists it reloads its state from the store.

A cron job makes sure the store is always available.
It restarts the store if the store is not running.
It also restarts a minimum set of processes required to bootstrap the system if they are not running.
