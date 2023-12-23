import tkinter as tk
import customtkinter as ctk
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Measure of Central Tendency Calculator")
        self.configure(fg_color="#f1f1f1")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.iconbitmap("Images/avrgLogo.ico")

        self.header = Header(self)
        self.header.pack()

        self.body = Body(self)
        self.body.pack()


class Header(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#1f1f1f",
            width=1000,
            height=150,
            corner_radius=0
        )
        self.pack_propagate(False)

        self.logo = ctk.CTkLabel(
            master=self,
            text_color="#f1f1f1",
            justify="right",
            text="Measure of Central Tendency Calculator",
            font=('Heavitas', 26)
        )
        self.logo.pack(anchor="center", pady=55)

class Body(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#FFFFFF",
            width=1000,
            height=550,
            corner_radius=0
        )
        self.grid_propagate(False)
        self.grid_columnconfigure(2, weight=500)

        self.inputForm = InputForm(self)
        self.inputForm.grid(row=1, column=0, padx=30, pady=58)

        self.outputPresentation = OutputPresentation(self)
        self.outputPresentation.grid(row=1, column=1)

class InputForm(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.pack_propagate(False)

        self.configure(
            width=360,
            height=430,
            fg_color="#9f9f9f",
            corner_radius=15
        )

        self.userInput = ctk.CTkEntry(
            master=self,
            width=340,
            height=100,
            placeholder_text="Input data (comma-separated)",
            font=("Product Sans", 16),
            text_color="#1f1f1f",
            corner_radius=7.5,
            fg_color="#f7f7f7"
        )
        self.userInput.pack(padx=10, pady=10)

        self.calculateBtn = ctk.CTkButton(
            master=self,
            width=340,
            height=50,
            corner_radius=7.5,
            text="CALCULATE",
            font=("Product Sans", 16, "bold"),
            fg_color="#1DB954",
            hover_color="SpringGreen",
            command=self.calculate_and_plot
        )
        self.calculateBtn.pack(padx=10)

        self.resetBtn = ctk.CTkButton(
            master=self,
            width=340,
            height=50,
            corner_radius=7.5,
            text="RESET",
            font=("Product Sans", 16, "bold"),
            fg_color="#DB4437",
            hover_color="red",
            command=self.reset
        )
        self.resetBtn.pack(padx=10, pady=10)

        self.meanLabel = ctk.CTkLabel(
            master=self,
            font=("Product Sans", 16),
            text="Mean = ",
            text_color="#1f1f1f",
        )
        self.meanLabel.pack(padx=10, pady=10)

        self.medianLabel = ctk.CTkLabel(
            master=self,
            font=("Product Sans", 16),
            text="Median = ",
            text_color="#1f1f1f"
        )
        self.medianLabel.pack(padx=10, pady=10)

        self.modeLabel = ctk.CTkLabel(
            master=self,
            font=("Product Sans", 16),
            text="Mode = ",
            text_color="#1f1f1f",
            wraplength=300 
        )
        self.modeLabel.pack(padx=10, pady=10)

    def calculate_and_plot(self):
        # Call the calculate method to update mean, median, and mode labels
        self.calculate()

        # Trigger the update_graph method in OutputPresentation to update the graph
        self.master.outputPresentation.update_graph()

    #from collections import Counter

# ...
    def reset(self):
        # Reset the labels to their starting values
        self.meanLabel.configure(text="Mean = ")
        self.medianLabel.configure(text="Median = ")
        self.modeLabel.configure(text="Mode = ")

        # Clear the text box
        self.userInput.delete(0, tk.END)

        # Trigger the update_graph method in OutputPresentation to clear the graph
        self.master.outputPresentation.update_graph(clear=True)

    def calculate(self):
        data_str = self.userInput.get()
        try:
            data = [float(x) for x in data_str.split(",")]
            mean_value = statistics.mean(data)
            median_value = statistics.median(data)

            # Use Counter to find modes
            data_counter = Counter(data)
            modes = [k for k, v in data_counter.items() if v == max(data_counter.values())]

            # Display "No mode" if there is no mode
            if len(set(data)) == 1:
                self.meanLabel.configure(text="Mean = {:.3f}".format(mean_value))
                self.medianLabel.configure(text="Median = {}".format(median_value))
                self.modeLabel.configure(text="No mode")
            else:
                # Display "Unimodal", "Bimodal", or "Multimodal" based on the number of modes
                mode_string = "Unimodal" if len(modes) == 1 else "Bimodal" if len(modes) == 2 else "Multimodal"
                
                # Display the mode values
                self.meanLabel.configure(text="Mean = {:.3f}".format(mean_value))
                self.medianLabel.configure(text="Median = {}".format(median_value))
                self.modeLabel.configure(text="{}: {}".format(mode_string, ", ".join(map(str, modes))))

        except ValueError:
            self.meanLabel.configure(text="Mean = Invalid input")
            self.medianLabel.configure(text="Median = Invalid input")
            self.modeLabel.configure(text="Mode = Invalid input")

    
   

class OutputPresentation(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.pack_propagate(False)

        self.configure(
            width=550,
            height=430,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        self.graphSelector = ctk.CTkOptionMenu(
            master=self,
            width=75,
            height=25,
            font=("Product Sans", 15),
            values=["Histogram", "Box Plot", "Bar Graph"],
            command=self.update_graph  # Bind the event to update the graph automatically
        )
        self.graphSelector.pack(padx=10, pady=10, anchor="w")

        # Create a canvas for the plot
        self.canvas = ctk.CTkFrame(
            master=self,
            fg_color="#ffffff"
        )
        self.canvas.pack(fill="both", expand=True)

    def update_graph(self, event=None):
        selected_graph = self.graphSelector.get()
        data_str = self.master.inputForm.userInput.get()

        try:
            data = [float(x) for x in data_str.split(",")]

            # Clear the previous plot
            for widget in self.canvas.pack_slaves():
                widget.destroy()

            # Create subplots for each graph
            fig, ax = plt.subplots(figsize=(8, 6))

            if selected_graph == "Histogram":
                ax.hist(data, bins=10, edgecolor='black')
                ax.set_title('Histogram')
                ax.set_xlabel('Values')
                ax.set_ylabel('Frequency')
            elif selected_graph == "Bar Graph":
                ax.bar(range(len(data)), data, color='blue')
                ax.set_title('Bar Graph')
                ax.set_xlabel('Index')
                ax.set_ylabel('Values')
            elif selected_graph == "Box Plot":
                ax.boxplot(data)
                ax.set_title('Box Plot')
                ax.set_ylabel('Values')

            # Add vertical lines for mean, median, and mode
            ax.axvline(np.mean(data), color='red', linestyle='dashed', linewidth=2, label='Mean')
            ax.axvline(np.median(data), color='green', linestyle='dashed', linewidth=2, label='Median')
            ax.axvline(float(np.argmax(np.bincount(data))), color='blue', linestyle='dashed', linewidth=2, label='Mode')
            ax.legend()

            # Embed the plot in Tkinter window
            figure = plt.gcf()
            canvas = FigureCanvasTkAgg(figure, master=self.canvas)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)

        except ValueError:
            self.master.inputForm.meanLabel.config(text="Mean = Invalid input")
            self.master.inputForm.medianLabel.config(text="Median = Invalid input")
            self.master.inputForm.modeLabel.config(text="Mode = Invalid input")


StatApp = Main()
StatApp.mainloop()
