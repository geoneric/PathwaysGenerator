.. _sec-changelog:

Changelog
=========
Description of of all notable changes made per version.


0.0.7
-----
- Ordering of actions in a pathway map (classic layout) is now based on the ordering of actions
  in the sequences file.


0.0.6
-----
- Added support for specifying action editions: the same action can occur at different horizontal
  locations (at different periods in time or at ranges of conditions) in a pathway map. To make
  this possible, such actions must be differentiated from each other. This can now be done using
  editions, which are just integral values. Each action has one. When not specified, the edition
  of an action is zero. Example::

    # Action a occurs twice, but they are different editions
    current a[1]
    current b
    b a[2]


0.0.5
-----
- Added ``ap_plot_pathway_map`` command. See ``ap_plot_pathway_map --help`` for more information.
- Added support for specifying combinations of actions in the file containing sequences. Example::

    current a
    current b
    current c
    # Action a continues, but is combined with the new action e
    a d(a & e)
