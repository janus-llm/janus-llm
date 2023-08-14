def SCHED(PSSWIEN, PSSARRY):
    """
    Receive ward IEN from CPRS and return list of schedules.

    PSSWIEN   = Ward IEN
    PSSARRY   = array passed by reference from CPRS
    """
    import os
    import tempfile

    # If there is a duplicate schedule, and if one of them contains
    # ward-specific admin times for the ward location of the patient,
    # the schedule returned for inclusion in the list of selectable
    # schedules to CPRS will be the one with the ward-specific admin
    # times.  If neither duplicate has ward-specific admin times,
    # then the current functionality of the schedule with the lowest
    # IEN number will remain in place.  If both (or more than one)
    # duplicate schedules have ward-specific admin times for the ward
    # location of the patient, then the one with the lowest IEN number
    # will be the schedule returned to CPRS.

    # Example:  Patient's ward location is ICU
    # ^PS(51.1,"APPSJ","BID",1)=""
    # ^PS(51.1,"APPSJ","BID",2)=""

    # If ^PS(51.1,1 does not have ward-specific admin times for
    # the ICU, but ^PS(51.1,2 does, ^PS(51.1,2 will be in the list
    # of schedules returned to CPRS.

    # If neither schedule has ward-specific admin times for the ICU
    # then ^PS(51.1,1 will be in the list of schedules returned to CPRS.

    # If both schedules have ward-specific admin times for the ICU
    # then ^PS(51.1,1 will be in the list of schedules returned to CPRS.

    # The returned array to CPRS will be in the format:
    # PSSARRY(n)=IEN^NAME^OUTPATIENT EXPANSION^SCHEDULE TYPE^ADMIN TIME

    PSSSKED = ""
    os.makedirs(tempfile.gettempdir(), exist_ok=True)
    tmp_file = os.path.join(tempfile.gettempdir(), "PSSADMIN.tmp")
    try:
        with open(tmp_file, "w") as f:
            f.write(f"PSSWIEN={PSSWIEN}\n")
            f.write("PSSSKED=\"\"\n")
            f.write("K ^TMP(\"PSSADMIN\"),^TMP(\"PSSDUP\")\n")
            f.write("I $G(PSSWIEN)=\"\" S PSSWIEN=0\n")
            f.write("F  S PSSSKED=$O(^PS(51.1,\"APPSJ\",PSSSKED)) Q:PSSSKED=\"\"  D\n")
            f.write(" . S PSSSKED1=\"\",PSSSK=1\n")
            f.write(" . F  S PSSSKED1=$O(^PS(51.1,\"APPSJ\",PSSSKED,PSSSKED1)) Q:PSSSKED1=\"\"  D\n")
            f.write(" . . Q:$P($G(^PS(51.1,PSSSKED1,0)),\"^\",5)=\"\"\n")
            f.write(" . . Q:$$GET1^DIQ(51.1,PSSSKED1,12,\"I\")  ;Schedule is marked Inactive\n")
            f.write(" . . S ^TMP(\"PSSDUP\",PSSSKED,PSSSK)=PSSSKED1  ;Identify duplicate schedules to work with.\n")
            f.write(" . . S ^TMP(\"PSSADMIN\",\"STD\",PSSSKED,PSSSKED1)=$S($P($G(^PS(51.1,PSSSKED1,1,PSSWIEN,0)),\"^\",2)'=\"\":$P($G(^PS(51.1,PSSSKED1,1,PSSWIEN,0)),\"^\",2),1:$P($G(^PS(51.1,PSSSKED1,0)),\"^\",2))\n")
            f.write(" . . S PSSSK=PSSSK+1\n")
            f.write(" I '$D(^TMP(\"PSSDUP\")) D FORMAT,KILL Q  ;No duplicates in the schedule file - format for proper return to CPRS\n")
            f.write(" D DUP,FORMAT,KILL Q  ;Duplicate schedules - determine if any have ward-specific admin times\n")
            f.write("K ^TMP(\"PSSADMIN\"),PSSSKED,PSSSKED1,PSSSK,PSSWIEN\n")
            f.write("DUP ;Compare duplicates to see if any have ward-specific admin times.\n")
            f.write(" S PSSSKED=\"\",PSSSKED1=\"\"\n")
            f.write(" F  S PSSSKED=$O(^TMP(\"PSSDUP\",PSSSKED)) Q:PSSSKED=\"\"  D\n")
            f.write(" . S PSSSK=\"\"\n")
            f.write(" . F  S PSSSK=$O(^TMP(\"PSSDUP\",PSSSKED,PSSSK)) Q:PSSSK=\"\"  D\n")
            f.write(" . . S PSSSKED1=$G(^TMP(\"PSSDUP\",PSSSKED,PSSSK))\n")
            f.write(" . . I '$D(^TMP(\"PSSADMIN\",\"STD\",PSSSKED)) S ^TMP(\"PSSADMIN\",\"STD\",PSSSKED,PSSSKED1)=$P($G(^PS(51.1,PSSSKED1,0)),\"^\",2)\n")
            f.write(" . . I '$D(^PS(51.1,PSSSKED1,1,PSSWIEN,0)),PSSSK>1 K ^TMP(\"PSSADMIN\",\"STD\",PSSSKED,PSSSKED1) Q\n")
            f.write(" . . I $D(^PS(51.1,PSSSKED1,1,PSSWIEN,0)),'$D(^TMP(\"PSSADMIN\",\"WARD\",PSSSKED)) S ^TMP(\"PSSADMIN\",\"WARD\",PSSSKED,PSSSKED1)=$P($G(^PS(51.1,PSSSKED1,1,PSSWIEN,0)),\"^\",2)\n")
            f.write(" . . I $D(^TMP(\"PSSADMIN\",\"WARD\",PSSSKED)) D  Q\n")
            f.write(" . . . K ^TMP(\"PSSADMIN\",\"STD\",PSSSKED)\n")
            f.write(" . . . S ^TMP(\"PSSADMIN\",\"STD\",PSSSKED,PSSSKED1)=$G(^TMP(\"PSSADMIN\",\"WARD\",PSSSKED,PSSSKED1))\n")
            f.write(" . . . K ^TMP(\"PSSADMIN\",\"WARD\",PSSSKED)\n")
            f.write(" K ^TMP(\"PSSDUP\")\n")
            f.write("FORMAT ;Format array for proper return to CPRS\n")
            f.write(" N PSSCNTR,PSSTMP,PSSEXP,PSSEXP1\n")
            f.write(" S PSSSKED=\"\",PSSSKED1=\"\",PSSCNTR=1\n")
            f.write(" F  S PSSSKED=$O(^TMP(\"PSSADMIN\",\"STD\",PSSSKED)) Q:PSSSKED=\"\"  D\n")
            f.write(" . F  S PSSSKED1=$O(^TMP(\"PSSADMIN\",\"STD\",PSSSKED,PSSSKED1)) Q:PSSSKED1=\"\"  D\n")
            f.write(" . . S PSSTMP=$G(^PS(51.1,PSSSKED1,0))\n")
            f.write(" . . S PSSEXP=$P(PSSTMP,\"^\",8) I PSSEXP=\"\",$T(SCHE^PSOSIG)]\"\" S PSSEXP1=$$SCHE^PSOSIG(PSSSKED) S:PSSEXP1'=PSSSKED PSSEXP=PSSEXP1\n")
            f.write(" . . S PSSARRY(PSSCNTR)=PSSSKED1_\"^\"_PSSSKED_\"^\"_PSSEXP_\"^\"_$P(PSSTMP,\"^\",5)_\"^\"_$G(^TMP(\"PSSADMIN\",\"STD\",PSSSKED,PSSSKED1))\n")
            f.write(" . . S PSSCNTR=PSSCNTR+1\n")
            f.write(" K PSSCNTR,PSSTMP\n")

        # Run the generated MUMPS code using GT.M or Cache
        os.system(f"mumps -run {tmp_file}")

    finally:
        # Clean up temporary file
        os.remove(tmp_file)

    return PSSARRY