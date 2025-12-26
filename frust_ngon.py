# This tool was built to help determine required cut sizes for small stained glass
# lampshades to be placed over small glasses as the lamp base. It uses matplotlib
# for visualizations and numpy to assist with wrangling data.  Otherwise, just
# straight math.  The repository includes a standalone distributable .EXE file
# for use on a Windows computer, but can also be executed from source.

# In general, the lampshade is represented by a frustum - a pyramidal shape
# with the top chopped off, creating a shape with parallel top and base.  The code
# permits the user to change various features of the frustum using a dynamically
# updating graphical interface, while text on the screen provides various key feedback
# to the user necessary for planning out cut lengths for individual glass pieces.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# setting initial parameters
init_sides = 5  # pentagonal shade was an initial request, so this is the default setting
f_h = 5.0       # total height set at 5cm

# establish basic plotting parameters
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.3)

# key helper functions
def get_face_vertices(radius, z, sides):
    # calculates coordinates for individual faces of frustum being built and returns as an array.
    # takes a desired radius, z-coordinate, and desired number of sides as inputs, then
    # utilizes polar coordinates, stopping at [sides+1] individual points distributed uniformly
    # around a circle to identify which angles the points will be at.  These are transformed with
    # cosine and sine operations to generate x and y coordinates, respectively, which are combined
    # with identified z-height and returned as an array.
    angles = np.linspace(0, 2 * np.pi, sides+1)[:-1]
    return np.array([[radius * np.cos(a), radius * np.sin(a), z] for a in angles])

def get_face_midpoints(inradius, z, sides):
    # knowledge of the interior dimensions of the frustum is required to calculate the intersection
    # of the interior column (representing the glass base) with the frustum (the lampshade), as
    # well as the height of each pane of glass.  This function takes the desired interior radius
    # the height [z] and the number of sides of the frustum.  Using math similar to the [get_face_vertices]
    # function, the function creates an array of [x,y,z] coordinates for each of the midpoints of each of
    # the faces of the frustum shape.
    angles = np.linspace(0, 2 * np.pi, sides+1)[:-1] + np.pi / 5
    return np.array([[inradius * np.cos(a), inradius * np.sin(a), z] for a in angles])

def get_inradius(s_len, sides):
    # helper function to generate an interior radius based on a number of sides of the frustum
    # and the length of each of those sides
    return (s_len/2)/np.tan(np.radians(180/sides))

def update_plot(f_bot_R, f_top_R, c_r, sides):
    # graphics routines for visualization

    ax.clear()

    # Math for Intersection of Frustum (lampshade) and cylinder (glass)
    COS36 = np.cos(np.radians(180 / sides))
    r_bot, r_top = f_bot_R * COS36, f_top_R * COS36
    if abs(r_top - r_bot) > 1e-5:
        z_int = (c_r - r_bot) * (f_h / (r_top - r_bot))
    else:
        z_int = -1

    z_vis = np.clip(z_int, 0, f_h)

    # Draw Frustum
    v_bot = get_face_vertices(f_bot_R, 0, sides)
    v_top = get_face_vertices(f_top_R, f_h, sides)
    faces = [v_bot, v_top]

    for i in range(sides):
        faces.append(np.array([v_bot[i], v_bot[(i + 1) % sides], v_top[(i + 1) % sides], v_top[i]]))
    ax.add_collection3d(Poly3DCollection(faces, alpha=0.15, edgecolor='k', facecolors='cyan'))

    # Calculate lengths of sides for glass cuts
    v_bot_len = np.sqrt((v_bot[0][0] - v_bot[1][0]) ** 2 + (v_bot[0][1] - v_bot[1][1]) ** 2)
    v_top_len = np.sqrt((v_top[0][0] - v_top[1][0]) ** 2 + (v_top[0][1] - v_top[1][1]) ** 2)
    m_top = get_face_midpoints(get_inradius(v_top_len, sides), f_h, sides)
    m_bot = get_face_midpoints(get_inradius(v_bot_len, sides), 0, sides)
    m_len = np.sqrt((m_top[0][0] - m_bot[0][0])**2 + (m_top[0][1] - m_bot[0][1])**2 + (m_top[0][2] - m_bot[0][2])**2)

    # Draw a segmented cylinder, meant to provide a graphical representation of the glass
    # Arbitrarily skinny at Z<=0 to represent the stem of the glass, and dynamically wide
    # above that to represent the diameter of the glass being used as the lamp base.
    # Define two Z ranges: [-2, 0] (fixed) and [0, z_vis] (dynamic)
    z_fixed = np.linspace(-2, 0, 10)
    z_dynamic = np.linspace(0, z_vis if z_int > 0 else 0.01, 20)
    z_total = np.concatenate([z_fixed, z_dynamic])

    # Define corresponding radii for each Z slice
    r_total = np.concatenate([np.ones(10), np.full(20, c_r)])

    theta = np.linspace(0, 2 * np.pi, 40)
    # Use broadcasting to create X, Y coordinates for each Z slice
    T, Z = np.meshgrid(theta, z_total)
    # Map each Z slice to its respective radius from r_total
    R_grid = np.tile(r_total, (40, 1)).T

    ax.plot_surface(R_grid * np.cos(T), R_grid * np.sin(T), Z, alpha=0.5, color='orange')

    # Plot intersection points and add user feedback
    if 0 <= z_int <= f_h:
        pts = get_face_midpoints(c_r, z_int, sides)
        ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color='red', s=80)
        ax.set_title(f"Height of glass covered = {z_int:.2f}\n"
                     f"Shade top length = {v_top_len:.1f}\n"
                     f"Shade bottom length = {v_bot_len:.1f}\n"
                     f"Shade length = {m_len:.1f}\n")
    else:
        ax.set_title("No Side Intersection")

    ax.set_xlim(-5, 5);
    ax.set_ylim(-5, 5);
    ax.set_zlim(-2, f_h)
    fig.canvas.draw_idle()

# UI Sliders
ax_bot = plt.axes([0.2, 0.18, 0.6, 0.03])
ax_top = plt.axes([0.2, 0.13, 0.6, 0.03])
ax_cyl = plt.axes([0.2, 0.08, 0.6, 0.03])
ax_sides = plt.axes([0.2, 0.03, 0.6, 0.03])

s_bot = Slider(ax_bot, 'Shade bottom', 1.0, 15.0, valinit=4.0, valstep = 0.1)
s_top = Slider(ax_top, 'Shade top', 0.5, 10.0, valinit=1.0, valstep = 0.1)
s_cyl = Slider(ax_cyl, 'Glass radius', 2.0, 6.0, valinit=2.0, valstep = 0.1)
s_sid = Slider(ax_sides, 'Num Sides', 4, 8, valinit=5, valstep = 1)

def update(val):
    update_plot(s_bot.val, s_top.val, s_cyl.val, s_sid.val)


s_bot.on_changed(update)
s_top.on_changed(update)
s_cyl.on_changed(update)
s_sid.on_changed(update)

update_plot(4.0, 1.0, 2.0, init_sides)
# Run this in full screen as the default
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
plt.show()
