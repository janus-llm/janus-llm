# BIR/RTR/WRT-Auto create Pharmacy Orderable Item File; 09/01/98 7:07
# 1.0;PHARMACY DATA MANAGEMENT;**8,15**;9/30/97

# make sure file has not already been created
PSSITE = int(input('$O(^PS(59.7,0)): '))
if int(input('$P($G(^PS(59.7,+PSSITE,80)),"^",2): ')):
    print(f"\nOrderable Item Auto-Create has {'already been queued' if $P(^(80),\"^\",2)==1 else 'already been completed'}, no action taken!\n")
    PSSITE = None
    input("Press RETURN to continue")

if PSSITE is not None:
    ^PS(59.7,PSSITE,80) = 1

# This job will create your Pharmacy Orderable Item File, and match IV Solutions,
# IV Additives, and Dispense Drugs to the Pharmacy Orderable Item File.
print("This job will create your Pharmacy Orderable Item File, and match IV Solutions,")
print("IV Additives, and Dispense Drugs to the Pharmacy Orderable Item File.")
print("Enter P to create your Pharmacy Orderable Item File first by Primary Drug")
print("Name, then by VA Generic Name")
print("Enter V to create the Pharmacy Orderable Item File by VA Generic Name only")
PSOHOW = input("Enter P or V: ")
if PSOHOW in ['P', 'V']:
    PSOQTIME = int(input("QUEUE TO RUN AT WHAT TIME: "))
    print("TASK QUEUED!")
else:
    ^PS(59.7,PSSITE,80) = ""