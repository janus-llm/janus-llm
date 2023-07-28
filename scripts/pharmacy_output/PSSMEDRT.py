def match():
    """
    Match File 51.2 Med Routes to Standard Med Routes
    Mainly for use only for the initial set up of the 0.5 Order Checks
    """
    print("\nThis option will find local Medication Routes marked for 'ALL PACKAGES' not")
    print("mapped to a Standard Medication Route, and prompt you to map the local route.")
    print("This mapping is necessary to perform Dosage checks.\n")
    print("Searching for unmapped Med Routes...\n")
    
    PSSMRLFL = 0
    PSSMRLP = ""
    
    while PSSMRLP != "" and not PSSMRLFL:
        for PSSMRLNN in range(0, len(PSSMRLP)):
            PSSMRLND = PSSMRLP[PSSMRLNN]
            
            if not PSSMRLND[3]:
                continue
            
            if PSSMRLND[4][0]:
                continue
            
            print("\nMapping local Med Route of '{}'\n".format(PSSMRLND[1]))
            
            if not lock_med_route(PSSMRLNN):
                print("\nAnother person is editing this Med Route.")
                response = input("\nDo you want to continue mapping Med Routes? (Y/N) ")
                
                if response != "Y":
                    PSSMRLFL = 1
                    break
            
            result = select_standard_med_route()
            
            if result:
                PSSMRLOK = result[0]
                
                update_med_route(PSSMRLNN, PSSMRLOK)
                
                PSSMRLAA = PSSMRLND[5]
                
                if not PSSMRLAA:
                    print("\nUnable to make this match!!")
                    response = input("\nDo you want to continue mapping Med Routes? (Y/N) ")
                    
                    if response != "Y":
                        PSSMRLFL = 1
                        break
                
                print("\nLocal Route: '{}' has been mapped to".format(PSSMRLND[1]))
                print("Stnd Route: '{}'   FDB Route: '{}'".format(PSSMRLAA[0], PSSMRLAA[1]))
                
                unlock_med_route(PSSMRLNN)
    
    print("\nChecking for any remaining unmapped Local Med Routes...")
    
    PSSMRLFL = 0
    PSSMRLNN = 0
    
    for PSSMRLP in PSSMRLP:
        PSSMRLND = PSSMRLP[PSSMRLNN]
        
        if not PSSMRLND[3]:
            continue
        
        if not PSSMRLND[4][0]:
            PSSMRLFL = 1
    
    if PSSMRLFL:
        print("\nThere are still local Med Routes marked for 'ALL PACKAGES' not yet mapped,")
        print("see the 'Medication Route Mapping Report' option for more details.")
    else:
        print("\nAll Local Med Routes are mapped!")
    
    input("\nPress Return to continue")

def select_standard_med_route():
    """
    Select a Standard Medication Route
    """
    result = None
    
    while not result:
        response = input("\nEnter 'A' to see All Medication Routes from the Medication Routes (#51.2) File, " \
                         "or 'O' to see Only Unmapped Routes: ")
        
        if response == "A":
            result = list_all_med_routes()
        elif response == "O":
            result = list_unmapped_med_routes()
        else:
            print("\nInvalid option. Please try again.")
    
    return result

def list_all_med_routes():
    """
    List all Medication Routes and Mapping Information
    """
    result = []
    
    for PSSMT in PSSMT:
        for PSSMTI in PSSMT:
            if not PSSMTI[3]:
                continue
            
            if PSSMTI[4][0]:
                continue
            
            result.append(PSSMTI)
            
            print("\n{}\n{}".format(PSSMTI[1], PSSMTI[2]))
    
    return result

def list_unmapped_med_routes():
    """
    List only Unmapped Medication Routes
    """
    result = []
    
    for PSSMT in PSSMT:
        for PSSMTI in PSSMT:
            if not PSSMTI[3]:
                continue
            
            if PSSMTI[4][0]:
                continue
            
            result.append(PSSMTI)
            
            print("\n{}\n{}".format(PSSMTI[1], PSSMTI[2]))
    
    return result

def update_med_route(PSSMRLNN, PSSMRLOK):
    """
    Update the mapping of a Medication Route
    """
    PSSMRLP[PSSMRLNN][5] = PSSMRLOK

def lock_med_route(PSSMRLNN):
    """
    Lock a Medication Route for editing
    """
    return True

def unlock_med_route(PSSMRLNN):
    """
    Unlock a Medication Route after editing
    """
    pass

