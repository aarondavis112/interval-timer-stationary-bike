#!/usr/bin/env python3

import rumps
import subprocess
import time
from threading import Thread


class IntervalTimerApp(rumps.App):
    def __init__(self):
        super(IntervalTimerApp, self).__init__("🚴 Ready")
        
        # Default settings
        self.work_seconds = 20
        self.rest_seconds = 10
        self.total_rounds = 8
        self.countdown_seconds = 3
        
        # State
        self.current_round = 0
        self.is_running = False
        self.is_work_phase = True
        self.is_countdown = False
        self.remaining_seconds = 0
        
        # Build menu
        self.start_stop_button = rumps.MenuItem("Start", callback=self.toggle_timer)
        self.reset_button = rumps.MenuItem("Reset", callback=self.reset_timer)
        
        # Settings submenus
        self.work_time_menu = rumps.MenuItem("Work Time")
        self.rest_time_menu = rumps.MenuItem("Rest Time")
        self.rounds_menu = rumps.MenuItem("Rounds")
        
        # Work time options
        for seconds in [5, 10, 15, 20, 30, 45, 60, 90, 120]:
            item = rumps.MenuItem(f"{seconds}s", callback=self.set_work_time)
            item.seconds = seconds
            if seconds == self.work_seconds:
                item.state = 1
            self.work_time_menu.add(item)
        
        # Rest time options
        for seconds in [5, 10, 15, 20, 30, 45, 60, 90, 120]:
            item = rumps.MenuItem(f"{seconds}s", callback=self.set_rest_time)
            item.seconds = seconds
            if seconds == self.rest_seconds:
                item.state = 1
            self.rest_time_menu.add(item)
        
        # Rounds options
        for rounds in [1, 3, 5, 8, 10, 12, 15, 20, 30]:
            item = rumps.MenuItem(f"{rounds}", callback=self.set_rounds)
            item.rounds = rounds
            if rounds == self.total_rounds:
                item.state = 1
            self.rounds_menu.add(item)

        
        # Status display
        self.status_item = rumps.MenuItem(self.get_settings_display())
        self.status_item.set_callback(None)
        
        self.menu = [
            self.start_stop_button,
            self.reset_button,
            None,  # Separator
            self.status_item,
            None,  # Separator
            self.work_time_menu,
            self.rest_time_menu,
            self.rounds_menu,
        ]
    
    def play_phase_sound(self):
        """Play a ding for phase transitions."""
        Thread(target=lambda: subprocess.run([
            'afplay', '-r', '1.5', '/System/Library/Sounds/Ping.aiff'
        ]), daemon=True).start()
    
    def play_done_sound(self):
        """Play a celebratory sound when workout is complete."""
        def play_celebration():
            for _ in range(3):
                subprocess.run(['afplay', '/System/Library/Sounds/Hero.aiff'])
                time.sleep(0.3)
        Thread(target=play_celebration, daemon=True).start()
    
    def play_countdown_tick(self):
        """Play a subtle tick for last 3 seconds."""
        Thread(target=lambda: subprocess.run([
            'afplay', '/System/Library/Sounds/Tink.aiff'
        ]), daemon=True).start()
    
    def get_progress_bar(self, current, total, width=10):
        """Generate a progress bar string."""
        if total == 0:
            return "░" * width
        filled = int((current / total) * width)
        empty = width - filled
        return "▓" * filled + "░" * empty
    
    def get_settings_display(self):
        return f"{self.work_seconds}s work / {self.rest_seconds}s rest × {self.total_rounds}"
    
    def update_status_display(self):
        self.status_item.title = self.get_settings_display()
    
    def set_work_time(self, sender):
        if self.is_running:
            rumps.notification("Interval Timer", "", "Stop timer before changing settings")
            return
        
        self.work_seconds = sender.seconds
        for item in self.work_time_menu.values():
            item.state = 1 if item.seconds == self.work_seconds else 0
        self.update_status_display()
        self.title = "🚴 Ready"
    
    def set_rest_time(self, sender):
        if self.is_running:
            rumps.notification("Interval Timer", "", "Stop timer before changing settings")
            return
            
        self.rest_seconds = sender.seconds
        for item in self.rest_time_menu.values():
            item.state = 1 if item.seconds == self.rest_seconds else 0
        self.update_status_display()
        self.title = "🚴 Ready"
    
    def set_rounds(self, sender):
        if self.is_running:
            rumps.notification("Interval Timer", "", "Stop timer before changing settings")
            return
            
        self.total_rounds = sender.rounds
        for item in self.rounds_menu.values():
            item.state = 1 if item.rounds == self.total_rounds else 0
        self.update_status_display()
        self.title = "🚴 Ready"
    
    def toggle_timer(self, _):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        self.is_running = True
        self.start_stop_button.title = "Pause"
        
        if self.current_round == 0:
            # Fresh start - begin with countdown
            self.current_round = 1
            self.is_countdown = True
            self.is_work_phase = True
            self.remaining_seconds = self.countdown_seconds
            rumps.notification("🚴 Interval Timer", "Get Ready!",
                             f"Starting in {self.countdown_seconds} seconds...")
        
        # Start timer thread
        Thread(target=self.run_timer, daemon=True).start()
    
    def stop_timer(self):
        self.is_running = False
        self.start_stop_button.title = "Resume"
    
    def reset_timer(self, _):
        self.is_running = False
        self.current_round = 0
        self.is_work_phase = True
        self.is_countdown = False
        self.remaining_seconds = 0
        self.start_stop_button.title = "Start"
        self.title = "🚴 Ready"
    
    def run_timer(self):
        while self.is_running:
            # Update display
            if self.is_countdown:
                # Simple countdown display - no progress bar
                self.title = f"Get ready... {self.remaining_seconds}s"
            else:
                phase = "Working" if self.is_work_phase else "Resting"
                phase_total = self.work_seconds if self.is_work_phase else self.rest_seconds
                phase_elapsed = phase_total - self.remaining_seconds
                mini_bar = self.get_progress_bar(phase_elapsed, phase_total, width=5)
                self.title = f"{phase} {self.remaining_seconds}s {mini_bar} R{self.current_round}"
            
            time.sleep(1)
            
            if not self.is_running:
                break
                
            self.remaining_seconds -= 1
            
            # Countdown ticks for last 3 seconds
            if self.remaining_seconds <= 3 and self.remaining_seconds > 0:
                self.play_countdown_tick()
            
            if self.remaining_seconds <= 0:
                # Phase complete
                if self.is_countdown:
                    # Countdown done, start work phase
                    self.is_countdown = False
                    self.remaining_seconds = self.work_seconds
                    self.play_phase_sound()
                    rumps.notification("🚴 Interval Timer", "GO!",
                                     f"Round 1/{self.total_rounds} - Start working!")
                elif self.is_work_phase:
                    # Work phase done
                    if self.current_round >= self.total_rounds:
                        # Last round - done! No rest after final work.
                        self.is_running = False
                        self.current_round = 0
                        self.start_stop_button.title = "Start"
                        self.title = "🚴 Done! 🎉"
                        self.play_done_sound()
                        rumps.notification("Workout Complete!",
                                        "Great job!",
                                        f"Completed {self.total_rounds} rounds!")
                    else:
                        # Not the last round, start rest
                        self.is_work_phase = False
                        self.remaining_seconds = self.rest_seconds
                        self.play_phase_sound()
                        rumps.notification("Rest",
                                        f"Round {self.current_round} work done!",
                                        f"Rest for {self.rest_seconds}s")
                else:
                    # Rest phase done, start next round
                    self.current_round += 1
                    self.is_work_phase = True
                    self.remaining_seconds = self.work_seconds
                    self.play_phase_sound()
                    rumps.notification("GO!",
                                    f"Round {self.current_round}/{self.total_rounds}",
                                    f"Work for {self.work_seconds}s!")


if __name__ == "__main__":
    app = IntervalTimerApp()
    app.run()