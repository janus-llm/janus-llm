def PSS50WS(PSSIEN, PSSFT, LIST):
    # PSSIEN - IEN of entry in 50
    # PSSFT - Free Text name in 50
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #        piece being returned.
    # Returns PSG node of 50
    import os

    # Variable definitions not provided, assuming they are assigned elsewhere

    if LIST == '':
        return

    os.system('k ^TMP($J,LIST)')

    if PSSIEN <= 0 and PSSFT == '':
        return

    if PSSIEN > 0:
        PSSIEN2 = os.system('$$FIND1^DIC(50,"","A","`"_PSSIEN,,,"")')
        os.system('k ^TMP("PSSP50",$J)')
        if PSSIEN2 <= 0:
            os.system('s ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND"')
            return
        os.system('s ^TMP($J,LIST,0)=1')
        os.system('k ^TMP("PSSP50",$J)')
        os.system('GETS^DIQ(50,+PSSIEN2,".01;2;3;12:16;20:25;31;51;52;301;302","IE","^TMP(""PSSP50"",$J)")')
        PSS = 0
        while PSS:
            os.system('SETWS')

    if PSSIEN != '':
        os.system('s ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND"')
        return

    if PSSFT != '':
        if PSSFT.find('??') != -1:
            os.system('LOOP')
        os.system('k ^TMP("DILIST",$J)')
        os.system('FIND^DIC(50,,"@;.01","QP",PSSFT,,"B",,,"")')
        if os.system('s +^TMP("DILIST",$J,0)=0'):
            os.system('s ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND"')
            return
        os.system('s ^TMP($J,LIST,0)=+^TMP("DILIST",$J,0)')
        PSSXX = 0
        while PSSXX:
            PSSIEN = os.system('+^TMP("DILIST",$J,PSSXX,0)')
            os.system('k ^TMP("PSSP50",$J)')
            os.system('GETS^DIQ(50,+PSSIEN,".01;2;3;12:16;20:25;31;51;52;301;302","IE","^TMP(""PSSP50"",$J)")')
            PSS = 0
            while PSS:
                os.system('SETWS')

    os.system('k ^TMP("DILIST",$J),^TMP("PSSP50",$J)')


def SETWS():
    os.system('s ^TMP($J,LIST,+PSS(1),.01)=$G(^TMP("PSSP50",$J,50,PSS(1),.01,"I"))')
    os.system('s ^TMP($J,LIST,"B",$G(^TMP("PSSP50",$J,50,PSS(1),.01,"I")),+PSS(1))=""')
    os.system('s ^TMP($J,LIST,+PSS(1),2)=$G(^TMP("PSSP50",$J,50,PSS(1),2,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),3)=$G(^TMP("PSSP50",$J,50,PSS(1),3,"I"))')
    PSSUTN = os.system('$G(^TMP("PSSP50",$J,50,PSS(1),12,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),12)=$S($G(PSSUTN)="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),12,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),12,"E")))')
    if PSSUTN != '':
        os.system('s ^TMP($J,LIST,+PSS(1),12)=^TMP($J,LIST,+PSS(1),12)+"^"+$P($G(^DIC(51.5,PSSUTN,0)),"^",2)')
    os.system('s ^TMP($J,LIST,+PSS(1),13)=$G(^TMP("PSSP50",$J,50,PSS(1),13,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),14.5)=$G(^TMP("PSSP50",$J,50,PSS(1),14.5,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),15)=$G(^TMP("PSSP50",$J,50,PSS(1),15,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),16)=$G(^TMP("PSSP50",$J,50,PSS(1),16,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),20)=$S($G(^TMP("PSSP50",$J,50,PSS(1),20,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),20,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),20,"E")))')
    os.system('s ^TMP($J,LIST,+PSS(1),21)=$G(^TMP("PSSP50",$J,50,PSS(1),21,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),22)=$S($G(^TMP("PSSP50",$J,50,PSS(1),22,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),22,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),22,"E")))')
    os.system('s ^TMP($J,LIST,+PSS(1),23)=$S($G(^TMP("PSSP50",$J,50,PSS(1),23,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),23,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),23,"E")))')
    os.system('s ^TMP($J,LIST,+PSS(1),25)=$S($G(^TMP("PSSP50",$J,50,PSS(1),25,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),25,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),25,"E"))+"^"+$P($G(^PS(50.605,+^TMP("PSSP50",$J,50,PSS(1),25,"I"),0)),"^",2))')
    os.system('s ^TMP($J,LIST,+PSS(1),31)=$G(^TMP("PSSP50",$J,50,PSS(1),31,"I"))')
    os.system('s ^TMP($J,LIST,+PSS(1),51)=$S($G(^TMP("PSSP50",$J,50,PSS(1),51,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),51,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),51,"E")))')
    os.system('s ^TMP($J,LIST,+PSS(1),52)=$S($G(^TMP("PSSP50",$J,50,PSS(1),52,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),52,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),52,"E")))')
    os.system('s ^TMP($J,LIST,+PSS(1),301)=$S($G(^TMP("PSSP50",$J,50,PSS(1),301,"I"))="":"",1:$G(^TMP("PSSP50",$J,50,PSS(1),301,"I"))+"^"+$G(^TMP("PSSP50",$J,50,PSS(1),301,"E")))')
    os.system('s ^TMP($J,LIST,+PSS(1),302)=$G(^TMP("PSSP50",$J,50,PSS(1),302,"I"))')


