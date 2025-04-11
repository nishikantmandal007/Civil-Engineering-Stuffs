import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import griddata # Import for smoothing contours

# --- Input Data ---
staff_readings_list = [
   [1.890, 1.930, 1.925, 1.955, 2.020, 2.155, 2.240, 2.320, 2.395, 2.425, 2.450],
   [1.815, 1.860, 1.895, 1.940, 2.030, 2.095, 2.250, 2.295, 2.320, 2.365, 2.440],
   [1.775, 1.820, 1.850, 1.925, 2.025, 2.100, 2.200, 2.245, 2.280, 2.350, 2.415],
   [1.850, 1.780, 1.830, 1.940, 2.020, 2.100, 2.165, 2.185, 2.245, 2.275, 2.335],
   [1.760, 1.810, 1.845, 1.940, 2.010, 2.070, 2.145, 2.145, 2.155, 2.255, 2.350],
   [1.760, 1.785, 1.830, 1.910, 1.980, 2.045, 2.030, 2.080, 2.150, 2.230, 2.295],
   [1.700, 1.790, 1.835, 1.915, 1.965, 2.010, 1.985, 2.070, 2.125, 2.210, 2.150],
   [1.720, 1.800, 1.855, 1.870, 1.915, 1.965, 1.985, 2.070, 2.125, 2.210, 2.150],
   [1.730, 1.770, 1.810, 1.835, 1.895, 1.875, 1.965, 2.020, 2.110, 2.170, 2.280],
   [1.655, 1.735, 1.755, 1.820, 1.855, 1.800, 1.950, 2.040, 2.110, 2.060, 2.260],
   [1.695, 1.700, 1.700, 1.800, 1.850, 1.835, 1.965, 2.050, 2.120, 2.180, 2.240]
   ]
HOI = 150.250  # Height of Instrument (m)
grid_spacing = 2  # meters
grid_dimension = 20 # meters

# --- Data Preparation ---
flipped = np.flipud(staff_readings_list)
staff_readings = np.array(flipped)

# --- Calculations ---
rl_values = HOI - staff_readings
num_points_y, num_points_x = staff_readings.shape
x_coords = np.linspace(0, grid_dimension, num_points_x)
y_coords = np.linspace(0, grid_dimension, num_points_y)
X_orig, Y_orig = np.meshgrid(x_coords, y_coords)

# --- Interpolation for Smoothing ---
points = np.array([X_orig.ravel(), Y_orig.ravel()]).T
values = rl_values.ravel()
grid_x_fine, grid_y_fine = np.mgrid[0:grid_dimension:200j, 0:grid_dimension:200j]
print("Interpolating data for smoother contours...")
grid_z_fine = griddata(points, values, (grid_x_fine, grid_y_fine), method='cubic')

# --- Plotting ---
print("Generating contour map...")

# Define figure size
fig, ax = plt.subplots(figsize=(9, 9.5)) # Adjusted height slightly

# Set background color to white
fig.patch.set_facecolor('white')
ax.patch.set_facecolor('white')

# Define contour levels
min_rl = np.nanmin(rl_values)
max_rl = np.nanmax(rl_values)
contour_levels = np.arange(np.floor(min_rl * 20) / 20, np.ceil(max_rl * 20) / 20 + 0.05, 0.05)
print(f"Calculated RL Range: {min_rl:.3f}m to {max_rl:.3f}m")
print(f"Using Contour Levels: {contour_levels}")


# Plot the SMOOTH contour lines using the FINE grid
CS = ax.contour(grid_x_fine, grid_y_fine, grid_z_fine,
                levels=contour_levels, colors='blue', linewidths=1.0)

# Add labels to the contour lines
ax.clabel(CS, inline=True, fontsize=8, fmt='%1.2f')

# Plot the ORIGINAL grid points and their RL values
for i in range(num_points_y):
    for j in range(num_points_x):
        ax.plot(x_coords[j], y_coords[i], 'ko', markersize=3)
        if i < rl_values.shape[0] and j < rl_values.shape[1]:
             ax.text(x_coords[j], y_coords[i] + 0.15, f'{rl_values[i, j]:.3f}',
                     ha='center', va='bottom', fontsize=7, color='black')

# --- Add North Arrow (Centered) ---
arrow_base_x = 10
arrow_base_y = 10
arrow_length = 1.5
north_angle_deg_from_vertical_west = 30 # The angle given: 30 deg West of Vertical
north_angle_deg = 90 + north_angle_deg_from_vertical_west # Angle from +X axis (Easting)
north_angle_rad = math.radians(north_angle_deg)
arrow_dx = arrow_length * math.cos(north_angle_rad)
arrow_dy = arrow_length * math.sin(north_angle_rad)
ax.arrow(arrow_base_x, arrow_base_y, arrow_dx, arrow_dy,
         head_width=0.4, head_length=0.6, fc='black', ec='black',
         length_includes_head=True, zorder=10)
