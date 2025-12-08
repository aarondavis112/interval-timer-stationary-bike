# 🚴 Stationary Bike Workout Interval Timer

A simple macOS menu bar app for interval training on your bike. The default is set for Tabata workouts.

## Features

- **Lives in your menu bar** - Always visible, always accessible
- **Configurable intervals** - Set work time, rest time, and number of rounds
- **Visual feedback** - Shows current phase, time remaining, and round number
- **Progress bars** - Live progress for current interval AND overall workout
- **Audio cues** - Different sounds for work/rest transitions + countdown ticks

## Installation

```bash
brew install python
pip3 install rumps
python3 bike_intervals.py
```

## Usage

1. **Click the menu bar icon** (shows 🚴 Ready when idle)
2. **Configure your workout:**
   - Work Time - how long each work interval lasts
   - Rest Time - how long each rest interval lasts  
   - Rounds - total number of rounds
3. **Click Start** to begin your workout
4. **Watch the menu bar** for current status:
   - Working (go hard!)
   - Resting (recover)
   - Shows seconds remaining, mini progress bar, and current round

## Confession

This was vibe coded lol
