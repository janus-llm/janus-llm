from ghidra.app.decompiler import DecompInterface

import __main__ as ghidra_app


def decompile_function(decompiler, function):

    timeout = None
    # decompile
    dec_status = decompiler.decompileFunction(function, 0, timeout)
    # check if it's successfully decompiled
    if dec_status and dec_status.decompileCompleted():
        # get psuedo c code
        dec_ret = dec_status.getDecompiledFunction()
        if dec_ret:
            return dec_ret.getC()


def decompile(decompiler):

    decompiled_buffer = ""
    all_functions = ghidra_app.currentProgram.getListing().getFunctions(True)

    # Set up a filter for imported library functions etc., which we presumably are not interested in
    external_functions = ghidra_app.currentProgram.getFunctionManager().getExternalFunctions()
    external_function_names = []
    for function in external_functions:
        external_function_names.append(function.getName())

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
    decompilation = decompile(decompiler)

    # Write the result to a file which binary.py will read
    with open(output_path, 'w') as fw:
        fw.write(decompilation)


if __name__ == '__main__':
    run_decompilation()
