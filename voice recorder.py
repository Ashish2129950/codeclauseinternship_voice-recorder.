import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
import os

class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.is_recording = False
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.audio = pyaudio.PyAudio()
        self.record_seconds = 0
        
        self.root = tk.Tk()
        self.root.title("Audio Recorder")
        
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Record button
        self.record_button = tk.Button(button_frame, text="Record", command=self.toggle_recording, bg="#4CAF50", fg="white", padx=20, pady=10, font=("Times New Roman", 14, "bold"), bd=0, relief=tk.RAISED)
        self.record_button.pack(side=tk.LEFT, padx=20)
        
        # Save button
        self.save_button = tk.Button(button_frame, text="Save Recording", command=self.save_recording, bg="#2196F3", fg="white", padx=20, pady=10, font=("Times New Roman", 14, "bold"), bd=0, relief=tk.RAISED, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=20)
        
        # Center the buttons
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Status: Ready", padx=10, pady=5, font=("Times New Roman", 14, "bold"))
        self.status_label.pack()
        
        # Timer label
        self.timer_label = tk.Label(self.root, text="Recording Time: 00:00", padx=10, pady=5, font=("Times New Roman", 14, "bold"))
        self.timer_label.pack()
        
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
            self.record_button.config(text="Stop Recording", bg="#f44336")
            self.save_button.config(state=tk.DISABLED)
            self.timer_label.config(text="Recording Time: 00:00")
            self.record_seconds = 0
            self.update_timer()
        else:
            self.stop_recording()
            self.record_button.config(text="Record", bg="#4CAF50")
            self.save_button.config(state=tk.NORMAL)
    
    def start_recording(self):
        self.frames = []  # Clear frames list
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        self.is_recording = True
        self.status_label.config(text="Status: Recording")
        # Start reading audio data from the stream
        self.read_audio()
    
    def read_audio(self):
        if self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            self.root.after(1, self.read_audio)  # Schedule the next read_audio call
    
    def stop_recording(self):
        self.is_recording = False
        self.status_label.config(text="Status: Stopped")
        self.stream.stop_stream()
        self.stream.close()
        self.update_timer()
        self.save_button.config(state=tk.NORMAL)  # Enable save button after recording stops
    
    def save_recording(self):
        if len(self.frames) == 0:
            messagebox.showwarning("Warning", "No recording to save.")
            return
        
        output_path = os.path.join("D:", "recordings", "output.wav")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        wf = wave.open(output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        messagebox.showinfo("Success", f"Recording saved as {output_path}")
    
    def update_timer(self):
        if self.is_recording:
            self.record_seconds += 1
            minutes = self.record_seconds // 60
            seconds = self.record_seconds % 60
            self.timer_label.config(text="Recording Time: {:02d}:{:02d}".format(minutes, seconds))
            self.timer_label.after(1000, self.update_timer)
    
    def close(self):
        if self.is_recording:
            self.stop_recording()
        self.audio.terminate()
        self.root.destroy()

if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.root.mainloop()
