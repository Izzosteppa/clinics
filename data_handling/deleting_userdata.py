import os
import time


def delete_files(filename1, filename2, filename3, seconds=1800):
    """Deletes files e.g token, user_data.pkl, events."""
    files_to_delete = [filename1, filename2, filename3]
    try:
        for i in files_to_delete:
            if time.time() - os.path.getmtime(i) > seconds:  # time in seconds
                os.remove(i)
    except FileNotFoundError:
        pass