def LOOP():
    import os

    os.system('D FIELD^DID(50,51,"Z","POINTER","PSS50D13","PSS50E13")')
    PSS51NFD = os.system('$G(PSS50D13("POINTER"))')
    os.system('D FIELD^DID(50,52,"Z","POINTER","PSS50D14","PSS50E14")')
    PSS52NFD = os.system('$G(PSS50D14("POINTER"))')
    os.system('D FIELD^DID(50,301,"Z","POINTER","PSS50D15","PSS50E15")')
    PSSG2N = os.system('$G(PSS50D15("POINTER"))')

    os.system('s PSSENCT=0')

    PSS = 0
    while PSS:
        if PSS51NF != '' and PSS51NFD != '' and PSS51NFD.find(PSS51NF + ':') != -1:
            os.system('s ^TMP($J,LIST,+PSS(1),51)=PSS51NF+"^"+$P($E(PSS51NFD,$F(PSS51NFD,(PSS51NF+":")),999),";")')
        else:
            os.system('s ^TMP($J,LIST,+PSS(1),51)=""')

        if PSS52NF != '' and PSS52NFD != '' and PSS52NFD.find(PSS52NF + ':') != -1:
            os.system('s ^TMP($J,LIST,+PSS(1),52)=PSS52NF+"^"+$P($E(PSS52NFD,$F(PSS52NFD,(PSS52NF+":")),999),";")')
        else:
            os.system('s ^TMP($J,LIST,+PSS(1),52)=""')

        if PSSG2 != '' and PSSG2N != '' and PSSG2N.find(PSSG2 + ':') != -1:
            os.system('s ^TMP($J,LIST,+PSS(1),301)=PSSG2+"^"+$P($E(PSSG2N,$F(PSSG2N,(PSSG2+":")),999),";")')
        else:
            os.system('s ^TMP($J,LIST,+PSS(1),301)=""')

        os.system('s ^TMP($J,LIST,+PSS(1),302)=$P(PSSG2NOD,"^",3)')

        os.system('SETWSLP')
        os.system('s PSSENCT=PSSENCT+1')

    os.system('s ^TMP($J,LIST,0)=$S($G(PSSENCT):$G(PSSENCT),1:"-1^NO DATA FOUND")')


def SETWSLP():
    os.system('s ^TMP($J,LIST,+PSS(1),.01)=$P(PSSZNODE,"^")')
    os.system('s ^TMP($J,LIST,"B",$P(PSSZNODE,"^"),+PSS(1))=""')
    os.system('s ^TMP($J,LIST,+PSS(1),2)=$P(PSSZNODE,"^",2)')
    os.system('s ^TMP($J,LIST,+PSS(1),3)=$P(PSSZNODE,"^",3)')
    os.system('s ^TMP($J,LIST,+PSS(1),12)=$S($P(PSS660,"^",2):$P(PSS660,"^",2)+"^"+$P($G(^DIC(51.5,+$P(PSS660,"^",2),0)),"^")+"^"+$P($G(^(0)),"^",2),1:"")')
    os.system('s ^TMP($J,LIST,+PSS(1),13)=$P(PSS660,"^",3)')
    os.system('s ^TMP($J,LIST,+PSS(1),14.5)=$P(PSS660,"^",8)')
    os.system('s ^TMP($J,LIST,+PSS(1),15)=$P(PSS660,"^",5)')
    os.system('s ^TMP($J,LIST,+PSS(1),16)=$P(PSS660,"^",6)')
    os.system('s ^TMP($J,LIST,+PSS(1),20)=$S($P(PSSNDNOD,"^"):$P(PSSNDNOD,"^")+"^"+$P($G(^PSNDF(50.6,+$P(PSSNDNOD,"^"),0)),"^"),1:"")')
    os.system('s ^TMP($J,LIST,+PSS(1),21)=$P(PSSNDNOD,"^",2)')
    os.system('s ^TMP($J,LIST,+PSS(1),22)=$S($P(PSSNDNOD,"^",3):$P(PSSNDNOD,"^",3)+"^"+$P($G(^PSNDF(50.68,+$P(PSSNDNOD,"^",3),0)),"^"),1:"")')
    os.system('s ^TMP($J,LIST,+PSS(1),23)=$S($P(PSSNDNOD,"^",4):$P(PSSNDNOD,"^",4)+"^"+$P($G(^PS(50.609,+$P(PSSNDNOD,"^",4),0)),"^"),1:"")')
    os.system('s ^TMP($J,LIST,+PSS(1),25)=$S($P(PSSNDNOD,"^",6):$P(PSSNDNOD,"^",6)+"^"+$P($G(^PS(50.605,+$P(PSSNDNOD,"^",6),0)),"^")+"^"+$P($G(^(0)),"^",2),1:"")')
    os.system('s ^TMP($J,LIST,+PSS(1),31)=$P(PSS2NODE,"^",4)')