import pandas as pd
import matplotlib.pyplot as plt

def plot_phonon_band_structure(file_path, color='green', symbol=1, linestyle='-', label='ACE'):
    # Read data from the CSV file, skipping lines starting with '#'
    x_values = []
    x_line = []
    y_values = []

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith('#   0') and symbol == 1:
                # Extract x values from the line starting with '#'
                x_line = [float(val) for val in line.split()[1:]]
                print(x_line)
            if not line.startswith('#'):
                values = line.split()
                if len(values) >= 2:
                    x_values.append(float(values[0]))
                    y_values.append(float(values[1]))

    # Plot the graph
    plt.ylabel('Frequency (THz)')
    plt.grid(axis='y', linestyle='--')
    # Remove x axis ticks
    plt.xticks([])

    # Plot lines between adjacent points except when the difference in x values exceeds 0.5
    for i in range(len(x_values) - 1):
        if abs(x_values[i] - x_values[i + 1]) > 0.5:
            continue
        plt.plot([x_values[i], x_values[i + 1]], [y_values[i], y_values[i + 1]], color=color,linestyle=linestyle)


    # Plot lines at specified x values
    for x in x_line:
        plt.axvline(x, color='gray', linestyle='--')
    xticks_pos = x_line
    # Plot lines at specified x values with Greek letters
    greek_letters = [r'$\Gamma$', r'$H$', r'$P$', r'$\Gamma$', r'$N$']  # Greek letter names
    for i, x in enumerate(x_line):
        # Find the corresponding tick position
        tick_index = x_line.index(x)
        tick_pos = xticks_pos[tick_index]
        plt.text(tick_pos, -0.7, greek_letters[i], fontsize=12, ha='center')

    # Add label for the entire curve
    plt.plot([], [], color=color, linestyle=linestyle, label=label)


# Plot the phonon band structure from phononband.csv
plot_phonon_band_structure("phononband.csv")
plot_phonon_band_structure("../REF_DATA/phonon_DFT.dat", color='dodgerblue', symbol=0, linestyle='-', label='DFT')

# Show legend
plt.legend()
# Save the plot as an image
plt.savefig('phonon_band_structure.png')

# Show the plot
plt.show()



