import rumps
import subprocess
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
        
        # Use rumps.Timer instead of threading
        self.timer = rumps.Timer(self.on_tick, 1)
        
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
            None,
            self.status_item,
            None,
            self.work_time_menu,
            self.rest_time_menu,
            self.rounds_menu,
        ]
    
    def play_sound(self, sound_name, rate=None):
        """Play a system sound in background thread."""
        def _play():
            cmd = ['afplay']
            if rate:
                cmd.extend(['-r', str(rate)])
            cmd.append(f'/System/Library/Sounds/{sound_name}.aiff')
            subprocess.run(cmd, capture_output=True)
        Thread(target=_play, daemon=True).start()
    
    def get_progress_bar(self, current, total, width=5):
        if total == 0:
            return "░" * width
        filled = int((current / total) * width)
        return "▓" * filled + "░" * (width - filled)
    
    def get_settings_display(self):
        return f"{self.work_seconds}s work / {self.rest_seconds}s rest × {self.total_rounds}"
    
    def update_status_display(self):
        self.status_item.title = self.get_settings_display()
    
    def set_work_time(self, sender):
        if self.is_running:
            return
        self.work_seconds = sender.seconds
        for item in self.work_time_menu.values():
            item.state = 1 if item.seconds == self.work_seconds else 0
        self.update_status_display()
        self.title = "🚴 Ready"
    
    def set_rest_time(self, sender):
        if self.is_running:
            return
        self.rest_seconds = sender.seconds
        for item in self.rest_time_menu.values():
            item.state = 1 if item.seconds == self.rest_seconds else 0
        self.update_status_display()
        self.title = "🚴 Ready"
    
    def set_rounds(self, sender):
        if self.is_running:
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
            self.current_round = 1
            self.is_countdown = True
            self.is_work_phase = True
            self.remaining_seconds = self.countdown_seconds
        
        self.update_title()
        self.timer.start()
    
    def stop_timer(self):
        self.is_running = False
        self.timer.stop()
        self.start_stop_button.title = "Resume"
    
    def reset_timer(self, _):
        self.timer.stop()
        self.is_running = False
        self.current_round = 0
        self.is_work_phase = True
        self.is_countdown = False
        self.remaining_seconds = 0
        self.start_stop_button.title = "Start"
        self.title = "🚴 Ready"
    
    def update_title(self):
        if self.is_countdown:
            self.title = f"Get ready... {self.remaining_seconds}s"
        else:
            phase = "Work" if self.is_work_phase else "Rest"
            phase_total = self.work_seconds if self.is_work_phase else self.rest_seconds
            phase_elapsed = phase_total - self.remaining_seconds
            bar = self.get_progress_bar(phase_elapsed, phase_total)
            self.title = f"{phase} {self.remaining_seconds}s {bar} R{self.current_round}"
    
    def on_tick(self, _):
        if not self.is_running:
            return
        
        self.remaining_seconds -= 1
        
        if 0 < self.remaining_seconds <= 3:
            self.play_sound("Tink")
        
        if self.remaining_seconds <= 0:
            self.play_sound("Ping", rate=1.5)
            
            if self.is_countdown:
                self.is_countdown = False
                self.remaining_seconds = self.work_seconds
            
            elif self.is_work_phase:
                if self.current_round >= self.total_rounds:
                    self.timer.stop()
                    self.is_running = False
                    self.current_round = 0
                    self.start_stop_button.title = "Start"
                    self.title = "🚴 Done! 🎉"
                    self.play_sound("Hero")
                    return
                else:
                    self.is_work_phase = False
                    self.remaining_seconds = self.rest_seconds
            
            else:
                self.current_round += 1
                self.is_work_phase = True
                self.remaining_seconds = self.work_seconds
        
        self.update_title()


if __name__ == "__main__":
    IntervalTimerApp().run()