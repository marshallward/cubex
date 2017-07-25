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

   >> prof.calltrees[0].print_tree()

This displays each node of the call tree, indented by depth, and labeled with
its corresponding region.

At this point, it helps if the user has some intuitive feel for the call tree
in the profile.  (And if anyone has feedback on how to improve this, please
submit feedback.)

Having said that, if one knows the function (or "region" in CUBE parlance) of
interest, then the data is accessed with the ``region`` property.

.. code:: python

   >> prof.regions[reg].cnodes
   [<cubex.calltree.CallTree object at 0x7f4437892f90>,
    <cubex.calltree.CallTree object at 0x7f4437539f10>,
    ...
   ]

This returns a list of each node (actually subtree) in the call tree where this
function was called.

To distinguish between ``cnodes``, one can inspect its call tree (using
``print_tree()``) or inspect its parent node.

.. code:: python

   >> cnode = prof.regions[reg].cnodes[0]
   >> cnode.parent.region.name
   'function_name_calling_cnode_'

One can also inspect the node index (``cnode.idx``) although this requires some
knowledge of the tree itself, which can be checked using the CUBE graphical
browser.

Finally, to get the metric values at the target ``cnode``, access its
``metrics`` property.

.. code:: python

   >> prof.regions[reg].cnodes[0].metrics['time']
   (496.59532077590507, 291.106782542039, 496.5975198073004, ...)

This returns a list of the time measured in each computational unit, such as an
MPI rank or OpenMP thread.


Notes
-----

* Region names follow C conventions.  Fortran programs will typically convert
  any function names to lower case and will append a ``_`` to the end of the
  function name.  For example,  a function named ``GET_LAPLACIAN`` will be
  stored as ``get_laplacian_``.

  This is the usual convention, but other compilers may deviate from thisj
  so it's recommended that you inspect the regions before accessing them.

* Currently only Score-P output is supported in the ``main`` branch.  Scalasca
  output is slightly different and currently does not work as well in
  ``cubex``.

  We have some internal versions that do work, but are not yet user-friendly
  and would need a bit of a cleanup before releasing publicly.
