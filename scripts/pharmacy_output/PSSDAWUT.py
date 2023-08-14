def DAWEXT(CODE):
    # Returns description for DAW code (Dispense as Written)
    DIC = 9002313.24
    DIC(0) = "Z"
    X = CODE
    ^DIC

    return $P($G(Y(0)),"^",2)


def INPUT():
    # Input Transform for DAW CODE
    if len(X) < 1 or len(X) > 2 or not X:
        del X
        return

    if X == "?":
        ^DD(50, 81, 4)
        return

    DIC(0) = "QM"
    DIC = "^BPS(9002313.24,"
    ^DIC
    X = $P(Y, U, 2)

    if Y < 0:
        del X


def HLP():
    # Executable help for DAW CODE field
    DIC = "^BPS(9002313.24,"
    D = "B"
    DIC(0) = ""
    DQ^DICQ