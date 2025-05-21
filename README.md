# Code Clinics Project 🏥

## Overview 📋

Code Clinics offers a helping hand to students struggling with coding problems by providing 30-minute personal sessions. This initiative is backed by skilled volunteers committed to fostering a productive learning environment where students can tackle their coding challenges.

---

### Perquisites 🚩

1. Have only one calender containing the word 'clinic' in your list of calendars 
2. Have a credentials.json downloaded from google calendar console api that you and your teammates are linked to, or use the one provided in the repo [a relative link](/credentials.json)

---


## Quick Start 🚀

### Set Up the Executable

1. Download the `cc16` executable file provided.
2. Move `cc16` to your `~/.local/bin/` directory:

    ```bash
    mv disk/cc16 ~/.local/bin/
    ```

3. Make `cc16` executable:

    ```bash
    chmod +x ~/.local/bin/cc16
    ```
4. Type `cc16` in your terminal then move `credentials.json` to `~/.ccjhb16/` directory if not atomically moved:

### Running Code Clinics

To start using Code Clinics, you can now run `cc16` directly from the terminal:

- To execute the program:

    ```bash
    cc16
    ```

- To log in with your custom username:

    ```bash
    cc16 -u 'your_username'
    ```

Replace `your_username` with your actual student username.

---

## Getting Started with Source Code 🚀

Follow these instructions if you prefer to run the Code Clinics application directly from the source code.

### Prerequisites 🚩

Ensure you have Python and pip installed on your system. For easier library installation run the following command in your source folder:
  ```bash
  pip install -r requirements.txt
  ```

### Installation ⚙️

To get started with the source code, install the required packages using pip:

```bash
pip install requests
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install rich
pip install simple_term_menu
```

---

## Usage 🛠️

Run the Code Clinics application with the following command structure:

```bash
python3 main_file.py [OPTIONS]
```

### Command Line Options

- `-h`, `--help`:
  Display the help message and exit.

- `--username <username>`, `-u <username>`:
  Enter your student username. Example: `-u jay023`.

- `--action <action>`, `-a <action>`:
  
  #### For Volunteers 🦸
  - `ViewSlots`: See your open slots.
  - `AddSlot`: Schedule a new slot.
  - `BookedSlots`: Check your booked slots.
  - `CancelEmptySlot`: Remove an empty slot.

  #### For Students 🙋
  - `Docs`: View all volunteers.
  - `ViewCal`: View events on your personal calendar.
  - `GetSlots`: Find available slots.
  - `CancelBookedSlot`: Withdraw a booked slot.
  - `ViewBookedSlots`: Review your booked slots.
  - `ExpCal`: Export slots in iCal format for use in calendar apps.

- `slot selector`:
  Use arrow keys to select events.

- `--date 'YYYY-MM-DD'`:
  Set the date for the slot.

- `--time 'HH:MM'`:
  Set the time for the slot.

- `--custom_days <days>`, `-dd <days>`:
  Select the number of days to display ev
```bash
python3 main_file.py --action GetSlots
```

Book a slot:

```bash
python3 main_file.py --action AddSlot --date '2024-02-10' --time '10:00'
```


## Support 🙌

For assistance or further information, please do not hesitate to reach out to our team.

---

Happy Coding! 🎉
