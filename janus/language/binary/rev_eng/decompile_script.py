import __main__ as ghidra_app
from ghidra.app.decompiler import DecompInterface


def decompile_function(decompiler, function):
    """Decompile a single function."""

    timeout = None
    # Try to decompile
    decompile_status = decompiler.decompileFunction(function, 0, timeout)
    # If it's successful...`
    if decompile_status and decompile_status.decompileCompleted():
        # Get and return the resulting C psuedocode
        decompiled_function = decompile_status.getDecompiledFunction()
        if decompiled_function:
            return decompiled_function.getC()


def decompile_program(decompiler):
    """Decompile each function in the current program."""

    # We'll decompilation of functions to this string as we go through each
    decompiled_buffer = ""
    all_functions = ghidra_app.currentProgram.getListing().getFunctions(True)

    # Set up a filter for imported library functions etc., which we presumably are not
    # interested in
    external_functions = (
        ghidra_app.currentProgram.getFunctionManager().getExternalFunctions()
    )
    external_function_names = []
    for function in external_functions:
        external_function_names.append(function.getName())

    # Iterate over all the non-imported functions, decompiling pushing each to the buffer
    for function in all_functions:
        if function.getName() not in external_function_names:
            function_decompilation = decompile_function(decompiler, function)
            if function_decompilation:
                decompiled_buffer += function_decompilation

    return decompiled_buffer


def run_decompilation():
    decompiler = DecompInterface()

    # Load up the binary we're decompiling
    decompiler.openProgram(ghidra_app.currentProgram)

    # binary.py will pass a temporary output directory to this script where we can store its output
    output_path = ghidra_app.getScriptArgs()[0]

    # Do the actual decompilation
    decompilation = decompile_program(decompiler)

    # Write the result to a file which binary.py will read
    with open(output_path, "w") as fw:
        fw.write(decompilation)


if __name__ == "__main__":
    run_decompilation()
