def PSSSCHRP():
    print("\nThis report displays entries from the ADMINISTRATION SCHEDULE (#51.1) File.")
    print("It can be run for all Schedules, or only Schedules without a FREQUENCY")
    print("(IN MINUTES). Only schedules with a PSJ Package Prefix will be displayed, since")
    print("they are the only schedules the software will look at when deriving a FREQUENCY")
    print("(IN MINUTES) for the daily dosage checks. If a FREQUENCY (IN MINUTES) cannot")
    print("be determined for an order, the daily dosage check cannot occur for that order.")
    
    DIR = input("Print All Schedules, or Only Schedules without a frequency (A/O)? ")
    if DIR.upper() not in ('A', 'O'):
        MESS()
        input("Press Return to continue")
        return
    
    PSSAFRP = DIR.upper()
    
    DIR = input("Print report in 80 or 132 column format (80/132)? ")
    if DIR != '80' and DIR != '132':
        MESS()
        input("Press Return to continue")
        return
    
    PSSALONG = DIR
    
    IOP = input("Enter the printer device (P) or terminal (C): ")
    
    if IOP.upper() == 'P':
        ZTRTN = "START^PSSSCHRP"
        ZTDESC = "Administration Schedule Report"
        ZTSAVE = {"PSSAFRP": PSSAFRP, "PSSALONG": PSSALONG}
        # Submit the job to the background queue
        return
    
    START(PSSAFRP, PSSALONG)

def START(PSSAFRP, PSSALONG):
    PSSAFOUT = 0
    PSSAFDEV = 'P' if IOP.upper() == 'P' else 'C'
    PSSAFCT = 1
    
    print_report_header(PSSAFRP, PSSALONG, PSSAFCT)
    
    PSSAFQ = ""
    while PSSAFQ != None and not PSSAFOUT:
        PSSAFQ = next_schedule(PSSAFQ)
        
        if PSSAFQ == None or PSSAFOUT:
            break
        
        PSSAFRA = PSSAFQ + ","
        PSSAFRAA = get_schedule_details(PSSAFRA)
        
        if PSSAFRAA["4"] != "PSJ":
            continue
        
        if PSSAFRP == 'O' and PSSAFRAA["2"]:
            continue
        
        PSSAFNOF = 1
        
        print("\n" + PSSAFRAA[".01"])
        
        if len(PSSAFRAA["1"]) > 0:
            print("STANDARD ADMINISTRATION TIMES: " + PSSAFRAA["1"])
        
        if len(PSSAFRAA["8"]) > 0:
            print("OUTPATIENT EXPANSION: " + PSSAFRAA["8"])
        
        if len(PSSAFRAA["8.1"]) > 0:
            print("OTHER LANGUAGE EXPANSION: " + PSSAFRAA["8.1"])
        
        if ($Y+5)>IOSL:
            print_report_header(PSSAFRP, PSSALONG, PSSAFCT)
            continue
        
        PSSWAS = 0
        while True:
            PSSWAS = next_ward(PSSAFQ, PSSWAS)
            
            if PSSWAS == None:
                break
            
            PSSWASNM = get_ward_name(PSSWAS)
            
            print("WARD: " + PSSWASNM)
            
            if ($Y+5)>IOSL:
                print_report_header(PSSAFRP, PSSALONG, PSSAFCT)
                continue
            
            PSSWASAD = get_ward_administration_times(PSSAFQ, PSSWAS)
            
            if PSSWASAD:
                print("WARD ADMINISTRATION TIMES: " + PSSWASAD)
            
            if ($Y+5)>IOSL:
                print_report_header(PSSAFRP, PSSALONG, PSSAFCT)
            
def print_report_header(PSSAFRP, PSSALONG, PSSAFCT):
    print("\n" + "-" * 78)
    print("ADMINISTRATION SCHEDULE FILE REPORT (All)" if PSSAFRP == 'A' else "ADMINISTRATION SCHEDULE WITHOUT FREQUENCY REPORT")
    print("PAGE: " + str(PSSAFCT))
    print("-" * 78)
    PSSAFCT += 1

def next_schedule(PSSAFQ):
    # Get the next schedule
    return None

def get_schedule_details(PSSAFRA):
    # Get the schedule details
    return {}

def next_ward(PSSAFQ, PSSWAS):
    # Get the next ward
    return None

def get_ward_name(PSSWAS):
    # Get the ward name
    return ""

def get_ward_administration_times(PSSAFQ, PSSWAS):
    # Get the ward administration times
    return ""

def MESS():
    print("\nNothing queued to print.")

PSSSCHRP()