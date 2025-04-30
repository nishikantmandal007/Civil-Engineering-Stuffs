#Gradation of coarse aggregates
Sieve_size = [40, 37.5, 31.5, 26.5, 22.5, 16, 9.5, 8, 5.6, 4.75] #Sieve size in mm
Percentage_passing = [100, 100, 100, 97.91, 78.78, 36.01, 3.61, 2.65, 1.66, 1.62] #Percentage passing

#Plotting the data with Ordinate as Percentage passing and abscissa as Sieve size
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Sample information text - now used as heading
info_text = "Sample: Coarse Aggregates | Test Date: April 30, 2025 | Lab: Transportation Engineering"

# Convert sieve size to natural logarithm
ln_Sieve_size = np.log(Sieve_size)

plt.figure(figsize=(8, 6))

# Create a smoother curve using spline interpolation
# Generate more points for a smoother curve
ln_Sieve_size_array = np.array(ln_Sieve_size)
percentage_array = np.array(Percentage_passing)

# Sort arrays by ln_Sieve_size for proper interpolation (important for spline)
sort_indices = np.argsort(ln_Sieve_size_array)
ln_Sieve_size_array = ln_Sieve_size_array[sort_indices]
percentage_array = percentage_array[sort_indices]

# Generate a smooth curve with more points
ln_Sieve_size_smooth = np.linspace(ln_Sieve_size_array.min(), ln_Sieve_size_array.max(), 300)
spl = make_interp_spline(ln_Sieve_size_array, percentage_array, k=3)  # k=3 for cubic spline
percentage_smooth = spl(ln_Sieve_size_smooth)

# Plot the smooth curve
plt.plot(ln_Sieve_size_smooth, percentage_smooth, linestyle='-', color='#3366FF', 
         linewidth=2.5, label='Gradation Curve')

# Plot the original data points
plt.plot(ln_Sieve_size, Percentage_passing, marker='o', linestyle='', color='#3366FF', 
         markersize=6, markerfacecolor='white', markeredgecolor='#3366FF', 
         markeredgewidth=1.5)

# Add grid with custom styling
plt.grid(True, which='both', linestyle='--', linewidth=0.8, alpha=0.7)

# Setting labels and title with custom fonts
plt.xlabel('ln(Sieve Size) [ln(mm)]', fontsize=10, fontweight='bold')
plt.ylabel('Percentage Passing (%)', fontsize=10, fontweight='bold')

# Add info text as title/heading
plt.title(f"Gradation Curve of Coarse Aggregates\n{info_text}", fontsize=11, 
          fontweight='bold', pad=15, color='#333333')

# Customizing the axes
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_linewidth(1.5)
plt.gca().spines['left'].set_linewidth(1.5)

# Invert x-axis to follow standard practice (larger sieve sizes on the left)
plt.gca().invert_xaxis()

# Create custom x-tick labels showing original sieve size
ln_ticks = ln_Sieve_size[::2]  # Use every other point to avoid crowding
original_ticks = [f"{size}" for size in Sieve_size[::2]]
plt.xticks(ln_ticks, original_ticks, rotation=45)

# Add annotations for key points
for i, (ln_size, percent) in enumerate(zip(ln_Sieve_size, Percentage_passing)):
    if i % 2 == 0:  # Annotate every other point to avoid clutter
        plt.annotate(f'{percent}%', 
                     xy=(ln_size, percent), 
                     xytext=(-5, 7),
                     textcoords='offset points',
                     fontsize=7,
                     fontweight='bold')

# Set y-axis limits with some padding
plt.ylim(0, 105)

# Add a light background color for better contrast
plt.gca().set_facecolor('#F8F9FA')
plt.gcf().set_facecolor('#FFFFFF')

# Create a legend box in top right corner with scale information
scale_text = "Scale:\nX-axis: ln(mm)\nY-axis: Percentage (%)"
legend_elements = [
    plt.Line2D([0], [0], color='#3366FF', lw=2.5, label='Gradation Curve'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white', 
               markeredgecolor='#3366FF', markersize=6, label=scale_text)
]
plt.legend(handles=legend_elements, loc='upper right', frameon=True, 
           framealpha=0.9, fontsize=9, title_fontsize=9,
           bbox_to_anchor=(0.98, 0.98), title="Legend")

# First call tight_layout to adjust the plot area
plt.tight_layout()

# Save as SVG with bbox_inches='tight' to include the text outside the axes
plt.savefig('aggregate_gradation_curve_smooth.svg', format='svg', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()



