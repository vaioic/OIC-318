from shared import core

filepath = r"../data/Dataset1"

# core.process_directory(filepath, "../processed/20260729", img_chunk_size=5)

# Have to process the remaining images
core.process_directory(filepath, "../processed/20260805", img_chunk_size=5)
