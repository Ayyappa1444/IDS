import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import List, Tuple

class Event:
    def __init__(self, description: str, start: str, end: str):
        self.description = description
        self.start_time = datetime.strptime(start, "%H:%M")
        self.end_time = datetime.strptime(end, "%H:%M")

class EventScheduler:
    def __init__(self):
        self.events = []
        self.conflicts = []
        self.resolutions = []

    def add_event(self, event: Event) -> bool:
        conflicts = self._check_conflicts(event)
        if conflicts:
            self.conflicts.append((event, conflicts))
            new_time = self._find_next_available_slot(event)
            self.resolutions.append((event, new_time))
            return False
        self.events.append(event)
        self._sort_events()
        return True

    def _check_conflicts(self, new_event: Event) -> List[Event]:
        return [
            event for event in self.events
            if (new_event.start_time < event.end_time and 
                new_event.end_time > event.start_time)
        ]

    def _find_next_available_slot(self, event: Event) -> Tuple[str, str]:
        if not self.events:  # If there are no events, return the original times
            return (event.start_time.strftime("%H:%M"), event.end_time.strftime("%H:%M"))
        
        last_event = max(self.events, key=lambda x: x.end_time)
        new_start = last_event.end_time
        duration = (event.end_time - event.start_time)
        new_end = new_start + duration
        return (new_start.strftime("%H:%M"), new_end.strftime("%H:%M"))

    def _sort_events(self):
        self.events.sort(key=lambda x: x.start_time)

    def get_schedule(self) -> List[str]:
        return [
            f"{i+1}. \"{event.description}\", Start: \"{event.start_time.strftime('%H:%M')}\", "
            f"End: \"{event.end_time.strftime('%H:%M')}\""
            for i, event in enumerate(self.events)
        ]

class EventSchedulerApp:
    def __init__(self, root):
        self.scheduler = EventScheduler()
        self.root = root
        self.root.title("Event Scheduler")

        # Create input fields
        self.description_label = tk.Label(root, text="Event Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.start_label = tk.Label(root, text="Start Time (HH:MM):")
        self.start_label.pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.pack()

        self.end_label = tk.Label(root, text="End Time (HH:MM):")
        self.end_label.pack()
        self.end_entry = tk.Entry(root)
        self.end_entry.pack()

        self.add_button = tk.Button(root, text="Add Event", command=self.add_event)
        self.add_button.pack()

        self.schedule_button = tk.Button(root, text="Show Schedule", command=self.show_schedule)
        self.schedule_button.pack()

        self.output_text = tk.Text(root, height=15, width=50)
        self.output_text.pack()

    def add_event(self):
        description = self.description_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        if not description or not start or not end:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            event = Event(description, start, end)
            success = self.scheduler.add_event(event)
            if success:
                messagebox.showinfo("Success", "Event added successfully!")
            else:
                messagebox.showwarning("Conflict Detected", f"Conflict detected with: {event.description}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid time in HH:MM format.")

    def show_schedule(self):
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        schedule = self.scheduler.get_schedule()
        if schedule:
            self.output_text.insert(tk.END, "Scheduled Events:\n")
            for line in schedule:
                self.output_text.insert(tk.END, line + "\n")
        else:
            self.output_text.insert(tk.END, "No events scheduled.")

        if self.scheduler.conflicts:
            self.output_text.insert(tk.END, "\nConflicting Events:\n")
           
                 
            
                