label_offset = 0.4
label_x = arrow_base_x + arrow_dx
label_y = arrow_base_y + arrow_dy + label_offset
ax.text(label_x, label_y, 'N', fontsize=12, fontweight='bold',
        ha='center', va='bottom', zorder=10)
ax.text(label_x, label_y, f"({north_angle_deg_from_vertical_west}° W)",
        fontsize=7, ha='center', va='top', zorder=10)

# --- Formatting Main Plot Area ---
ax.set_xticks(x_coords)
ax.set_yticks(y_coords)
ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')
ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")
ax.set_title(f"Contour Map (HOI = {HOI:.3f} m) \n Site: Area between Admin building and Mining Department")
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-grid_spacing / 2, grid_dimension + grid_spacing / 2)
ax.set_ylim(-grid_spacing / 2, grid_dimension + grid_spacing / 2)

# --- Add Instrument Symbol OUTSIDE Axes ---
plt.subplots_adjust(bottom=0.15, top=0.9, right=0.9) # Adjust margins for symbols
fig.text(0.02, 0.13, "Instrument\nPosition", ha='center', va='baseline', fontsize=9, color='red')
fig.text(0.02, 0.18, u"▶", ha='center', va='baseline', fontsize=12, color='red')

# --- Add Rotated Cardinal Direction Rose with Degrees ---
# Create a small inset axes in the top-left corner (moved from top-right for colorbar)
ax_rose = fig.add_axes([-0.01, 0.90, 0.1, 0.1]) # Position near top LEFT, slightly larger
ax_rose.axis('off')

center_x, center_y = 0.5, 0.5
arm_len = 0.30 # Shorter arms
label_dist = arm_len + 0.18 # Distance for N,E,S,W labels
ref_len = arm_len + 0.08 # Length for reference cross
degree_dist = ref_len + 0.12 # Distance for degree labels

# 1. Draw Reference Cross (aligned with map grid)
ax_rose.plot([center_x - ref_len, center_x + ref_len], [center_y, center_y],
             color='grey', linestyle=':', lw=1) # Horizontal (Map East-West)
ax_rose.plot([center_x, center_x], [center_y - ref_len, center_y + ref_len],
             color='grey', linestyle=':', lw=1) # Vertical (Map North-South)

# 2. Add Degree Labels for Reference Cross
ax_rose.text(center_x + degree_dist, center_y, '0°', color='grey', fontsize=7, ha='left', va='center') # East
ax_rose.text(center_x, center_y + degree_dist, '90°', color='grey', fontsize=7, ha='center', va='bottom') # North
ax_rose.text(center_x - degree_dist, center_y, '180°', color='grey', fontsize=7, ha='right', va='center') # West
ax_rose.text(center_x, center_y - degree_dist, '270°', color='grey', fontsize=7, ha='center', va='top') # South


# 3. Define True Cardinal Directions (Angles from Map +X axis)
directions = { 'N': 120, 'E': 30, 'S': -60, 'W': 210 }

# 4. Draw Rotated Arms and Labels
for label, angle_deg in directions.items():
    angle_rad = math.radians(angle_deg)
    # Arm endpoint
    end_x = center_x + arm_len * math.cos(angle_rad)
    end_y = center_y + arm_len * math.sin(angle_rad)
    # Label position
    lab_x = center_x + label_dist * math.cos(angle_rad)
    lab_y = center_y + label_dist * math.sin(angle_rad)

    # Draw arm
    ax_rose.plot([center_x, end_x], [center_y, end_y], 'k-', lw=1.5)
    # Draw label
    ax_rose.text(lab_x, lab_y, label, ha='center', va='center', fontsize=8, fontweight='bold')


# --- SAVE FIGURE ---
# **Important:** Add this line BEFORE plt.show()
output_filename = 'contour_uncolored.svg'
fig.savefig(output_filename, format='svg', bbox_inches='tight')
print(f"Map saved as SVG: {output_filename}")

# Display the plot
plt.show()


print("\n--- Reduced Levels (RLs) Grid (Original Data - Flipped Input) ---")
# Print the RL values in a grid format for reference
print("   ", end="")
for x in x_coords:
    print(f"{x:6.1f}m", end=" ")
print("\n" + "-" * (8 * num_points_x + 4))
for i in range(num_points_y):
    print(f"{y_coords[i]:4.1f}m|", end="")
    for j in range(num_points_x):
        print(f"{rl_values[i, j]:7.3f}", end=" ")
    print()