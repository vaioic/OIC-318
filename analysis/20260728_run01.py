from shared import core

filepath = r"D:\Projects\OIC-318\data\untiled_images"

core.process_directory(filepath, "../processed/20260728 Dev", img_chunk_size=3)
