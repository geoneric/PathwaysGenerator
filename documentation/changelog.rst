.. _sec-changelog:

Changelog
=========
Description of of all notable changes made per version.


0.0.5
-----
- Added ``ap_plot_pathway_map`` command. See ``ap_plot_pathway_map --help`` for more information.
- Added support for specifying combinations of actions in the file containing sequences. Example::

    current a
    current b
    current c
    # Action a continues, but is combined with the new action e
    a d(a & e)