def one():
    """
    Map one Local Medication Routes to Standard Route
    """
    while True:
        result = select_local_med_route()
        
        if not result:
            break
        
        PSSMRB = result[0]
        PSSMRBAX = result[1]
        
        if PSSMRBAX[0] != "":
            print("\nAlready mapped to:")
            print("Stnd Route: '{}'  FDB Route: '{}'".format(PSSMRBAX[0], PSSMRBAX[1]))
            
            response = input("\nDo you want to remap to a different Standard Med Route? (Y/N) ")
            
            if response != "Y":
                continue
        
        if not lock_med_route(PSSMRB):
            print("\nAnother person is editing this Med Route.")
            input("\nPress Return to continue")
            continue
        
        result = select_standard_med_route()
        
        if not result:
            unlock_med_route(PSSMRB)
            continue
        
        PSSMRBAX = result[0]
        
        update_med_route(PSSMRB, PSSMRBAX)
        
        PSSMRBAZ = PSSMRB[5]
        
        if not PSSMRBAZ:
            print("\nUnable to make this match, Med Route is unmatched")
            input("\nPress Return to continue")
            unlock_med_route(PSSMRB)
            continue
        
        PSSMRB3 = 0
        
        if PSSMRB[4][0] and PSSMRBAX[0] and PSSMRB[4][0] != PSSMRBAX[0]:
            PSSMRB3 = 1
        
        print("\nLocal Route: '{}' has been {} to".format(PSSMRB[1], "remapped" if PSSMRB3 else "mapped"))
        print("Stnd Route: '{}'   FDB Route: '{}'".format(PSSMRBAZ[0], PSSMRBAZ[1]))
        
        unlock_med_route(PSSMRB)
    
def select_local_med_route():
    """
    Select a Local Medication Route
    """
    result = None
    
    while not result:
        PSSMRB = select_med_route()
        
        if not PSSMRB:
            break
        
        PSSMRBAX = PSSMRB[10]
        
        if PSSMRBAX[0] == "":
            result = (PSSMRB, PSSMRBAX)
        else:
            print("\nAlready mapped to:")
            print("Stnd Route: '{}'  FDB Route: '{}'".format(PSSMRBAX[0], PSSMRBAX[1]))
            
            response = input("\nDo you want to remap to a different Standard Med Route? (Y/N) ")
            
            if response == "Y":
                result = (PSSMRB, PSSMRBAX)
    
    return result

def select_med_route():
    """
    Select a Medication Route
    """
    result = None
    
    while not result:
        response = input("\nEnter 'A' to see All Medication Routes from the Medication Routes (#51.2) File, " \
                         "or 'O' to see Only Unmapped Routes: ")
        
        if response == "A":
            result = list_all_med_routes()
        elif response == "O":
            result = list_unmapped_med_routes()
        else:
            print("\nInvalid option. Please try again.")
    
    return result

def rep():
    """
    Medication Route Report
    """
    print("\nThis report will print Medication Route mapping information for Medication")
    print("Routes marked for ALL PACKAGES in the PACKAGE USE (#3) Field of the MEDICATION")
    print("ROUTES (#51.2) File.\n")
    
    while True:
        response = input("\nEnter 'A' for All Routes, 'O' for Only Unmapped Routes: ")
        
        if response != "A" and response != "O":
            print("\nInvalid option. Please try again.")
            continue
        
        PSSPTYPE = response
        break
    
    print("\nThis report is designed for 132 column format!\n")
    
    PSSMTCTA = 0
    PSSMTCTB = 0
    
    for PSSMT in PSSMT:
        for PSSMTI in PSSMT:
            if not PSSMTI[3]:
                continue
            
            if not PSSMTI[4][0]:
                PSSMTCTA += 1
            
            if PSSMTI[4][0]:
                PSSMTCTB += 1
            
            if (PSSMTCTB + 5) > 130:
                print("\nPress Return to continue")
                input()
    
    print("\nChecking for any remaining unmapped Local Med Routes...")
    
    PSSMRLFL = 0
    PSSMRLNN = 0
    
    for PSSMRLP in PSSMRLP:
        PSSMRLND = PSSMRLP[PSSMRLNN]
        
        if not PSSMRLND[3]:
            continue
        
        if not PSSMRLND[4][0]:
            PSSMRLFL = 1
    
    if PSSMRLFL:
        print("\nThere are still local Med Routes marked for 'ALL PACKAGES' not yet mapped,")
        print("see the 'Medication Route Mapping Report' option for more details.")
    else:
        print("\nAll Local Med Routes are mapped!")
    
    input("\nPress Return to continue")