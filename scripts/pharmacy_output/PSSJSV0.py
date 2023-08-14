# BIR/CML3, WRT-SCHEDULE VALIDATION CONT. ; 08/21/97 8:26
# 1.0;PHARMACY DATA MANAGEMENT;**218**;9/30/97;Build 13

def ENPSJI():
    PSJPP = "PSJ"

def ENI():
    X = input("\nSelect STANDARD SCHEDULE: ")
    if X == "" or X == "^":
        del X
        del PSJPP
        return
    if X == "?":
        print("\nEnter a standard schedule to view the information pertaining to that schedule.")
    # Rest of the code

def ENSVH():
    if X == "?":
        print("\nEnter a schedule for this order.")
    if X == "??":
        print("\n...", end="")
    Q = input("\n(Press RETURN to continue.) ")
    if Q == "" or Q == "^":
        if not Q:
            Q = "^"
        return
    DIC = "^PS(51.1,"
    DIC(0) = "E"
    DIC("S") = "I $P(^(0),""^"",4)=""" + PSJPP + """"
    DIC("W") = "D DICW^PSSJSV0"
    # Rest of the code

def SCHT():
    print("\n This is the frequency that the action of the order is to take place over"
          "the life of the order.  The schedule may have various forms, such as 'ONCE',"
          "'STAT', 'DAILY', 'Q8H', 'QOD', 'Q5XD', and 'MO-WE-FR@09'."
          "Please note that unexact schedules, such as 'Q4-6H' may not produce the"
          "desired results."
          "Also, when entering a schedule involving days of the week, you need not"
          "enter the entire name of each day, but you must enter at least the first two"
          "letters of each day.")
    print("\n...", end="")
    # Rest of the code

def DICW():
    # Rest of the code

def ENSTH():
    print("\nThe TYPE OF SCHEDULE determines how the schedule will be processed.")
    print("\nA CONTINUOUS schedule is one in which an action is to take place on a regular"
          "basis, such as 'three times a day' or 'once every two days'."
          "A DAY OF THE WEEK schedule is one in which the action is to take place only"
          "on specific days of the week.  This type of schedule should have admin times"
          "entered with it.  If not, the start time of the order is used as the"
          "admin time.  Whenever this type is chosen, the name of the schedule must be in the"
          "form of 'MO-WE-FR'.")
    if PSJPP == "":
        print("\nA DAY OF THE WEEK-RANGE schedule is one in which the action to take place"
              "only on specific days of the week, but at no specific time of day (no admin"
              "times).  Whenever this type is chosen, the name of the schedule must be in "
              "the form of 'MO-WE-FR'.")
    print("\nA ONE-TIME schedule is one in which the action is to take place once only"
          "at a specific date and time.")
    if PSJPP != "":
        print("\nA RANGE schedule is one in which the action will take place within a given"
              "date range."
              "A SHIFT schedule is one in which the action will take place within a given"
              "range of times of day.")