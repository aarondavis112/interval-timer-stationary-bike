# 🚴 Stationary Bike Workout Interval Timer

A simple macOS menu bar app for interval training on your bike. The default is set for Tabata workouts.

## Features

- **Lives in your menu bar** - Always visible, always accessible
- **Configurable intervals** - Set work time, rest time, and number of rounds
- **Visual feedback** - Shows current phase (🔥 work / 😮‍💨 rest), time remaining, and round number
- **Progress bars** - Live progress for current interval AND overall workout
- **Audio cues** - Different sounds for work/rest transitions + countdown ticks
- **Voice announcements** - "Go!" for work, "Rest" for recovery
- **Notifications** - Alerts you when phases change so you can focus on riding

## Installation

```bash
brew install python
pip3 install rumps
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

## Confession

This was vibe coded lol
