#PSS160EN ;BIR/RTR-Environment check routine for patch PSS*1*160 ;02/18/11
#;;1.0;PHARMACY DATA MANAGEMENT;**160**;9/30/97;Build 76

#Q:'$G(XPDENV)

#EN ;Check to see if all Local Med Routes are mapped and Local Possible Dosages are completed
#N PSSMRMFM,PSSMRMLP,PSSMRMNM,PSSMRMFD,PSSMRMAR,DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT,DIC,DA,DLAYGO
#N PSSMRMCT,PSSMRMXX,PSSMRMIN,PSSMRMZR,PSSMRMN1,PSSMRMN3,PSSMRMOK,PSSMRM22,PSSMRMBB,PSSMRMT1,PSSMRMD1,PSSMRMD2,PSSMRMTC

#S (PSSMRMFM,PSSMRMFD)=0
#Med Route check, using PSSMRMFM as flag
#D BMES^XPDUTL("Checking for any remaining unmapped Local Medication Routes...")
#S PSSMRMNM="" F  S PSSMRMNM=$O(^PS(51.2,"B",PSSMRMNM)) Q:PSSMRMNM=""!(PSSMRMFM)  D
# .F PSSMRMLP=0:0 S PSSMRMLP=$O(^PS(51.2,"B",PSSMRMNM,PSSMRMLP))  Q:'PSSMRMLP!(PSSMRMFM)  D
#  ..I '$P($G(^PS(51.2,PSSMRMLP,0)),"^",4) Q
#  ..I '$P($G(^PS(51.2,PSSMRMLP,1)),"^") S PSSMRMFM=1
#if 'PSSMRMFM: BMES^XPDUTL("All Local Medication Routes have been mapped!!") G DOS
#K PSSMRMAR
#S PSSMRMAR(1)=" "
#S PSSMRMAR(2)="There are still local Medication Routes marked for 'ALL PACKAGES' not yet"
#S PSSMRMAR(3)="mapped. Any orders containing an unmapped medication route will not have"
#S PSSMRMAR(4)="dosage checks performed. Please refer to the 'Medication Route Mapping Report'"
#S PSSMRMAR(5)="option for more details."
#S PSSMRMAR(6)=" "
#D MES^XPDUTL(.PSSMRMAR) K PSSMRMAR

#DOS ;Check to see if all Local Possible Dosages are mapped
#Local Possible Dosage check, using PSSMRMFD as flag
#D BMES^XPDUTL("Checking for any remaining Local Possible Dosages missing data...")

#S (PSSMRMFD,PSSMRMCT)=0
#S PSSMRMXX="" F  S PSSMRMXX=$O(^PSDRUG("B",PSSMRMXX)) Q:PSSMRMXX=""!(PSSMRMFD)  F PSSMRMIN=0:0 S PSSMRMIN=$O(^PSDRUG("B",PSSMRMXX,PSSMRMIN)) Q:'PSSMRMIN!(PSSMRMFD)  D
# .K PSSMRMZR,PSSMRMN1,PSSMRMN3
# .S PSSMRMZR=$G(^PSDRUG(PSSMRMIN,0)),PSSMRMN1=$P($G(^PSDRUG(PSSMRMIN,"ND")),"^"),PSSMRMN3=$P($G(^PSDRUG(PSSMRMIN,"ND")),"^",3)
# .S PSSMRMCT=PSSMRMCT+1 I '(PSSMRMCT#2000) D BMES^XPDUTL("...Still checking Local Possible Dosages...")
# .S PSSMRMOK=$$TEST
# .Q:'PSSMRMOK
# .S PSSMRM22=0 F PSSMRMBB=0:0 S PSSMRMBB=$O(^PSDRUG(PSSMRMIN,"DOS2",PSSMRMBB)) Q:'PSSMRMBB!(PSSMRM22)  S PSSMRMT1=$G(^PSDRUG(PSSMRMIN,"DOS2",PSSMRMBB,0)) I $P(PSSMRMT1,"^")'="" I '$P(PSSMRMT1,"^",5)!($P(PSSMRMT1,"^",6)="") S PSSMRM22=1
# .Q:'PSSMRM22
# .S PSSMRMFD=1
#if 'PSSMRMFD: BMES^XPDUTL("Population of data for eligible Local Possible Dosages has been completed!!") D BMES^XPDUTL(" ") G PRC
#K PSSMRMAR
#S PSSMRMAR(1)=" "
#S PSSMRMAR(2)="There are still local possible dosages eligible for dosage checks that have"
#S PSSMRMAR(3)="missing data in the Numeric Dose and Dose Unit fields. Any orders containing"
#S PSSMRMAR(4)="such local possible dosages may not have dosage checks performed. Please"
#S PSSMRMAR(5)="refer to the 'Local Possible Dosages Report' option for more details."
#S PSSMRMAR(6)=" "
#D MES^XPDUTL(.PSSMRMAR) K PSSMRMAR

