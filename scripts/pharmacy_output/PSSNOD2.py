# PSSNOD2 ;BIR/TTH-Delete Node #2 Field #21 and #70 ;[ 01/15/98  1:26 PM ]
# ;;1.0;PHARMACY DATA MANAGEMENT;**4**;9/30/97
PSDX = 0
while True:
    PSDX = PSDX + 1
    if not PSDX in ^PS(55,"B"):
        break
    del ^PS(55,PSDX,2)

del DIU
DIU = 55.05
DIU(0) = "SD"
DIU2()

del DIK, DA
for DA in [21, 70]:
    DIK = "^DD(55,"
    DA(1) = 55
    DIK()

del DA, DIK, PSDX, X, Y