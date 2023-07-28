def PSSHRPST():
    """
    WOIFO/STEVE GORDON - PRE - Post-Init to load pharmacy classes
    08/26/08
    """
    return

def EN():
    """
    main entry point for pharmacy post-init
    XML (PSSPRE_1_0.XML) must be in Kernel default directory
    """
    # delete all classes gov package
    DELETE()

    # --

    PSSTAT = IMPORT(GETDIR(), SUPPORT())
    if not PSSTAT:
        print("Error occurred during the importing of pharmacy classes file:")
        print("  Directory: " + GETDIR())
        print("  File Name: " + SUPPORT())
        print("      Error: " + PSSTAT.split("^")[2])
        print(" o  Pharmacy class not imported.")
    else:
        print(" o  Pharmacy classes imported successfully.")
        print(" ")
        MAILMSG()

def DELETE():
    """
    delete classes for clean slate and remove previous releases
    """
    # delete all classes in pharmacy package
    print(" o  Deleting gov classes:")

    PSSTAT = $SYSTEM.OBJ.DeletePackage("gov")
    if PSSTAT:
        print("       ...[gov] deletion finished successfully.")
    else:
        print("       ...[gov] deletion failed.")
    print("")

def SUPPORT():
    """
    Returns the standard name of the XML file
    """
    return "PSSPRE_1_0.XML"

def GETDIR():
    """
    get directory where install files are located--default is in Kernel parameters.
    """
    return DEFDIR^%ZISH()

def MAILMSG():
    XMDUZ = "PACKAGE PSS*1.0*136 INSTALL"
    XMY = [DUZ]
    XMY.append("G.PSS ORDER CHECKS")
    XMSUB = "PSS*1.0*136 Installation Complete"
    message = "Installation of Patch PSS*1.0*136 has been successfully completed!"
    print(message)