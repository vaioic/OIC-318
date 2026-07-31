from shared import core

filepath = r"../data/Dataset1"

core.process_directory(filepath, "../processed/20260729", img_chunk_size=5)
