==========
betterpath
==========

betterpath, or "bp", is an adaptation of the classic Twisted ``FilePath`` type
and interface. bp provides a simple, robust, well-tested object abstraction
over file paths, generalizing the concept of file paths beyond filesystems.

File Paths
==========

bp exposes an interface, `bp.abstract.IFilePath`, for file paths, and provides
the following concrete implementations:

 * `bp.filepath.FilePath`, for the root filesystem
 * `bp.zippath.ZipPath`, for ZIP archives
 * `bp.memory.MemoryPath`, for in-memory temporary filesystems

Examples
========

Saving Data to Disk
-------------------

The Old Way
~~~~~~~~~~~

::

    def save(base, fragments, data):
        # Unsafe either way; what if `fragments` contains ".."?
        path = os.path.join(os.path.abspath(base), os.sep.join(fragments))
        # path = os.path.join(os.path.abspath(base), *fragments)
        # I hope that this doesn't fail mid-write! Also, did the directories
        # exist? I think so, yes.
        with open(path, "wb") as handle:
            handle.write(data)

The New Way
~~~~~~~~~~~

::

    def save(base, fragments, data):
        path = base.descendant(fragments)        
        path.parent().makeDirs()
        path.setContent(data)
