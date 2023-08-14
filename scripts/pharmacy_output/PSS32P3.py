def ALL(PSSIEN, PSSFT, LIST):
    """
    PSSIEN - IEN of entry in 9009032.3.
    PSSFT - Free Text TYPE in 9009032.3.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
    Field Number of the data piece being returned.
    Returns TYPE field (#.01) of APSP INTERVENTION TYPE file (#9009032.3).
    """
    import os
    import tempfile

    if not LIST:
        return
    os.makedirs(tempfile.gettempdir(), exist_ok=True)
    tmp_file = os.path.join(tempfile.gettempdir(), f"{LIST}.txt")

    with open(tmp_file, "w") as f:
        f.write("")

    if PSSIEN is None and not PSSFT:
        with open(tmp_file, "a") as f:
            f.write(f"-1^NO DATA FOUND\n")
        return

    if isinstance(PSSIEN, str) and PSSIEN.isdigit():
        PSSIEN = int(PSSIEN)

    if PSSIEN and isinstance(PSSIEN, int) and PSSIEN > 0:
        PSSIEN2 = find_entry(PSSIEN)
        if not PSSIEN2:
            with open(tmp_file, "a") as f:
                f.write(f"-1^NO DATA FOUND\n")
            return
        with open(tmp_file, "a") as f:
            f.write("1\n")
        PSS32P3 = get_fields(PSSIEN2, [".01"])
        for PSS in PSS32P3:
            set_all(tmp_file, PSS32P3[PSS][0][0], PSS)

    if not PSSIEN and PSSFT:
        if "??" in PSSFT:
            loop(tmp_file)
        else:
            result = find_entry_by_name(PSSFT)
            if not result:
                with open(tmp_file, "a") as f:
                    f.write(f"-1^NO DATA FOUND\n")
                return
            with open(tmp_file, "a") as f:
                f.write(f"{len(result)}\n")
            for PSSXX in result:
                PSSIEN = result[PSSXX][0]
                PSS32P3 = get_fields(PSSIEN, [".01"])
                for PSS in PSS32P3:
                    set_all(tmp_file, PSS32P3[PSS][0][0], PSS)

    with open(tmp_file, "r") as f:
        result = f.readlines()
    os.remove(tmp_file)
    return result


def find_entry(PSSIEN):
    """
    Find entry in 9009032.3 with the given IEN.
    """
    # Implementation not provided
    pass


def get_fields(PSSIEN, fields):
    """
    Get specified fields for the given entry in 9009032.3.
    """
    # Implementation not provided
    pass


def set_all(tmp_file, field_value, PSS):
    """
    Set data in the temporary file.
    """
    with open(tmp_file, "a") as f:
        f.write(f"{PSS}\n")
        f.write(f"{field_value}\n")


def find_entry_by_name(PSSFT):
    """
    Find entry in 9009032.3 with the given name.
    """
    # Implementation not provided
    pass


def loop(tmp_file):
    """
    Loop through all entries in 9009032.3.
    """
    # Implementation not provided
    pass