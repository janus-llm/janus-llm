! *****************************************************************************
SUBROUTINE CENTROID(IT)
    ! *****************************************************************************
    
    INTEGER, INTENT(IN) :: IT
    INTEGER :: I, IXCEN, IYCEN, COUNT
    TYPE(NODE), POINTER :: C
    
    IXCEN=0
    IYCEN=0
    COUNT=0
    C => LIST_TAGGED%HEAD
    
    DO I = 1, LIST_TAGGED%NUM_NODES
       IF (C%BURNED) THEN
          C => C%NEXT
          CYCLE
       ENDIF
       IF (C%TIME_SUPPRESSED .GT. 0.) THEN
          C => C%NEXT
          CYCLE
       ENDIF
    
       COUNT = COUNT + 1
       IXCEN = IXCEN + C%IX
       IYCEN = IYCEN + C%IY
       C => C%NEXT
    ENDDO
    
    IF (COUNT .EQ. 0) COUNT = 1
    IXCEN=NINT(REAL(IXCEN)/REAL(COUNT))
    IYCEN=NINT(REAL(IYCEN)/REAL(COUNT))
    
    SUPP(IT)%IXCEN = IXCEN
    SUPP(IT)%IYCEN = IYCEN
    
    ! *****************************************************************************
    END SUBROUTINE CENTROID
    ! *****************************************************************************