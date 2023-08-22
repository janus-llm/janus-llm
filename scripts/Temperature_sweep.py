
import subprocess

def run_translation_and_check(temp_values):
    for run in range(10):
        for temp in temp_values:
            # Call the translate script with the given temperature value
            translate_cmd = [
                "python", "scripts/translate.py",
                "--input-dir", "scripts/pharmacy_input_subset",
                "--input-lang", "mumps",
                "--output-lang", "python-3.10",
                "--output-dir", f"scripts/pharmacy_output_subset/temp_{temp}/run_{run}",
                "--llm-name", "gpt-3.5-turbo-16k",
                "--temp", str(temp)
            ]
            subprocess.run(translate_cmd)

            # Call the pyright_count_syntax script
            pyright_cmd = [
                "python", "scripts/pyright_count_syntax.py",
                f"scripts/pharmacy_output_subset/temp_{temp}/run_{run}",
                f"scripts/pharmacy_output_subset_errors/temp_{temp}/run_{run}.json"
            ]
            subprocess.run(pyright_cmd)

if __name__ == "__main__":
    # Define the temperature values you want to sweep through
    temperature_values = [i/10 for i in range(0,11)]  
    run_translation_and_check(temperature_values)