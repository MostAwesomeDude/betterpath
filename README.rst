==========
betterpath
==========

betterpath, or "bp", is an adaptation of the classic Twisted FilePath type and
interface. bp provides a simple, robust, well-tested object abstraction over
file paths, generalizing the concept of file paths beyond filesystems.

File Paths
==========

bp exposes an interface, `bp.abstract.IFilePath`, for file paths, and provides
the following concrete implementations:

 * `bp.filepath.FilePath`, for the root filesystem
 * `bp.zippath.ZipPath`, for ZIP archives
 * `bp.memory.MemoryPath`, for in-memory temporary filesystems
