# 🚴 Bike Workout Interval Timer

A simple macOS menu bar app for interval training on your bike.

## Features

- **Lives in your menu bar** - Always visible, always accessible
- **Configurable intervals** - Set work time, rest time, and number of rounds
- **Visual feedback** - Shows current phase (🔥 work / 😮‍💨 rest), time remaining, and round number
- **Progress bars** - Live progress for current interval AND overall workout
- **Audio cues** - Different sounds for work/rest transitions + countdown ticks
- **Voice announcements** - "Go!" for work, "Rest" for recovery
- **Notifications** - Alerts you when phases change so you can focus on riding

## Installation

### 1. Install Python (if you don't have it)

```bash
brew install python
```

### 2. Install the required package

```bash
pip3 install rumps
```

### 3. Run the app

```bash
python3 bike_intervals.py
```

## Usage

1. **Click the menu bar icon** (shows 🚴 Ready when idle)
2. **Configure your workout:**
   - ⏱️ Work Time - how long each work interval lasts
   - 😮‍💨 Rest Time - how long each rest interval lasts  
   - 🔁 Rounds - total number of rounds
   - 🔊 Sounds - enable/disable audio, test each sound
3. **Click ▶️ Start** to begin your workout
4. **Watch the menu bar** for current status:
   - 🔥 = Work phase (go hard!)
   - 😮‍💨 = Rest phase (recover)
   - Shows seconds remaining, mini progress bar, and current round
5. **Click the menu** to see detailed progress:
   - Current phase with time remaining
   - Interval progress bar (how far through current work/rest)
   - Workout progress bar (overall completion)
   - Current round number
6. **Listen for audio cues:**
   - "Go!" + energetic sound = time to work
   - "Rest" + calm sound = recovery time
   - Tick sounds in last 3 seconds of each phase
   - Celebration sound when workout complete

## Default Settings

- 20 seconds work
- 10 seconds rest
- 10 rounds

## Making it Launch at Login (Optional)

1. Open **System Preferences** → **Users & Groups**
2. Click your username, then **Login Items**
3. Click **+** and add a script that runs the app

Or create an Automator app:
1. Open **Automator**
2. Create new **Application**
3. Add **Run Shell Script** action
4. Enter: `python3 /path/to/bike_intervals.py`
5. Save as an app
6. Add that app to Login Items

## Building as a Standalone App (Optional)

To create a proper .app bundle:

```bash
pip3 install py2app
```

Create `setup.py`:
```python
from setuptools import setup

APP = ['bike_intervals.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # Makes it a menu bar only app
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

Then build:
```bash
python3 setup.py py2app
```

Your app will be in the `dist` folder!

## Tips

- The timer will pause if you click Pause, and resume where it left off
- Reset returns everything to the starting state
- You can't change settings while the timer is running (pause first)
- Works great with a bike trainer - just glance up at the menu bar!

Enjoy your workout! 💪🚴
