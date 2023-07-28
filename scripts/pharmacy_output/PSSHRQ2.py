def PSSHRQ2():
    """
    WOIFO/AV,TS - Makes a request to PEPS and returns as Global
    09/20/07
    """
    pass


def IN(PSSBASE):
    """
    Handles request/response to PEPS
    """
    # Cleanup output global
    # KILL ^TMP($JOB,PSSBASE,"OUT")  ; PO: commented as requested by Stan Brown on 6/4/09

    # save "IN" nodes
    PSSHRTMX = 0
    ^TMP($J,"SAVE","IN") = ^TMP($J,PSSBASE,"IN")
    PSSRBASE = PSSBASE

    # Check FDB status if an update is occurring
    FDBFLG = CHKSTAT^PSSDSFDB()
    # If FDB update set global and quit
    if FDBFLG:
        ^TMP($J,PSSBASE,"OUT",0) = FDBFLG
        return

    # Validate input global
    PSS["validationResult"] = DRIVER^PSSHRVAL(PSSBASE)
    if PSS["validationResult"] == 0:
        # Check if data written to global, set to 1 if data exist
        if $DATA(^TMP($JOB,PSSBASE,"OUT")):
            ^TMP($JOB,PSSBASE,"OUT",0) = 1
        # If no data in output global , set to 0
        if '$DATA(^TMP($JOB,PSSBASE,"OUT")):
            ^TMP($JOB,PSSBASE,"OUT",0) = 0
        return

    # End call if no call to make
    if PSS["validationResult"] == 0:
        return

    # Create XML request
    PSSXML = BLDPREQ^PSSHREQ(PSSBASE)
    # Send XML request to PEPS, receive handle to XML in return

RETRY:  # Retry entry point if first connection attempt fails
    PSSRESLT = PEPSPOST^PSSHTTP(.PSSDOC, PSSXML)

    # If request unsuccessful go straight to error handling
    if +PSSRESLT == 0:
        ALTERROR^PSSHRQ2O(PSSBASE)
        return

    # If request is successful parse response
    # and put in results global object.  Also set the last successful run time.
    if +PSSRESLT > 0:
        OUT^PSSHRQ2O(PSSDOC, PSSBASE)
        SLASTRUN^PSSHRIT(NOW^XLFDT())

    if not PSSHRTMX:
        PSSHRTRT = $P(^TMP($J,PSSRBASE,"OUT",0), "^")
        if PSSHRTRT != 0 and PSSHRTRT != 1:
            K ^TMP($J,PSSRBASE,"OUT")
            ^TMP($J,PSSRBASE,"OUT",0) = "-1^An unexpected error has occurred."
        SHG()
        goto RETRY

END:  # re-store "IN" nodes
    ^TMP($J,PSSBASE,"IN") = ^TMP($J,"SAVE","IN")
    K ^TMP($J,"SAVE","IN")
    PSSRBASX = $P(^TMP($J,PSSRBASE,"OUT",0), "^")
    if PSSRBASX != -1 and PSSRBASX != 0 and PSSRBASX != 1:
        K ^TMP($J,PSSRBASE,"OUT")
        ^TMP($J,PSSRBASE,"OUT",0) = "-1^An unexpected error has occurred."
    if $P(^TMP($J,PSSRBASE,"OUT",0), "^") != -1:
        CLEXP^PSSHRQ2O()
    return


def SHG():
    # Hang before retry
    PSSHRTMX = 1
    if $E(PSSRBASE, 1, 4) != "PING" or ($G(PSSMCHK) == "CHECK"):
        H 3
        return
    H 30
    return