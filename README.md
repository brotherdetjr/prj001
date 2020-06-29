`Engine` contains all `World` instances.
`World` describes certain isolated location at given time. It can be spawned from a parent `World` when a player
first time-travels to a given point of time.
In theory, a deterministic discrete-time world can be described with a _global_ state and related
transition rule(s) &mdash; an algorithm of calculation of next tick's state.
In practice, it may appear too costly to recompute the global state every single tick.
Apparently, the world can be partitioned into separate objects, so that we could operate the _local_ states of these
objects.
To keep the number of calculations reasonable, the next object's state should not depend on too many other objects.
For example, we model a world consisting of billiard balls. The ball's properties (position, direction and velocity)
at next sampling time must be determined by the current ball's properties, and obstacle it faces, if any.
Conversely, if we add gravity and want to calculate it absolutely precisely, we need to factor in the position and
mass of every ball in our world.
Local objects' states assume we can have a dedicated transition rule for every object or object type,
i.e. we don't need to have a one-for-all algorithm to calculate the next state anymore, but we can apply relatively
small isolated rules.
