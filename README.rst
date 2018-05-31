=====
cubex
=====

``cubex`` is a Python module for analysing CUBE (.cubex) profiles.


Quick start guide
=================

``cubex`` is still a work in progress, but it is currently useable and the
following instructions should help you get started.

To create a new ``Cube`` object, open a new file.

.. code:: python

   >> import cubex
   >> prof = cubex.open('profile.cubex')

Use the ``show_metrics()`` function to list the available metrics.

.. code:: python

   >>> prof.show_metrics()
   bytes_sent
   visits
   time
   ...

By default, ``cubex`` does not load all available metrics into memory.  To load
the desired metric, say ``time``, use the ``read_data()`` function.

.. code:: python

   >> prof.read_data('time')

The ``Cube`` stores the call tree in a list, ``prof.calltrees``.  For most
programs, this will consist of a single entry.  For profiles containing
multiple executables (MPMD), each program's calltree will be an element in the
list.

The call tree can be printed using the ``print_calltree()`` function inside the
profile's calltree.

.. code:: python

   >> prof.print_tree()

This displays each node of the call tree, indented by depth, and labeled with
its corresponding region.  To limit the tree depth, use the ``depth``
argument.

.. code:: python

   >> prof.print_tree(depth=2)

To check the metric values for a particular calltree node, use the ``metrics``
function.

.. code:: python

   >> tree = prof.calltrees[0]
   >> tree.metrics('time')
   (0.0, 2217.959667782429, 2217.9596701080204, 2217.959673855075, ... )

In the example above, ``metrics`` returns a tuple of times in each
computational unit, such as an MPI rank or OpenMP thread.

For a quick inspection of the contents, start with the ``print_weights``
function on one of the call trees.  (In most cases, there will only be one
calltree.)

.. code:: python

   >> tree = prof.calltrees[0]
   >> tree.print_weights('time')
   0.877: [6] cpl_interfaces.into_cpl_
   0.068: [7] cpl_interfaces.coupler_termination_
   0.042: [2] cpl_interfaces.init_cpl_
   ...

The first column indicates the relative proportion of the metric total (in this
case, relative time) in the denoted region.  The second column indicates the
index of the child node for ``tree``.

(The particular format of this function is a work in progress, and any feedback
is welcome.)

To further inspect a region, say ``cpl_interfaces.into_cpl_``, repeat this
function over index 6.

.. code:: python

   >> tree[6].print_weights('time')
   0.979: [1] mod_oasis_getput_interface.oasis_put_r28_
   0.011: [2] MPI_Recv
   0.009: [0] remap_runoff_mod.remap_runoff_do_
   0.000: [-] cpl_interfaces.into_cpl_

The dash (``-``) indicates time spent inside the function.


Notes
-----

* Region names follow C conventions.  Fortran programs will typically convert
  any function names to lower case and will append a ``_`` to the end of the
  function name.  For example,  a function named ``GET_LAPLACIAN`` will be
  stored as ``get_laplacian_``.

  This is the usual convention, but other compilers may deviate from this, so
  it's best to inspect the regions with ``print_tree()`` or some other method
  first.

* Currently only Score-P output is supported in the ``main`` branch.  Scalasca
  output is slightly different and currently does not work as well in
  ``cubex``.

  We have some internal versions that do work, but are not yet user-friendly
  and would need a bit of a cleanup before releasing publicly.
