import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AirQualityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Air Quality Analysis Software")
        self.root.geometry("800x600")
        self.root.configure(bg="#DFF6FF")  # Soft light blue background

        # Set up grid weights for responsive design
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Main frame to center all content
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Inner frame for widgets
        self.frame = ttk.Frame(self.main_frame)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add weights for the widget container frame
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Title Label
        self.title_label = ttk.Label(
            self.frame, 
            text="🌏 Air Quality Analysis", 
            font=("Arial", 20, "bold"), 
            background="#007ACC", 
            foreground="white",
            anchor="center",
            padding=(10, 5)
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")

        # Buttons
        self.load_button = ttk.Button(self.frame, text="📂 Load Data", command=self.load_data)
        self.load_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.analyze_button = ttk.Button(self.frame, text="📊 Analyze Data", command=self.analyze_data, state=tk.DISABLED)
        self.analyze_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.plot_pm25_button = ttk.Button(self.frame, text="🌫️ Plot PM2.5 Data", command=self.plot_pm25_data, state=tk.DISABLED)
        self.plot_pm25_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.plot_corr_button = ttk.Button(self.frame, text="📈 Plot Correlation Matrix", command=self.plot_corr_matrix, state=tk.DISABLED)
        self.plot_corr_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Result Label
        self.result_label = ttk.Label(
            self.frame, 
            text="📝 Results will appear here.", 
            wraplength=700, 
            font=("Arial", 11, "italic"), 
            background="#DFF6FF",
            foreground="#333"
        )
        self.result_label.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew")

        # Add weights for rows and columns in the inner frame
        for i in range(4):  # 4 rows
            self.frame.rowconfigure(i, weight=1)
        for j in range(2):  # 2 columns
            self.frame.columnconfigure(j, weight=1)

        # Initialize the data variable
        self.data = None

    def load_data(self):
        """Load multiple datasets through file dialog."""
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])  # Select multiple files
        if file_paths:
            try:
            # Initialize an empty list to store data from all files
                all_data = []
            
                for file_path in file_paths:
                # Read each CSV file and append to the list
                    data = pd.read_csv(file_path)
                    data['date'] = pd.to_datetime(data['date'])
                    all_data.append(data)
                
            # Concatenate all dataframes into one
                self.data = pd.concat(all_data, ignore_index=True)
            
                messagebox.showinfo("Success", f"{len(file_paths)} files loaded successfully.")
                self.analyze_button.config(state=tk.NORMAL)
                self.plot_pm25_button.config(state=tk.NORMAL)
                self.plot_corr_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the data: {e}")

    def analyze_data(self):
        """Analyze the data and show basic insights."""
        if self.data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        # Clean the dataset
        self.data = self.data.dropna()

        # Basic Statistics
        basic_stats = self.data.describe()

        # Average pollution by city
        avg_pollution = self.data.groupby('city')[['PM2.5', 'PM10', 'NO2', 'CO', 'O3']].mean()

        # Display Insights
        insights = f"--- Basic Statistics ---\n{basic_stats}\n\n--- Average Pollution by City ---\n{avg_pollution}"
        self.result_label.config(text=insights)

    def plot_pm25_data(self):
        """Plot PM2.5 levels over time for each city."""
        if self.data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        # Create a new window for plotting PM2.5 data
        plot_window = tk.Toplevel(self.root)
        plot_window.title("PM2.5 Levels Over Time")
        plot_window.geometry("800x600")

        # Plot PM2.5 levels over time for each city
        fig, ax = plt.subplots(figsize=(12, 6))
        for city in self.data['city'].unique():
            city_data = self.data[self.data['city'] == city]
            ax.plot(city_data['date'], city_data['PM2.5'], label=city)

        ax.set_title('PM2.5 Levels Over Time by City')
        ax.set_xlabel('Date')
        ax.set_ylabel('PM2.5 Levels')
        ax.legend()
        ax.grid()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        canvas.draw()

    def plot_corr_matrix(self):
        """Plot correlation matrix of pollutants and weather variables."""
        if self.data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        # Create a new window for plotting the correlation matrix
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Correlation Matrix")
        plot_window.geometry("800x600")

        # Calculate correlation between weather and pollutants
        correlation = self.data[['PM2.5', 'PM10', 'CO', 'NO2', 'O3', 'temperature', 'humidity']].corr()

        # Plot the correlation matrix
        fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax_corr)
        ax_corr.set_title('Correlation Matrix')

        # Embed the plot in the Tkinter window
        canvas_corr = FigureCanvasTkAgg(fig_corr, master=plot_window)
        canvas_corr.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        canvas_corr.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirQualityApp(root)
    root.mainloop()