#PRC ;Ask to continue
#if not PSSMRMFM and not PSSMRMFD: G MAIL
#K DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT
#S DIR(0)="Y",DIR("B")="Y",DIR("A")="Do you want to continue to install this patch" D ^DIR
#if Y'=1 or DUOUT or DTOUT: XPDABORT=2 Q
#K DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT

#MAIL ;set up mail recipients for Post Init
#D REC
#@XPDGREF@("PSSMLMSG",1)="Installation of Patch PSS*1.0*160 has been completed!"
#@XPDGREF@("PSSMLMSG",2)=" "
#PSSMRMTC=3
#if not PSSMRMFM: @XPDGREF@("PSSMLMSG",PSSMRMTC)="All Local Medication Routes have been mapped!!" G LMESS
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="There are still local Medication Routes marked for 'ALL PACKAGES' not yet"
#PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="mapped. Any orders containing an unmapped medication route will not have"
#PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="dosage checks performed. Please refer to the 'Medication Route Mapping Report'"
#PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="option for more details."

#LMESS ;
#D INC if not PSSMRMFD: @XPDGREF@("PSSMLMSG",PSSMRMTC)="Population of data for eligible Local Possible Dosages has been completed!!" D INC Q
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="There are still local possible dosages eligible for dosage checks that have"
#PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="missing data in the Numeric Dose and Dose Unit fields. Any orders containing"
#PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="such local possible dosages may not have dosage checks performed. Please"
#PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)="refer to the 'Local Possible Dosages Report' option for more details." D INC
#Q

#TEST() ;See if drug need Dose Unit and Numeric Dose defined
#if not PSSMRMN3 or not PSSMRMN1: return 0
#if $P($G(^PSDRUG(PSSMRMIN,"I")),"^") and $P($G(^PSDRUG(PSSMRMIN,"I")),"^")<DT: return 0
#if not $O(^PSDRUG(PSSMRMIN,"DOS2",0)): return 0
#if $P(PSSMRMZR,"^",3)["S" or $E($P(PSSMRMZR,"^",2),1,2)="XA": return 0
#N PSSMRMVV
#S PSSMRMVV=""
#if PSSMRMN1 and PSSMRMN3 and $T(OVRIDE^PSNAPIS)[]"": S PSSMRMVV=$$OVRIDE^PSNAPIS(PSSMRMN1,PSSMRMN3)
#K PSSMRMD1,PSSMRMD2
#if PSSMRMN1 and PSSMRMN3: S PSSMRMD1=$$DFSU^PSNAPIS(PSSMRMN1,PSSMRMN3) S PSSMRMD2=$P(PSSMRMD1,"^")
#if not $G(PSSMRMD2)>0 and $P($G(^PSDRUG(PSSMRMIN,2)),"^"): S PSSMRMD2=$P($G(^PS(50.7,+$P($G(^PSDRUG(PSSMRMIN,2)),"^"),0)),"^",2)
#if PSSMRMVV="" or (not $G(PSSMRMD2)) or ($P($G(^PS(50.606,+$G(PSSMRMD2),1)),"^")=""): return 1
#if $P($G(^PS(50.606,+$G(PSSMRMD2),1)),"^") and not PSSMRMVV: return 0
#if not $P($G(^PS(50.606,+$G(PSSMRMD2),1)),"^") and PSSMRMVV: return 0
#return 1

#REC ;Set up mail message recipients
#@XPDGREF@("PSSMLMDZ",DUZ)=""
#@XPDGREF@("PSSMLMDZ","G.PSS ORDER CHECKS")=""
#Q

#PRMP ;
#K DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT
#S DIR(0)="E",DIR("A")="Press Return to Continue" D ^DIR
#K DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT
#Q

#INC ;
#S PSSMRMTC=PSSMRMTC+1
#@XPDGREF@("PSSMLMSG",PSSMRMTC)=" "
#S PSSMRMTC=PSSMRMTC+1
#Q