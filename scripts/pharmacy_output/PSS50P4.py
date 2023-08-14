def ALL(PSSIEN, PSSFT, LIST):
    """
    PSSIEN - IEN of entry in 50.4.
    PSSFT - Free Text name in 50.4.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01) and CONCENTRATION UNITS field (#1) of DRUG ELECTROLYTES file (#50.4).
    """
    import os
    import errno
    import tempfile
    import subprocess

    if not LIST:
        return

    TMP_DIR = tempfile.mkdtemp()
    try:
        # Create a temporary file for the M code
        m_code_file = os.path.join(TMP_DIR, "m_code.m")
        with open(m_code_file, "w") as f:
            f.write(f" ;;; PLACEHOLDER FOR M CODE TRANSLATION OF PSS50P4\n")

        # Run the M code using the GT.M/YottaDB shell
        command = ["mumps", "-run", m_code_file]
        result = subprocess.run(command, capture_output=True, text=True)
        m_output = result.stdout

        # Parse the M output and populate the ^TMP array
        tmp_output = m_output.split("\n")
        for line in tmp_output:
            if line.startswith("^TMP"):
                parts = line.split(",")
                subscript = parts[1]
                field_number = parts[2].split(")")[0]
                data = parts[3].split("=")[1].strip()

                if subscript not in LIST:
                    LIST[subscript] = {}
                LIST[subscript][field_number] = data

    except OSError as e:
        if e.errno == errno.ENOENT:
            print("GT.M/YottaDB is not installed or not in the system path.")
        else:
            print("An error occurred while running the M code:", e)
    finally:
        # Clean up the temporary directory
        os.remove(m_code_file)
        os.rmdir(TMP_DIR)

    return LIST