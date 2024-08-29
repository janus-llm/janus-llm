#!/bin/bash

INPUT_DIR="llm-data/ITMod/documentation-tests/chunking-experiments/mumps-irt-20240730/exhaustive-madlibs-input"
OUTPUT_DIR="llm-data/ITMod/documentation-tests/chunking-experiments/mumps-irt-20240730/generated-comments"
LANGUAGE="mumps"

MODELS=("gpt-4-1025-preview" "bedrock-claude-sonnet" "bedrock-llama3-70b-instruct" "bedrock_mixtral")

# Create experiment_logs dir if it doesn't exist
mkdir -p experiment_logs

for MODEL in "${MODELS[@]}"; do
    nohup python janus/scripts/comment-generation-experiment/mumps_alc_comment_experiment.py --input-dir "$INPUT_DIR" --output-dir "$OUTPUT_DIR" --source-language "$LANGUAGE" --model "$MODEL" > experiment_logs/"$LANGUAGE"_"$MODEL".out 2>&1 &
done

exit 0
