# Evaluating

There are a few different ways you can evaluate the products generated with `janus-llm`:

- Evaluate a set of requirements with an LLM based on INCOSE standards.
- Evaluate the reading level of summaries or requirements, etc.
- Compare the difference between two texts with BLEU, chrF, ROUGE, and similarity scores.
- Evaluate the cyclomatic complexity, maintainability, Halstead difficulty, effort, and volume of source code.

Some of these evaluation metrics require a target and a reference (e.g., BLEU, chrF, ROUGE, and similarity scores). Others only require a target (e.g., cyclomatic complexity, flesch, etc.).

The output of `janus evaluate -h` is seen below:

```output
> janus evaluate -h
                                                                                                         
 Usage: janus evaluate [OPTIONS] COMMAND [ARGS]...                                                       
                                                                                                         
 Evaluation of generated source code or documentation                                                    
                                                                                                         
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────╮
│ bleu                         BLEU score using sacrebleu                                               │
│ chrf                         chrF score using sacrebleu                                               │
│ cyclomatic-complexity        Cyclomatic complexity score                                              │
│ difficulty                   Halstead difficulty score                                                │
│ effort                       Halstead effort score                                                    │
│ flesch                       The Flesch Readability score                                             │
│ flesch-grade                 The Flesch Grade Level Readability score                                 │
│ gunning-fog                  The Gunning-Fog Readability score                                        │
│ gunning-fog-grade            The Gunning-Fog Grade Level Readability score                            │
│ llm                          LLM self-evaluation on a target file                                     │
│ llm-ref                      LLM self-evaluation on a target file and a reference file                │
│ maintainability              Maintainability score                                                    │
│ rouge                        ROUGE score                                                              │
│ similarity-score             Distance between embeddings of strings.                                  │
│ volume                       Halstead volume score                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

There's also an LLM Self Evaluation command. The help command has been trimmed for brevity:

```output
❯ janus llm-self-eval -h
                                                                                                         
 Usage: janus llm-self-eval [OPTIONS]                                                                    
                                                                                                         
 Use an LLM to evaluate its own performance.                                                             
                                                                                                         
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                            [default: gpt-4o]          │
│    --evaluation-type         -e                 [incose|comments]          Type of output to          │
│                                                                            evaluate.                  │
│                                                                            [default: incose]          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Evaluation with an LLM

### Adding a Model

Before you can evaluate with an LLM, you need to add an LLM model to your configuration. You can do this by running the following command:

```shell
janus llm add my-gpt --type OpenAI
```

And then follow the CLI instructions to add the model to your configuration.

### Evaluating Requirements

First, generate this requirements with `janus`:

```shell
janus document  --doc-mode requirements --input janus/cli/ --output-dir janus-docs --llm my-gpt --language python -r RequirementsFormatRefiner
```

You can use an LLM to evaluate requirements against the [INCOSE standard](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_040423_final_drafts.pdf?sfvrsn=5c877fc7_2).

```shell
janus llm-self-eval --input janus-docs --output-dir janus-evals --llm myazure --language python -e incose
```

## Evaluation without a Reference

### Flesch Grade Level

Adding `-S` to an `evaluate` command will read in the target and reference as a string instead of reading in a file's contents.

```shell
janus evaluate flesch-grade -o test-output.json -t "This is an example of the reading grade level" -S
```

## Evaluation with a Reference

### BLEU

```shell
janus evaluate bleu -o test-output.json -t "This is an example of the BLEU metric" -r "This is a test of the BLEU metric" -S
```

