# BIR/RTR-Data used to populate Dose Unit and Numeric Dose
# 02/12/09
# 1.0;PHARMACY DATA MANAGEMENT;**117**;9/30/97;Build 101

# Initialize the temporary storage variables
# ^TMP($J,"PSSQVCS2"), ^TMP($J,"PSSQVCS4"), ^TMP($J,"PSSQVCS5")
PSSQVCAA = 1
PSSQVCBB = $T(SET4+PSSQVCAA)
while $P(PSSQVCBB, ";;", 2) != "":
    ^TMP($J,"PSSQVCS4",$P(PSSQVCBB,";;",2)) = $P(PSSQVCBB,";;",3)_"^"_$P(PSSQVCBB,";;",4)
    PSSQVCAA += 1
    PSSQVCBB = $T(SET4+PSSQVCAA)

PSSQVCCC = 1
PSSQVCDD = $T(SET2+PSSQVCCC)
while $P(PSSQVCDD, ";;", 2) != "":
    ^TMP($J,"PSSQVCS2",$P(PSSQVCDD,";;",2),$P(PSSQVCDD,";;",3)) = $P(PSSQVCDD,";;",4)_"^"_$P(PSSQVCDD,";;",5)
    PSSQVCCC += 1
    PSSQVCDD = $T(SET2+PSSQVCCC)

# Call the PSSDSBDB routine
^PSSDSBDB