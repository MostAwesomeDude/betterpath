def modeIsWriting(mode):
    """
    Determine whether a file mode will permit writing.
    """

    m = mode.lower()
    return m not in ("r", "rb", "ru", "rub")
