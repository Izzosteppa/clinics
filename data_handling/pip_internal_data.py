import os.path
import pickle

import logic_code.user_input as ui


def events_writer(modified_data, path_to_file):
    """Internal data stored in a pickle file to keep state."""
    if os.path.exists(ui.resource_path(path_to_file)):
        with open(ui.resource_path(path_to_file), "rb") as f:
            deserialized_dict = pickle.load(f)
        if deserialized_dict == modified_data or modified_data == "no_username":
            return deserialized_dict
        else:
            with open(ui.resource_path(path_to_file), "wb") as f:
                pickle.dump(modified_data, f)

            with open(ui.resource_path(path_to_file), "rb") as f:
                deserialized_dict = pickle.load(f)
    else:
        with open(ui.resource_path(path_to_file), "wb") as f:
            pickle.dump(modified_data, f)

        with open(ui.resource_path(path_to_file), "rb") as f:
            deserialized_dict = pickle.load(f)
    return deserialized_dict


