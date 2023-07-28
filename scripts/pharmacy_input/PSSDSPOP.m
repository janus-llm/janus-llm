PSSDSPOP ;BIR/RTR-Populate Dose Unit and Numeric Dose on PSS*1*129 install ;05/03/08
 ;;1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/07;Build 67
 ;
 ;Called from PSSPO129 to auto-populate Dose unit and numeric Dose Fields in File 50
 ;
ENX ;
 Q
 ;
 ;
TEST(PSSVWIEN) ;Test to see if Numeric Dose and Dose Unit should be prompted for
 ;In Drug Enter/Edit and Dosage Enter/Options
 N PSSVWND1,PSSVWND3,PSSVWZR,PSSVWDOV,PSSVWNDF,PSSVWDF
 S PSSVWZR=$G(^PSDRUG(+PSSVWIEN,0))
 I $P(PSSVWZR,"^",3)["S"!($E($P(PSSVWZR,"^",2),1,2)="XA") Q 0
 S PSSVWND1=$P($G(^PSDRUG(+PSSVWIEN,"ND")),"^"),PSSVWND3=$P($G(^PSDRUG(+PSSVWIEN,"ND")),"^",3)
 S PSSVWDOV=""
 I PSSVWND1,PSSVWND3,$T(OVRIDE^PSNAPIS)]"" S PSSVWDOV=$$OVRIDE^PSNAPIS(PSSVWND1,PSSVWND3)
 I PSSVWND1,PSSVWND3 S PSSVWNDF=$$DFSU^PSNAPIS(PSSVWND1,PSSVWND3) S PSSVWDF=$P(PSSVWNDF,"^")
 I $G(PSSVWDF)'>0,$P($G(^PSDRUG(PSSVWIEN,2)),"^") S PSSVWDF=$P($G(^PS(50.7,+$P($G(^PSDRUG(PSSVWIEN,2)),"^"),0)),"^",2)
 I PSSVWDOV=""!('$G(PSSVWDF))!($P($G(^PS(50.606,+$G(PSSVWDF),1)),"^")="") Q 1
 I $P($G(^PS(50.606,+$G(PSSVWDF),1)),"^"),'PSSVWDOV Q 0
 I '$P($G(^PS(50.606,+$G(PSSVWDF),1)),"^"),PSSVWDOV Q 0
 Q 1
 ;
 ;
MS ;Called from Drug Enter Edit and Dose Enter Edit
 N PSSVWX,PSSVWXX,X,Y,DIR,DTOUT,DUOUT,DIRUT,DIROUT
 S PSSVWX=$S($E($G(PSSNATST),1)=".":"0"_$G(PSSNATST),1:$G(PSSNATST))
 S PSSVWXX=$S($E($P($G(^PSDRUG(PSSIEN,"DOS")),"^"),1)=".":"0"_$P($G(^PSDRUG(PSSIEN,"DOS")),"^"),1:$P($G(^PSDRUG(PSSIEN,"DOS")),"^"))
 I PSSVWX'="",PSSVWXX'="",PSSVWX'=PSSVWXX W !!,"Please note: Strength of drug does not match strength of VA Product it is",!,"matched to." D
 .I $G(PSSDESTP) K DIR W ! S DIR(0)="E",DIR("A")="Press Return to Continue" D ^DIR K DIR
 Q
 ;
EN ;
 ;Finish adding data
 D ^PSSDSDAT
 N PSSQVNMX,PSSQVIEN,PSSQVZR,PSSQVND1,PSSQVND3,PSSQVTOT,PSSQVOK,PSSQVLPX,PSSQVLC1,PSSQVLCD,PSSQVDF1,PSSQVDF2,PSSQVDF3,PSSQVFZ,PSSQVMUL
 N X,Y,DIC,DTOUT,DLAYGO,PSSQVDF4,PSSQVDF5,PSSQVDF6,PSSQVDF7,PSSQVQT,PSSQVDF8,PSSQV9,PSSQVNUM,PSSQVRSL,PSSQVFNC,PSSQVFNX,PSSQVNDF,PSSQVDF
 N PSSQVXF4,PSSQVXF5,PSSQVXF6,PSSQVXF7,PSSQVXF8,PSSQVXF9,PSSQVFL9,PSSQVFL8,PSSQVFZA
 S PSSQVTOT=0
 S PSSQVNMX="" F  S PSSQVNMX=$O(^PSDRUG("B",PSSQVNMX)) Q:PSSQVNMX=""  F PSSQVIEN=0:0 S PSSQVIEN=$O(^PSDRUG("B",PSSQVNMX,PSSQVIEN)) Q:'PSSQVIEN  D
 .K PSSQVZR,PSSQVND1,PSSQVND3,PSSQVOK,PSSQVLPX,PSSQVLC1,PSSQVLCD,PSSQVDF1,PSSQVDF2,PSSQVDF3
 .S PSSQVZR=$G(^PSDRUG(PSSQVIEN,0)),PSSQVND1=$P($G(^PSDRUG(PSSQVIEN,"ND")),"^"),PSSQVND3=$P($G(^PSDRUG(PSSQVIEN,"ND")),"^",3)
 .S PSSQVTOT=PSSQVTOT+1 I '(PSSQVTOT#1000) D BMES^XPDUTL("...still mapping Local Possible Dosages...")
 .K PSSQVNDF,PSSQVDF,PSSQVFZ
 .S PSSQVFZ=""
 .S PSSQVOK=$$TESTX
 .Q:'PSSQVOK
 .I $G(PSSQVDF) S PSSQVFZ=$P($G(^PS(50.606,PSSQVDF,0)),"^")
 .L +^PSDRUG(PSSQVIEN):$S($G(DILOCKTM)>0:DILOCKTM,1:3) I '$T Q
 .F PSSQVLPX=0:0 S PSSQVLPX=$O(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX)) Q:'PSSQVLPX  S PSSQVLC1=$G(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0)) I $P(PSSQVLC1,"^")'="" I '$P(PSSQVLC1,"^",5),($P(PSSQVLC1,"^",6)="") D
 ..S PSSQVLCD=$$UP^XLFSTR($P(PSSQVLC1,"^"))
 ..K PSSQVDF1,PSSQVDF2,PSSQVDF3,PSSQVQT
 ..S PSSQVQT=0
 ..;
 ..;
 ..;Condition Set 4 (Part 1)
 ..I $D(^TMP($J,"PSSQVCS4",PSSQVLCD)) D  K Y
 ...S PSSQVQT=1
 ...S PSSQVDF1=$P(^TMP($J,"PSSQVCS4",PSSQVLCD),"^"),PSSQVDF2=$P(^TMP($J,"PSSQVCS4",PSSQVLCD),"^",2)
 ...S PSSQVDF3=$$DFIND(PSSQVDF2) I PSSQVDF3,PSSQVDF1 D
 ....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVDF3
 ....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVDF1
 ..Q:PSSQVQT
 ..;
 ..;
 ..;Condition Set 4 (Part 2)
 ..D CS4
 ..Q:PSSQVQT
 ..;
 ..;
 ..;Condition Set 1
 ..I $P($G(PSSQVNDF),"^",4)'="",$P($G(PSSQVNDF),"^",6)'="" D
 ...I PSSQVFZ["TAB"!(PSSQVFZ["CAP")!(PSSQVFZ="GUM,CHEWABLE")!(PSSQVFZ="IMPLANT")!(PSSQVFZ="LOZENGE")!(PSSQVFZ="SUPP,RTL")!(PSSQVFZ="TROCHE")!(PSSQVFZ="INJ/IMPLANT") D
 ....I $P(PSSQVNDF,"^",6)="MG"!($P(PSSQVNDF,"^",6)="MCG")!($P(PSSQVNDF,"^",6)="UNT")!($P(PSSQVNDF,"^",6)="GM")!($P(PSSQVNDF,"^",6)="MEQ") D
 .....S PSSQVQT=1
 .....K PSSQVDF4,PSSQVDF5,PSSQVDF6,PSSQVDF7,PSSQVDF8,PSSQVMUL
 .....S PSSQVDF4=$P($G(^PSDRUG(PSSQVIEN,"DOS")),"^"),PSSQVDF5=$P($G(^PSDRUG(PSSQVIEN,"DOS")),"^",2)
 .....I PSSQVDF5 K X S X=$P($G(^PS(50.607,PSSQVDF5,0)),"^") I X'="" S PSSQVDF6=$$DFIND(X)
 .....I '$G(PSSQVDF6) K X S X=$P(PSSQVNDF,"^",6) S PSSQVDF6=$$DFIND(X)
 .....K Y,X I '$G(PSSQVDF6) Q
 .....S PSSQVDF7=$S($G(PSSQVDF4)'="":$G(PSSQVDF4),$P(PSSQVNDF,"^",4)'="":$P(PSSQVNDF,"^",4),1:"")
 .....I PSSQVDF7'?.N&(PSSQVDF7'?.N1".".N) K PSSQVDF7
 .....Q:$G(PSSQVDF7)=""
 .....S PSSQVDF8=$$NUM^PSSDSPON
 .....Q:'PSSQVDF8
 .....S PSSQVMUL=PSSQVDF8*PSSQVDF7
 .....K:+PSSQVMUL'=PSSQVMUL!(PSSQVMUL>99999999999999)!(PSSQVMUL<.00001)!(PSSQVMUL?.E1"."6N.N) PSSQVMUL
 .....I '$G(PSSQVMUL) Q
 .....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVDF6
 .....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVMUL
 ..Q:$G(PSSQVQT)
 ..;
 ..;
 ..;Condition Set 2
 ..I $P($G(PSSQVNDF),"^",4)'="",$P($G(PSSQVNDF),"^",6)'="" D
 ...K PSSQV9,PSSQVFL8,PSSQVFZA
 ...S PSSQV9=$P(PSSQVNDF,"^",6)
 ...I PSSQVFZ="ELIXIR"!(PSSQVFZ="LIQUID")!(PSSQVFZ="LIQUID,ORAL")!(PSSQVFZ="PWDR,RENST-ORAL")!(PSSQVFZ="SOLN,CONC")!(PSSQVFZ="SOLN,ORAL")!(PSSQVFZ="SUSP")!(PSSQVFZ="SUSP,ORAL")!(PSSQVFZ="SYRUP")!(PSSQVFZ="SYRUP,ORAL") S PSSQVFZA=1
 ...I PSSQVFZ="INJ"!(PSSQVFZ="INJ,SOLN") S PSSQVFZA=1
 ...I $G(PSSQVFZA) D
 ....I PSSQV9="GM/ML"!(PSSQV9="GM/1ML")!(PSSQV9="GM/5ML")!(PSSQV9="GM/10ML")!(PSSQV9="GM/15ML")!(PSSQV9="GM/30ML") S PSSQVFL8=1
 ....I PSSQV9="MG/ML"!(PSSQV9="MG/1ML")!(PSSQV9="MG/5ML")!(PSSQV9="MG/10ML")!(PSSQV9="MG/15ML")!(PSSQV9="MG/30ML")!(PSSQV9="MEQ/ML")!(PSSQV9="MEQ/1ML")!(PSSQV9="MEQ/5ML")!(PSSQV9="MEQ/10ML")!(PSSQV9="MEQ/15ML")!(PSSQV9="MEQ/30ML") S PSSQVFL8=1
 ....I $G(PSSQVFL8) D
 .....S PSSQVQT=1
 .....K PSSQVXF4,PSSQVXF5,PSSQVXF6,PSSQVXF7,PSSQVXF8,PSSQVXF9,PSSQVNUM,PSSQVFL9
 .....S PSSQVXF4=$P($G(^PSDRUG(PSSQVIEN,"DOS")),"^"),PSSQVXF5=$P($G(^PSDRUG(PSSQVIEN,"DOS")),"^",2)
 .....I PSSQVXF5 K X S X=$P($G(^PS(50.607,PSSQVXF5,0)),"^") D
 ......S PSSQVFL9=0
 ......I X="GM/ML"!(X="GM/1ML")!(X="GM/5ML")!(X="GM/10ML")!(X="GM/15ML")!(X="GM/30ML") S PSSQVFL9=1
 ......I X="MG/ML"!(X="MG/1ML")!(X="MG/5ML")!(X="MG/10ML")!(X="MG/15ML")!(X="MG/30ML")!(X="MEQ/ML")!(X="MEQ/1ML")!(X="MEQ/5ML")!(X="MEQ/10ML")!(X="MEQ/15ML")!(X="MEQ/30ML") S PSSQVFL9=1
 ......Q:'PSSQVFL9
 ......S PSSQVXF8=$P(X,"/") S PSSQVNUM=+$P(X,"/",2) S PSSQVXF6=$$DFIND(PSSQVXF8)
 .....I '$G(PSSQVXF6) K PSSQVNUM,PSSQVXF6 K X S X=PSSQV9 S PSSQVXF9=$P(X,"/") S PSSQVXF6=$$DFIND(PSSQVXF9) S PSSQVNUM=+$P(PSSQV9,"/",2)
 .....I '$G(PSSQVXF6) Q
 .....I PSSQVNUM'=0,PSSQVNUM'=1,PSSQVNUM'=5,PSSQVNUM'=10,PSSQVNUM'=15,PSSQVNUM'=30 Q
 .....I PSSQVNUM=0 S PSSQVNUM=1
 .....S PSSQVXF7=$S($G(PSSQVXF4)'="":$G(PSSQVXF4),$P(PSSQVNDF,"^",4)'="":$P(PSSQVNDF,"^",4),1:"")
 .....I PSSQVXF7'?.N&(PSSQVXF7'?.N1".".N) K PSSQVXF7
 .....Q:$G(PSSQVXF7)=""
 .....I '$D(^TMP($J,"PSSQVCS2",PSSQVLCD,PSSQVNUM)) Q
 .....K PSSQVFNX,PSSQVRSL,PSSQVFNC
 .....S PSSQVRSL=$P(^TMP($J,"PSSQVCS2",PSSQVLCD,PSSQVNUM),"^"),PSSQVFNC=$P(^TMP($J,"PSSQVCS2",PSSQVLCD,PSSQVNUM),"^",2)
 .....I PSSQVFNC="M" S PSSQVFNX=PSSQVXF7*PSSQVRSL
 .....I PSSQVFNC="D" S PSSQVFNX=PSSQVXF7/PSSQVRSL
 .....Q:$G(PSSQVFNX)=""
 .....I +PSSQVFNX'=PSSQVFNX!(PSSQVFNX>99999999999999)!(PSSQVFNX<.00001)!(PSSQVFNX?.E1"."6N.N) Q
 .....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVXF6
 .....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVFNX
 ..Q:$G(PSSQVQT)
 ..;
 ..;
 ..;Condition Set 3
 ..I $P($G(PSSQVNDF),"^",4)'="",$P($G(PSSQVNDF),"^",6)'="" D
 ...N PSSQVPK1,PSSQVPK2,PSSQVPK3,PSSQVPK4,PSSQVPK5,PSSQVPK6,PSSQVPK7,PSSQVPK8,PSSQVPK9,PSSQVPKZ,PSSQVPKA,PSSQVPKB
 ...S PSSQVPK1=$P(PSSQVNDF,"^",6)
 ...S PSSQVPK3=0 F PSSQVPK2=1:1:$L(PSSQVPK1) I $E(PSSQVPK1,PSSQVPK2)="/" S PSSQVPK3=PSSQVPK3+1
 ...I PSSQVPK3=1,$P(PSSQVPK1,"/",2)="PKT" D
 ....S PSSQVQT=1
 ....S PSSQVPK4=$P($G(^PSDRUG(PSSQVIEN,"DOS")),"^"),PSSQVPK5=$P($G(^PSDRUG(PSSQVIEN,"DOS")),"^",2)
 ....K PSSQVPK6,PSSQVPK7,PSSQVPK8,PSSQVPK9,PSSQVPKZ,PSSQVPKA,PSSQVPKB
 ....I PSSQVPK5 S PSSQVPK6=$P($G(^PS(50.607,PSSQVPK5,0)),"^") D
 .....S PSSQVPK3=0 F PSSQVPK2=1:1:$L(PSSQVPK6) I $E(PSSQVPK6,PSSQVPK2)="/" S PSSQVPK3=PSSQVPK3+1
 .....I PSSQVPK3=1,$P(PSSQVPK6,"/",2)="PKT" S PSSQVPK7=$P(PSSQVPK6,"/") S PSSQVPK8=$$DFIND(PSSQVPK7)
 ....I '$G(PSSQVPK8) K PSSQVPK8 S PSSQVPK9=$P(PSSQVPK1,"/") S PSSQVPK8=$$DFIND(PSSQVPK9)
 ....I '$G(PSSQVPK8) Q
 ....S PSSQVPKZ=$S($G(PSSQVPK4)'="":$G(PSSQVPK4),$P(PSSQVNDF,"^",4)'="":$P(PSSQVNDF,"^",4),1:"")
 ....I PSSQVPKZ'?.N&(PSSQVPKZ'?.N1".".N) K PSSQVPKZ
 ....Q:$G(PSSQVPKZ)=""
 ....S PSSQVPKB=$$NUM^PSSDSPON
 ....Q:'PSSQVPKB
 ....S PSSQVPKA=PSSQVPKZ*PSSQVPKB
 ....I +PSSQVPKA'=PSSQVPKA!(PSSQVPKA>99999999999999)!(PSSQVPKA<.00001)!(PSSQVPKA?.E1"."6N.N) Q
 ....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVPK8
 ....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVPKA
 ..Q:$G(PSSQVQT)
 ..;
 ..;
 ..;Condition set 5
 ..I PSSQVND1,PSSQVND3,$P($G(PSSQVNDF),"^",4)="",$P($G(PSSQVNDF),"^",6)="" D
 ...I $D(^TMP($J,"PSSQVCS5",PSSQVLCD)) D
 ....N PSSQVF51,PSSQVF52,PSSQVF53
 ....S PSSQVF51=$P(^TMP($J,"PSSQVCS5",PSSQVLCD),"^"),PSSQVF52=$P(^TMP($J,"PSSQVCS5",PSSQVLCD),"^",2)
 ....S PSSQVF53=$$DFIND(PSSQVF52) I PSSQVF51,PSSQVF53 D
 .....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVF53
 .....S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVF51
 .D ULK
 K ^TMP($J,"PSSQVCS2")
 K ^TMP($J,"PSSQVCS4")
 K ^TMP($J,"PSSQVCS5")
 Q
 ;
