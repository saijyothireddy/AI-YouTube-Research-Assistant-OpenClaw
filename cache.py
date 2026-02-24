import os
import pickle

CACHE_DIR = "data/cache"

def save_cache(video_id, data):
    with open(f"{CACHE_DIR}/{video_id}.pkl","wb") as f:
        pickle.dump(data,f)

def load_cache(video_id):
    path=f"{CACHE_DIR}/{video_id}.pkl"
    if os.path.exists(path):
        with open(path,"rb") as f:
            return pickle.load(f)
    return None