ULK ;
 L -^PSDRUG(PSSQVIEN)
 Q
 ;
TESTX() ;See if drug needs Dose Unit and Numeric Dose defined
 I 'PSSQVND3!('PSSQVND1) Q 0
 I $P($G(^PSDRUG(PSSQVIEN,"I")),"^"),$P($G(^PSDRUG(PSSQVIEN,"I")),"^")<DT Q 0
 N PSSQVDOV
 S PSSQVDOV=""
 I PSSQVND1,PSSQVND3,$T(OVRIDE^PSNAPIS)]"" S PSSQVDOV=$$OVRIDE^PSNAPIS(PSSQVND1,PSSQVND3)
 I '$O(^PSDRUG(PSSQVIEN,"DOS2",0)) Q 0
 I $P(PSSQVZR,"^",3)["S"!($E($P(PSSQVZR,"^",2),1,2)="XA") Q 0
 I PSSQVND1,PSSQVND3 S PSSQVNDF=$$DFSU^PSNAPIS(PSSQVND1,PSSQVND3) S PSSQVDF=$P(PSSQVNDF,"^")
 I $G(PSSQVDF)'>0,$P($G(^PSDRUG(PSSQVIEN,2)),"^") S PSSQVDF=$P($G(^PS(50.7,+$P($G(^PSDRUG(PSSQVIEN,2)),"^"),0)),"^",2)
 I PSSQVDOV=""!('$G(PSSQVDF))!($P($G(^PS(50.606,+$G(PSSQVDF),1)),"^")="") Q 1
 I $P($G(^PS(50.606,+$G(PSSQVDF),1)),"^"),'PSSQVDOV Q 0
 I '$P($G(^PS(50.606,+$G(PSSQVDF),1)),"^"),PSSQVDOV Q 0
 Q 1
 ;
CS4 ;
 I PSSQVLCD?.N1" UNITS" D CS4ST Q
 I PSSQVLCD?.N1" UNIT" D CS4ST Q
 I PSSQVLCD?.N1" UNIT(S)" D CS4ST Q
 I PSSQVLCD?.N1" UNT" D CS4ST Q
 I PSSQVLCD?.N1" UNT(S)" D CS4ST Q
 I PSSQVLCD?.N1" UNTS" D CS4ST Q
 I PSSQVLCD?.N1".".N1" UNITS" D CS4ST Q
 I PSSQVLCD?.N1".".N1" UNIT" D CS4ST Q
 I PSSQVLCD?.N1".".N1" UNIT(S)" D CS4ST Q
 I PSSQVLCD?.N1".".N1" UNT" D CS4ST Q
 I PSSQVLCD?.N1".".N1" UNT(S)" D CS4ST Q
 I PSSQVLCD?.N1".".N1" UNTS" D CS4ST Q
 D COMMA
 Q
 ;
CS4ST ;
 S PSSQVQT=1
 N PSSQVXXX,PSSQVD11,PSSQVD12
 S PSSQVXXX=+PSSQVLCD
 K:+PSSQVXXX'=PSSQVXXX!(PSSQVXXX>99999999999999)!(PSSQVXXX<.00001)!(PSSQVXXX?.E1"."6N.N) PSSQVXXX
 I '$G(PSSQVXXX) Q
 S PSSQVD12="UNIT(S)"
 S PSSQVD11=$$DFIND(PSSQVD12) I PSSQVD11 D
 .S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVD11
 .S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVXXX
 K Y
 Q
 ;
NUM() ;Only checking combinations of "one-half to one" and "one to two"
 ;** This section of code was only called in test v1, now uses routine PSSDSPON **
 ;Doing trailing space, because something like 10,000 Units (with comma), would have gotten by condition set 4
 ;Combinations of "one-half to one"
 I PSSQVLCD["ONE-HALF ",PSSQVLCD["ONE ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR " Q 1
 I PSSQVLCD["ONE HALF ",PSSQVLCD["ONE ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR " Q 1
 ;Removed PSSQVLCD'["2 " because 1/2 space would contain 2 space, is that ok, could probably remove 3 and 4
 I PSSQVLCD["1/2 ",PSSQVLCD["1 ",PSSQVLCD'["3 ",PSSQVLCD'["4 " Q 1
 ;Combinations of "one to two"
 I PSSQVLCD["ONE ",PSSQVLCD["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE-HALF " Q 2
 I PSSQVLCD["ONE ",PSSQVLCD["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE HALF " Q 2
 I PSSQVLCD["1 ",PSSQVLCD["2 ",PSSQVLCD'["3 ",PSSQVLCD'["4 ",PSSQVLCD'["1/2 " Q 2
 ;Checking for 0.5
 I PSSQVLCD["ONE-HALF ",PSSQVLCD'["ONE ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR " Q .5
 I PSSQVLCD["ONE HALF ",PSSQVLCD'["ONE ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR " Q .5
 ;Removed PSSQVLCD'["2 " because 1/2 space would contain 2 space, is that ok, could probably remove 3 and 4
 I PSSQVLCD["1/2 ",PSSQVLCD'["1 ",PSSQVLCD'["3 ",PSSQVLCD'["4 " Q .5
 ;Checking for 1
 I PSSQVLCD["ONE ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE-HALF " Q 1
 I PSSQVLCD["ONE ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE HALF " Q 1
 I PSSQVLCD["1 ",PSSQVLCD'["2 ",PSSQVLCD'["3 ",PSSQVLCD'["4 ",PSSQVLCD'["1/2 " Q 1
 ;Checking for 2
 I PSSQVLCD["TWO ",PSSQVLCD'["ONE ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE-HALF " Q 2
 I PSSQVLCD["TWO ",PSSQVLCD'["ONE ",PSSQVLCD'["THREE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE HALF " Q 2
 I PSSQVLCD["2 ",PSSQVLCD'["1 ",PSSQVLCD'["3 ",PSSQVLCD'["4 ",PSSQVLCD'["1/2 " Q 2
 ;Checking for 3
 I PSSQVLCD["THREE ",PSSQVLCD'["TWO ",PSSQVLCD'["ONE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE-HALF " Q 3
 I PSSQVLCD["THREE ",PSSQVLCD'["TWO ",PSSQVLCD'["ONE ",PSSQVLCD'["FOUR ",PSSQVLCD'["ONE HALF " Q 3
 I PSSQVLCD["3 ",PSSQVLCD'["2 ",PSSQVLCD'["1 ",PSSQVLCD'["4 ",PSSQVLCD'["1/2 " Q 3
 ;Checking for 4
 I PSSQVLCD["FOUR ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["ONE ",PSSQVLCD'["ONE-HALF " Q 4
 I PSSQVLCD["FOUR ",PSSQVLCD'["TWO ",PSSQVLCD'["THREE ",PSSQVLCD'["ONE ",PSSQVLCD'["ONE HALF " Q 4
 I PSSQVLCD["4 ",PSSQVLCD'["2 ",PSSQVLCD'["3 ",PSSQVLCD'["1 ",PSSQVLCD'["1/2 " Q 4
 Q 0
 ;
DFIND(PSSQVFND) ;Fine IEN, can't do DIC Lookup because of exact match check
 N PSSQVFN1
 S PSSQVFN1=$O(^PS(51.24,"B",PSSQVFND,0)) I PSSQVFN1,'$$SCREEN^XTID(51.24,.01,PSSQVFN1_",") Q PSSQVFN1
 S PSSQVFN1=$O(^PS(51.24,"C",PSSQVFND,0)) I PSSQVFN1,'$$SCREEN^XTID(51.24,.01,PSSQVFN1_",") Q PSSQVFN1
 S PSSQVFN1=$O(^PS(51.24,"D",PSSQVFND,0)) I PSSQVFN1,'$$SCREEN^XTID(51.24,.01,PSSQVFN1_",") Q PSSQVFN1
 Q 0
 ;
COMMA ;
 N PSSQVCM1,PSSQVCM2,PSSQVCM3,PSSQVCM4
 I PSSQVLCD'[" " Q
 S PSSQVCM1=$P(PSSQVLCD," ")
 S PSSQVCM3=$F(PSSQVLCD," ")
 S PSSQVCM2=$TR(PSSQVCM1,",","")
 S PSSQVCM4=PSSQVCM2_$E(PSSQVLCD,(PSSQVCM3-1),$L(PSSQVLCD))
 I PSSQVCM4?.N1" UNITS" D CS4ST1 Q
 I PSSQVCM4?.N1" UNIT" D CS4ST1 Q
 I PSSQVCM4?.N1" UNIT(S)" D CS4ST1 Q
 I PSSQVCM4?.N1" UNT" D CS4ST1 Q
 I PSSQVCM4?.N1" UNT(S)" D CS4ST1 Q
 I PSSQVCM4?.N1" UNTS" D CS4ST1 Q
 Q
 ;
CS4ST1 ;
 S PSSQVQT=1
 N PSSQVCM5,PSSQVCM6,PSSQVCM7
 S PSSQVCM5=+PSSQVCM4
 K:+PSSQVCM5'=PSSQVCM5!(PSSQVCM5>99999999999999)!(PSSQVCM5<.00001)!(PSSQVCM5?.E1"."6N.N) PSSQVCM5
 I '$G(PSSQVCM5) Q
 S PSSQVCM7="UNIT(S)"
 S PSSQVCM6=$$DFIND(PSSQVCM7) I PSSQVCM6 D
 .S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",5)=PSSQVCM6
 .S $P(^PSDRUG(PSSQVIEN,"DOS2",PSSQVLPX,0),"^",6)=PSSQVCM5
 K Y
 Q
