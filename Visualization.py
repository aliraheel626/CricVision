import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


from library import estimate_bounce_point,estimate_impact_point,estimate_trajectory,estimate_release_point,estimate_bowling_side,estimate_btasman_side

BATSMAN_HEIGHT=191
CORNER_POINT_A=(-140,0,0)
CORNER_POINT_B=(140,0,0)
CORNER_POINT_C=(166, -321,0)
CORNER_POINT_D=(-166, -321,0)


def plot_all_3D(detections):
    # Creating figure
    fig = plt.figure(figsize=(16, 9))
    ax = plt.axes(projection="3d")

    # Add x, y gridlines
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.3, alpha=0.1)

    # Creating color map
    my_cmap = plt.get_cmap('hsv')

    # finding the bowling side
    bowling_side = estimate_bowling_side(detections)

    # Release Point
    (X, Y, Z) = estimate_release_point(bowling_side)
    ax.scatter3D(X, Y, Z, color="green")

    # Bounce Point
    (X_bounce, Y_bounce) = estimate_bounce_point(detections)
    if X_bounce is not None and Y_bounce is not None:
        ax.scatter3D(X_bounce, Y_bounce, 0, color="black")

    # Impact Point
    (X_impact, Y_impact) = estimate_impact_point(detections)
    if X_impact is not None and Y_impact is not None:
        ax.scatter3D(X_impact, 0, Y_impact, color="red")

    # Trajectory Point (after impact point)
    (X_trajectory, Y_trajectory) = estimate_trajectory(detections)
    # if trajectory Point is Known
    if X_trajectory is not None and Y_trajectory is not None:
        ax.scatter3D(X_trajectory, 0, Y_trajectory, color="blue")

    # Batsman
    ax.scatter3D(0, 0, 0)

    # -----------------------------------------------------------------------------------

    # Draw rectangle (for Pitch Boundary)
    corner_points = [
        CORNER_POINT_A,
        CORNER_POINT_B,
        CORNER_POINT_C,
        CORNER_POINT_D,
        CORNER_POINT_A
    ]

    # Extract the x, y, and z coordinates from the corner points
    x = [point[0] for point in corner_points]
    y = [point[1] for point in corner_points]
    z = [point[2] for point in corner_points]

    # Connect the corner points to form a rectangle
    plt.plot([x[0], x[1]], [y[0], y[1]], [z[0], z[1]], 'r')
    plt.plot([x[1], x[2]], [y[1], y[2]], [z[1], z[2]], 'r')
    plt.plot([x[2], x[3]], [y[2], y[3]], [z[2], z[3]], 'r')
    plt.plot([x[3], x[0]], [y[3], y[0]], [z[3], z[0]], 'r')

    # To fill the Pitch area
    polygon = [corner_points]
    poly = Poly3DCollection(polygon, alpha=0.5)
    poly.set_color((128 / 255, 128 / 255, 128 / 255))
    ax.add_collection3d(poly)

    # -----------------------------------------------------------------------------------

    # Plot lines to draw the uppper wicket
    # verticle lines
    y11_w1, y21_w1 = [CORNER_POINT_A[1] + 1, CORNER_POINT_A[1] + 70]
    plt.plot([0, 0], [0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    # # Horizontal Lines
    y12_w1, y22_w1 = [CORNER_POINT_A[1] + 70, CORNER_POINT_A[1] + 70]
    plt.plot([0 - 8, 0], [0, 0], [y12_w1, y22_w1], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [0, 0], [y12_w1, y22_w1], 'black', linewidth=3)

    # -----------------------------------------------------------------------------------
    # To fill the piching line
    pitching_line = [
        (-11, 0, 0),
        (11, 0, 0),
        (11, -321, 0),
        (-11, -321, 0)
    ]

    # fill the pitching line
    polygon = [pitching_line]
    poly = Poly3DCollection(polygon, alpha=0.5)
    poly.set_color((65 / 255, 105 / 255, 225 / 255))
    ax.add_collection3d(poly)

    # -----------------------------------------------------------------------------------

    # pixel/meter
    factor = 18.17
    # stups point
    stumpA = CORNER_POINT_A[1] + (1.22 * factor)
    stumpB = CORNER_POINT_B[1] + (1.22 * factor)
    # define the y values for every line
    y_values_A = [
        (CORNER_POINT_A[1]),
        stumpA - (2 * factor),
        stumpA - (4 * factor),
        stumpA - (6 * factor),
        stumpA - (7 * factor),
        stumpA - (8 * factor)
    ]

    y_values_B = [
        (CORNER_POINT_B[1]),
        stumpB - (2 * factor),
        stumpB - (4 * factor),
        stumpB - (6 * factor),
        stumpB - (7 * factor),
        stumpB - (8 * factor)
    ]

    # Plot lines for the checking of ball
    plt.plot([CORNER_POINT_A[0], CORNER_POINT_B[0] + 150], [y_values_A[1], y_values_B[1]], 'r-', linewidth=1.5,
             color='black')
    ax.text(CORNER_POINT_B[0] + 81, y_values_A[1] + 3, 0, 'YORKER LENGTH (0-2m)', color='black', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 2, CORNER_POINT_B[0] + 150], [y_values_A[2], y_values_B[2]], linestyle='dotted',
             linewidth=1.5, color='black')
    ax.text(CORNER_POINT_B[0] + 77, y_values_A[2] + 15, 0, 'FULL LENGTH (2-4m)', color='black', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 5, CORNER_POINT_B[0] + 150], [y_values_A[3], y_values_B[3]], linewidth=1.5,
             color='black')
    ax.text(CORNER_POINT_B[0] + 77, y_values_A[3] + 15, 0, 'FULL LENGTH (4-6m)', color='black', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 6, CORNER_POINT_B[0] + 150], [y_values_A[4], y_values_B[4]], linestyle='dotted',
             linewidth=1.5, color='black')
    ax.text(CORNER_POINT_B[0] + 80, y_values_A[4] + 5, 0, 'GOOD LENGTH (6-7m)', color='black', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 8, CORNER_POINT_B[0] + 150], [y_values_A[5], y_values_B[5]], linewidth=1.5,
             color='black')
    ax.text(CORNER_POINT_B[0] + 85, y_values_A[5] + 5, 0, 'BACK OF LENGTH (7-8m)', color='black', fontsize=6)

    ax.text(CORNER_POINT_B[0] + 85, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, 0, 'SHORT LENGTH (>8m)',
            color='black', fontsize=6)

    # -----------------------------------------------------------------------------------

    # to draw the body of Batsman

    # Define the height and width scaling factors
    height_scale = 191
    extra_height = 20
    total_height = height_scale + extra_height
    width_scale = 141

    # Draw the head
    # Set the position and size of the circle
    center = (0, 0, height_scale - (0.15 * width_scale))
    radius = 0.15 * width_scale
    # Create a 3D circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x = center[0] + radius * np.cos(theta)
    y = np.full_like(theta, center[1])
    z = center[2] + radius * np.sin(theta)
    # Plot the circle in 3D
    plt.plot(x, y, z, color='black')

    # Draw the body
    plt.plot([0, 0], [0, 0], [height_scale - (0.3 * width_scale), height_scale * 0.2], linewidth=1.5, color='black')

    # Draw the ARMS
    # Right Arm
    plt.plot([0, 20], [0, 0], [150, 100], linewidth=1.5, color='black')
    # Left Arm
    plt.plot([0, -20], [0, 0], [150, 100], linewidth=1.5, color='black')

    # Draw the  legs
    # Right leg
    plt.plot([0, 20], [0, 0], [50, 0], linewidth=1.5, color='black')
    # Left Leg
    plt.plot([0, -20], [0, 0], [50, 0], linewidth=1.5, color='black')

    # -----------------------------------------------------------------------------------
    # Plot the arrow between points

    if X_bounce is not None and Y_bounce is not None and X_impact is not None and Y_impact is not None:
        arrow_vector = [X_bounce - X, Y_bounce - Y, 0 - Z]
        ax.quiver(X, Y, Z, arrow_vector[0], arrow_vector[1], arrow_vector[2]
                  , arrow_length_ratio=0)

        arrow_vector = [X_impact - X_bounce, 0 - Y_bounce, Y_impact - 0]
        ax.quiver(X_bounce, Y_bounce, 0, arrow_vector[0], arrow_vector[1], arrow_vector[2]
                  , arrow_length_ratio=0)

        # if the Trajectory pooint is known
        if X_trajectory is not None and Y_trajectory is not None:
            arrow_vector = [X_trajectory - X_impact, 0 - 0, Y_trajectory - Y_impact]
            ax.quiver(X_impact, 0, Y_impact, arrow_vector[0], arrow_vector[1], arrow_vector[2]
                      , arrow_length_ratio=0)

    # -----------------------------------------------------------------------------------

    # Set labels for the axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # box height and width
    ax.set_box_aspect([2.5, 4.5, 1])
    return plt


def plot_bounce_2D(detections):
    # finding the bounce point
    (x_bounce, y_bounce) = estimate_bounce_point(detections)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Points to be plot
    x = [x_bounce]
    y = [y_bounce]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Creating figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot lines to draw the uppper wicket
    # verticle lines
    y11_w1, y21_w1 = [CORNER_POINT_A[1] + 1, CORNER_POINT_A[1] + 50]
    plt.plot([0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w1, y21_w1], 'black', linewidth=3)
    # Horizontal Lines
    y12_w1, y22_w1 = [CORNER_POINT_A[1] + 52, CORNER_POINT_A[1] + 52]
    plt.plot([0 - 8, 0], [y12_w1, y22_w1], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w1, y22_w1], 'black', linewidth=3)

    # Plot lines to draw the lower wicket
    # verticle lines
    y11_w2, y21_w2 = [CORNER_POINT_C[1] + 1, CORNER_POINT_C[1] + 50]
    plt.plot([0, 0], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w2, y21_w2], 'black', linewidth=3)
    # Horizontal Lines
    y12_w2, y22_w2 = [CORNER_POINT_C[1] + 52, CORNER_POINT_C[1] + 52]
    plt.plot([0 - 8, 0], [y12_w2, y22_w2], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w2, y22_w2], 'black', linewidth=3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Draw the Pitch and fill the color bw it
    polygon = plt.Polygon([(CORNER_POINT_A[0], CORNER_POINT_A[1]), (CORNER_POINT_B[0], CORNER_POINT_B[1]),
                           (CORNER_POINT_C[0], CORNER_POINT_C[1]), (CORNER_POINT_D[0], CORNER_POINT_D[1])],
                          facecolor=(138 / 255, 133 / 255, 109 / 255), edgecolor='red')
    ax.add_patch(polygon)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # # plot lines wicket to wicket
    # plt.plot([0-11,0-11], [CORNER_POINT_A[1], CORNER_POINT_C[1]], 'black', linewidth=0)
    # plt.plot([0+11,0+11], [CORNER_POINT_A[1], CORNER_POINT_C[1]], 'black', linewidth=0)

    # fill the area between the two vertical lines
    plt.fill_betweenx([CORNER_POINT_A[1], CORNER_POINT_C[1]], 0 - 11, 0 + 11, color='lightblue', alpha=0.3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # define the color for points
    colors = ['black']

    # Plot the points
    if x_bounce is not None and y_bounce is not None:
        ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Lines in the pitch

    # pixel/meter
    factor = 18.17
    # stups point
    stumpA = CORNER_POINT_A[1] + (1.22 * factor)
    stumpB = CORNER_POINT_B[1] + (1.22 * factor)
    # define the y values for every line
    y_values_A = [
        (CORNER_POINT_A[1]),
        stumpA - (2 * factor),
        stumpA - (4 * factor),
        stumpA - (6 * factor),
        stumpA - (7 * factor),
        stumpA - (8 * factor)
    ]

    y_values_B = [
        (CORNER_POINT_B[1]),
        stumpB - (2 * factor),
        stumpB - (4 * factor),
        stumpB - (6 * factor),
        stumpB - (7 * factor),
        stumpB - (8 * factor)
    ]

    # Plot lines for the checking of ball
    plt.plot([CORNER_POINT_A[0], CORNER_POINT_B[0] + 150], [y_values_A[1], y_values_B[1]], 'r-', linewidth=0.5,
             color='black')
    plt.text(CORNER_POINT_B[0] + 81, y_values_A[1] + 3, 'YORKER LENGTH (0-2m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 2, CORNER_POINT_B[0] + 150], [y_values_A[2], y_values_B[2]], linestyle='dotted',
             linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[2] + 15, 'FULL LENGTH (2-4m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 5, CORNER_POINT_B[0] + 150], [y_values_A[3], y_values_B[3]], linewidth=0.5,
             color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[3] + 15, 'FULL LENGTH (4-6m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 6, CORNER_POINT_B[0] + 150], [y_values_A[4], y_values_B[4]], linestyle='dotted',
             linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 80, y_values_A[4] + 5, 'GOOD LENGTH (6-7m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 8, CORNER_POINT_B[0] + 150], [y_values_A[5], y_values_B[5]], linewidth=0.5,
             color='black')
    plt.text(CORNER_POINT_B[0] + 85, y_values_A[5] + 5, 'BACK OF LENGTH (7-8m)', ha='center', fontsize=6)

    plt.text(CORNER_POINT_B[0] + 85, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, 'SHORT LENGTH (>8m)',
             ha='center', fontsize=6)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Bounce Point')

    # return the plot
    return plt


def plot_impact1_2D(detections):
    # Define  the height and width scaling factors
    height_scale = 191
    extra_height = 20
    total_height = height_scale + extra_height
    width_scale = 141

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # finding the impact points
    (x_impact, y_impact) = estimate_impact_point(detections)
    print(x_impact, y_impact)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the coordinates of the points to plot
    x = [x_impact]
    y = [y_impact]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # creating figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    colors = ['r']  # colors for each point

    # Plot the impact points
    if x_impact is not None and y_impact is not None:
        scatter = ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set the x-axis and y-axis limits
    plt.xlim(-width_scale, width_scale)
    plt.ylim(0, total_height)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Load and display the image
    image_path = 'a.jpg'
    image = plt.imread(image_path)
    if estimate_btasman_side(detections) == "RIGHT HANDED BATSMAN":
        ax.imshow(image, extent=[width_scale, -width_scale, -10, total_height])
    else:
        ax.imshow(image, extent=[-width_scale, width_scale, -10, total_height])

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Impact Point')

    return plt


def plot_impact2_2D(detections):
    # Define the height and width scaling factors
    height_scale = 191
    extra_height = 20
    total_height = height_scale + extra_height
    width_scale = 141

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # creating figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # finding the impact_points
    (x_impact, y_impact) = estimate_impact_point(detections)
    print(x_impact, y_impact)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the coordinates of the points to plot
    x = [x_impact]
    y = [y_impact]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    colors = ['r']  # colors for each point
    # Plot the impact_points
    scatter = ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Draw the head
    head = plt.Circle((0, height_scale - (0.15 * width_scale)), 0.15 * width_scale, color='black')
    ax.add_artist(head)

    # Draw the body
    body = plt.Line2D([0, 0], [height_scale * 0.9, height_scale * 0.2], color='black', linewidth=3)
    ax.add_artist(body)

    # Draw the arms
    left_arm = plt.Line2D([0, -0.2 * width_scale], [height_scale * 0.6, height_scale * 0.4], color='black')
    ax.add_artist(left_arm)
    right_arm = plt.Line2D([0, 0.2 * width_scale], [height_scale * 0.6, height_scale * 0.4], color='black')
    ax.add_artist(right_arm)

    # Draw the hands
    left_hand = plt.Circle((-0.2 * width_scale, height_scale * 0.4), 2, color='black')
    ax.add_artist(left_hand)
    right_hand = plt.Circle((0.2 * width_scale, height_scale * 0.4), 2, color='black')
    ax.add_artist(right_hand)

    # Draw the legs
    left_leg = plt.Line2D([0, -0.2 * width_scale], [height_scale * 0.2, 0], color='black')
    ax.add_artist(left_leg)
    right_leg = plt.Line2D([0, 0.2 * width_scale], [height_scale * 0.2, 0], color='black')
    ax.add_artist(right_leg)

    # Draw the foots
    left_hand = plt.Circle((-0.2 * width_scale, 0.2), 2, color='black')
    ax.add_artist(left_hand)
    right_hand = plt.Circle((0.2 * width_scale, 0.2), 2, color='black')
    ax.add_artist(right_hand)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set the x-axis and y-axis limits
    plt.xlim(-width_scale, width_scale)
    plt.ylim(0, total_height)
    # plt.axis('off')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Impact Point')

    return plt


def plot_trajectory_2D(detections):
    # creating figure
    fig, ax = plt.subplots()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # finding the impact points
    (x_impact, y_impact) = estimate_impact_point(detections)
    (x_trajectory, y_trajectory) = estimate_trajectory(detections)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # if the Trajectory Point is known
    if x_trajectory is not None and y_trajectory is not None:
        # Define the coordinates of the points to plot
        x = [x_impact, x_trajectory]
        y = [y_impact, y_trajectory]

        (x_new_trajectory, y_new_trajectory) = (x_trajectory - x_impact, y_trajectory - y_impact)

        # Now the impact point will be (0,0)
        x = [0, x_new_trajectory]
        y = [0, y_new_trajectory]

        # Calculate the vector
        vector = (x[1] - x[0], y[1] - y[0])

        # Calculate the magnitude of the vector
        magnitude = (vector[0] ** 2 + vector[1] ** 2) ** 0.5

        try:
            # Calculate the unit vector
            unit_vector = (vector[0] / magnitude, vector[1] / magnitude)
            # New point will be origin and unit vector
            x = [0, unit_vector[0]]
            y = [0, unit_vector[1]]
        except:
            pass

    else:
        x = [0]
        y = [0]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add an ellipse (four ground)
    ellipse = Ellipse(xy=(0, 0), width=4, height=5.5, edgecolor='blue', facecolor='green')
    ax.add_patch(ellipse)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # # Add a colored square at the midpoint(mini pitch)
    # square = Rectangle((-0.125, -0.7), 0.25, 1, facecolor=(0.3, 0.29, 0))
    # ax.add_patch(square)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if x_trajectory and y_trajectory:
        colors = ['white', 'blue']  # Colors for each point
        # Plot the points
        ax.scatter(x, y, c=colors)
    else:
        colors = ['white']  # Colors for each point
        # Plot the points
        ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if x_trajectory is not None and y_trajectory is not None:
        # Plot an arrow between the two points
        plt.annotate('', xy=(x[1], y[1]), xytext=(x[0], y[0]), arrowprops=dict(arrowstyle='->', color='yellow'))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # # Add text on the left and right side of the impact point
    # if estimate_btasman_side(detections) == "RIGHT HANDED BTSMAN":
    #     plt.text(0 - 1.5, 0, 'OFF SIDE ', fontsize=12)
    #     plt.text(0 + 0.7, 0, 'LEG SIDE', fontsize=12)
    # else:
    #     plt.text(0 - 1.5, 0, 'LEG SIDE', fontsize=12)
    #     plt.text(0 + 0.7, 0, 'OFF SIDE', fontsize=12)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set the x-axis and y-axis limits
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Trajectory')

    # Display the plot
    return plt


def plot_all_2D(detections):
    # finding all the points
    bowling_side = estimate_bowling_side(detections)
    (X, Y, Z) = estimate_release_point(bowling_side)
    (x_bounce, y_bounce) = estimate_bounce_point(detections)
    (x_impact, y_impact) = estimate_impact_point(detections)
    (x_trajectory, y_trajectory) = estimate_trajectory(detections)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Points to be ploted
    x = [X, x_bounce, x_impact, x_trajectory]
    y = [Y, y_bounce, y_impact, y_trajectory]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # creating figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot lines to draw the uppper wicket
    # verticle lines
    y11_w1, y21_w1 = [CORNER_POINT_A[1] + 1, CORNER_POINT_A[1] + 50]
    plt.plot([0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w1, y21_w1], 'black', linewidth=3)
    # Horizontal Lines
    y12_w1, y22_w1 = [CORNER_POINT_A[1] + 52, CORNER_POINT_A[1] + 52]
    plt.plot([0 - 8, 0], [y12_w1, y22_w1], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w1, y22_w1], 'black', linewidth=3)

    # Plot lines to draw the lower wicket
    # verticle lines
    y11_w2, y21_w2 = [CORNER_POINT_C[1] + 1, CORNER_POINT_C[1] + 50]
    plt.plot([0, 0], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w2, y21_w2], 'black', linewidth=3)
    # Horizontal Lines
    y12_w2, y22_w2 = [CORNER_POINT_C[1] + 52, CORNER_POINT_C[1] + 52]
    plt.plot([0 - 8, 0], [y12_w2, y22_w2], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w2, y22_w2], 'black', linewidth=3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Draw the pitch and fill the color bw it
    polygon = plt.Polygon([(CORNER_POINT_A[0], CORNER_POINT_A[1]), (CORNER_POINT_B[0], CORNER_POINT_B[1]),
                           (CORNER_POINT_C[0], CORNER_POINT_C[1]), (CORNER_POINT_D[0], CORNER_POINT_D[1])],
                          facecolor=(138 / 255, 133 / 255, 109 / 255), edgecolor='red')
    ax.add_patch(polygon)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # fill the area between the two vertical lines
    plt.fill_betweenx([CORNER_POINT_A[1], CORNER_POINT_C[1]], 0 - 11, 0 + 11, color='lightblue', alpha=0.3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # colors for each points
    colors = ['green', 'black', "red", "blue"]

    # Filter out missing points and colors
    filtered_points = [(xi, yi, color) for xi, yi, color in zip(x, y, colors) if xi is not None and yi is not None]
    x, y, colors = zip(*filtered_points)

    # plot the points
    ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # lines in the pitch (region to check for the ball)

    # pixel/meter
    factor = 18.17
    # stups point
    stumpA = CORNER_POINT_A[1] + (1.22 * factor)
    stumpB = CORNER_POINT_B[1] + (1.22 * factor)
    # define the y values for every line
    y_values_A = [
        (CORNER_POINT_A[1]),
        stumpA - (2 * factor),
        stumpA - (4 * factor),
        stumpA - (6 * factor),
        stumpA - (7 * factor),
        stumpA - (8 * factor)
    ]

    y_values_B = [
        (CORNER_POINT_B[1]),
        stumpB - (2 * factor),
        stumpB - (4 * factor),
        stumpB - (6 * factor),
        stumpB - (7 * factor),
        stumpB - (8 * factor)
    ]

    # Plot lines for the checking of ball
    plt.plot([CORNER_POINT_A[0], CORNER_POINT_B[0] + 150], [y_values_A[1], y_values_B[1]], 'r-', linewidth=0.5,
             color='black')
    plt.text(CORNER_POINT_B[0] + 81, y_values_A[1] + 3, 'YORKER LENGTH (0-2m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 2, CORNER_POINT_B[0] + 150], [y_values_A[2], y_values_B[2]], linestyle='dotted',
             linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[2] + 15, 'FULL LENGTH (2-4m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 5, CORNER_POINT_B[0] + 150], [y_values_A[3], y_values_B[3]], linewidth=0.5,
             color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[3] + 15, 'FULL LENGTH (4-6m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 6, CORNER_POINT_B[0] + 150], [y_values_A[4], y_values_B[4]], linestyle='dotted',
             linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 80, y_values_A[4] + 5, 'GOOD LENGTH (6-7m)', ha='center', fontsize=6)

    plt.plot([CORNER_POINT_A[0] - 8, CORNER_POINT_B[0] + 150], [y_values_A[5], y_values_B[5]], linewidth=0.5,
             color='black')
    plt.text(CORNER_POINT_B[0] + 85, y_values_A[5] + 5, 'BACK OF LENGTH (7-8m)', ha='center', fontsize=6)

    plt.text(CORNER_POINT_B[0] + 85, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, 'SHORT LENGTH (>8m)',
             ha='center', fontsize=6)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the height and width scaling factors
    height_scale = 191
    extra_height = 20
    total_height = height_scale + extra_height
    width_scale = 141

    # Draw the head
    head = plt.Circle((0, height_scale - (0.15 * width_scale)), 0.15 * width_scale, color='black')
    ax.add_artist(head)

    # # Draw the body
    # body = plt.Line2D([0, 0], [height_scale*0.9, height_scale*0.2], color='black' ,linewidth=3)
    # ax.add_artist(body)

    # Draw the body
    plt.plot([0, 0], [height_scale * 0.9, height_scale * 0.2], color='black', linewidth=3)

    # # Draw the ARMS
    # left_arm = plt.Line2D([0, -0.2*width_scale], [height_scale*0.6, height_scale*0.4], color='black')
    # ax.add_artist(left_arm)
    # right_arm = plt.Line2D([0, 0.2*width_scale], [height_scale*0.6, height_scale*0.4], color='black')
    # ax.add_artist(right_arm)

    # Draw the ARMS
    # Right Arm
    plt.plot([0, -0.2 * width_scale], [height_scale * 0.6, height_scale * 0.4], color='black')
    # Left Arm
    plt.plot([0, 0.2 * width_scale], [height_scale * 0.6, height_scale * 0.4], color='black')

    # Draw the hands
    left_hand = plt.Circle((-0.2 * width_scale, height_scale * 0.4), 2, color='black')
    ax.add_artist(left_hand)
    right_hand = plt.Circle((0.2 * width_scale, height_scale * 0.4), 2, color='black')
    ax.add_artist(right_hand)

    # # Draw the LEGS
    # left_leg = plt.Line2D([0, -0.2*width_scale], [height_scale*0.2, 0], color='black')
    # ax.add_artist(left_leg)
    # right_leg = plt.Line2D([0, 0.2*width_scale], [height_scale*0.2, 0], color='black')
    # ax.add_artist(right_leg)

    # Draw the  LEGS
    # Right leg
    plt.plot([0, -0.2 * width_scale], [height_scale * 0.2, 0], color='black')
    # Left Leg
    plt.plot([0, 0.2 * width_scale], [height_scale * 0.2, 0], color='black')

    # Draw the foots
    left_hand = plt.Circle((-0.2 * width_scale, 0.2), 2, color='black')
    ax.add_artist(left_hand)
    right_hand = plt.Circle((0.2 * width_scale, 0.2), 2, color='black')
    ax.add_artist(right_hand)

    # Set the x-axis and y-axis limits
    # plt.xlim(-width_scale, width_scale)
    plt.ylim(CORNER_POINT_C[1], total_height)
    # plt.axis('off')

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if x_bounce is not None and y_bounce is not None and x_impact is not None and y_impact is not None:
        # Plot an arrow between the release point and bounce point
        plt.annotate('', xy=(x_bounce, y_bounce), xytext=(X, Y), arrowprops=dict(arrowstyle='->', color='black'))

        # Plot an arrow between the bounce point and impact point
        plt.annotate('', xy=(x_impact, y_impact), xytext=(x_bounce, y_bounce),
                     arrowprops=dict(arrowstyle='->', color='black'))

        if x_trajectory is not None and y_trajectory is not None:
            # Plot an arrow between the imact point and after imact point
            plt.annotate('', xy=(x_trajectory, y_trajectory), xytext=(x_impact, y_impact),
                         arrowprops=dict(arrowstyle='->', color='black'))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of all Points')

    # return the plot
    return plt


def bounce_statistics(detectionss):
    # creating the figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # pixel to meter
    factor = 18.17
    # Define the coordinates of the points to plot (also check whether it is None or Not)
    x = [estimate_bounce_point(detection)[0] for detection in detectionss if
         estimate_bounce_point(detection)[0] is not None]
    y = [estimate_bounce_point(detection)[1] for detection in detectionss if
         estimate_bounce_point(detection)[1] is not None]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # define the y values for every line
    y_values_A = [
        (CORNER_POINT_A[1]),
        (CORNER_POINT_A[1] + (1.22 * factor)) - (2 * factor),
        (CORNER_POINT_A[1] + (1.22 * factor)) - (4 * factor),
        (CORNER_POINT_A[1] + (1.22 * factor)) - (6 * factor),
        (CORNER_POINT_A[1] + (1.22 * factor)) - (7 * factor),
        (CORNER_POINT_A[1] + (1.22 * factor)) - (8 * factor)
    ]

    y_values_B = [
        (CORNER_POINT_B[1]),
        (CORNER_POINT_B[1] + (1.22 * factor)) - (2 * factor),
        (CORNER_POINT_B[1] + (1.22 * factor)) - (4 * factor),
        (CORNER_POINT_B[1] + (1.22 * factor)) - (6 * factor),
        (CORNER_POINT_B[1] + (1.22 * factor)) - (7 * factor),
        (CORNER_POINT_B[1] + (1.22 * factor)) - (8 * factor)
    ]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Initialize a variables to store  counts
    first = second = third = fourth = fifth = sixth = 0

    # check percentage for each region
    for p in y:
        if y_values_A[0] > p and p > y_values_A[1]:
            first += 1
        elif y_values_A[1] > p and p > y_values_A[2]:
            second += 1
        elif y_values_A[2] > p and p > y_values_A[3]:
            third += 1
        elif y_values_A[3] > p and p > y_values_A[4]:
            fourth += 1
        elif y_values_A[4] > p and p > y_values_A[5]:
            fifth += 1
        else:
            sixth += 1

    # calculate the all percentages
    count = len(y)
    percentages = [int((x / count) * 100) for x in [first, second, third, fourth, fifth, sixth]]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot lines to draw the uppper wicket
    # verticle lines
    y11_w1, y21_w1 = [CORNER_POINT_A[1] + 1, CORNER_POINT_A[1] + 50]
    plt.plot([0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w1, y21_w1], 'black', linewidth=3)
    # Horizontal Lines
    y12_w1, y22_w1 = [CORNER_POINT_A[1] + 52, CORNER_POINT_A[1] + 52]
    plt.plot([0 - 8, 0], [y12_w1, y22_w1], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w1, y22_w1], 'black', linewidth=3)

    # Plot lines to draw the lower wicket
    # verticle lines
    y11_w2, y21_w2 = [CORNER_POINT_C[1] + 1, CORNER_POINT_C[1] + 50]
    plt.plot([0, 0], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w2, y21_w2], 'black', linewidth=3)
    # Horizontal Lines
    y12_w2, y22_w2 = [CORNER_POINT_C[1] + 52, CORNER_POINT_C[1] + 52]
    plt.plot([0 - 8, 0], [y12_w2, y22_w2], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w2, y22_w2], 'black', linewidth=3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Draw the pitch and fill the color bw it
    polygon = plt.Polygon([(CORNER_POINT_A[0], CORNER_POINT_A[1]), (CORNER_POINT_B[0], CORNER_POINT_B[1]),
                           (CORNER_POINT_C[0], CORNER_POINT_C[1]), (CORNER_POINT_D[0], CORNER_POINT_D[1])],
                          facecolor=(138 / 255, 133 / 255, 109 / 255), edgecolor='red')
    ax.add_patch(polygon)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # # plot lines wicket to wicket
    # plt.plot([0-11,0-11], [CORNER_POINT_A[1], CORNER_POINT_C[1]], 'black', linewidth=0)
    # plt.plot([0+11,0+11], [CORNER_POINT_A[1], CORNER_POINT_C[1]], 'black', linewidth=0)

    # fill the area between the two vertical lines
    plt.fill_betweenx([CORNER_POINT_A[1], CORNER_POINT_C[1]], 0 - 11, 0 + 11, color='lightblue', alpha=0.3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Generate random colors for each point
    num_points = len(x)
    colors = np.random.rand(num_points, 3)

    # Plot the points
    scatter = ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot lines for the checking of ball
    line_x_min, line_x_max = CORNER_POINT_A[0] - 80, CORNER_POINT_B[0] + 150
    left_text_x = CORNER_POINT_A[0] - 40
    plt.plot([line_x_min, line_x_max], [y_values_A[1], y_values_B[1]], 'r-', linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 81, y_values_A[1] + 3, 'YORKER LENGTH (0-2m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[1] + 3, f'{percentages[0]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[2], y_values_B[2]], linestyle='dotted', linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[2] + 15, 'FULL LENGTH (2-4m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[2] + 15, f'{percentages[1]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[3], y_values_B[3]], linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[3] + 15, 'FULL LENGTH (4-6m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[3] + 15, f'{percentages[2]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[4], y_values_B[4]], linestyle='dotted', linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 80, y_values_A[4] + 5, 'GOOD LENGTH (6-7m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[4] + 5, f'{percentages[3]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[5], y_values_B[5]], linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 85, y_values_A[5] + 5, 'BACK OF LENGTH (7-8m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[5] + 5, f'{percentages[4]}%', ha='center', fontsize=6)

    plt.text(CORNER_POINT_B[0] + 85, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, 'SHORT LENGTH (>8m)',
             ha='center', fontsize=6)
    plt.text(left_text_x, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, f'{percentages[5]}%', ha='center',
             fontsize=6)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of all Stats')

    # return the plot
    return plt


def impact_statistics(detectionss):
    # creating the figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the coordinates of the points to plot
    x = [estimate_impact_point(detection)[0] for detection in detectionss if
         estimate_impact_point(detection)[0] is not None]
    y = [estimate_impact_point(detection)[1] for detection in detectionss if
         estimate_impact_point(detection)[1] is not None]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the height and width scaling factors
    height_scale = 191
    extra_height = 20
    total_height = height_scale + extra_height
    width_scale = 141

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # colors for each point

    colors = "red"

    # Plot the impact points
    scatter = ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set the x-axis and y-axis limits
    plt.xlim(-width_scale, width_scale)
    plt.ylim(0, total_height)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Impact Point')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Load and display the image
    image_path = 'a.jpg'
    image = plt.imread(image_path)
    ax.imshow(image, extent=[width_scale, -width_scale, -10, total_height])

    # if estimate_btasman_side(detectionss[0]) == "RIGHT HANDED BATSMAN":
    #     ax.imshow(image, extent=[width_scale, -width_scale, -10, total_height])
    # else:
    #     ax.imshow(image, extent=[-width_scale, width_scale, -10, total_height])

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return plt


def trajectory_statistics(detectionss):
    # creating the figure
    fig, ax = plt.subplots()

    # Define the coordinates of the points to plot
    x_impact = [estimate_impact_point(detection)[0] for detection in detectionss]
    y_impact = [estimate_impact_point(detection)[1] for detection in detectionss]

    # Define the coordinates of the points to plot
    x_trajectory = [estimate_trajectory(detection)[0] for detection in detectionss]
    y_trajectory = [estimate_trajectory(detection)[1] for detection in detectionss]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    xx = [0]
    yy = [0]

    # To converrt the points to unit vector
    for i in range(len(x_trajectory)):
        # if the Trajectory Point is known
        if x_trajectory[i] is not None and y_trajectory[i] is not None:
            (x_new_trajectory, y_new_trajectory) = (x_trajectory[i] - x_impact[i], y_trajectory[i] - y_impact[i])

            # Now the impact point will be (0,0)
            x = [0, x_new_trajectory]
            y = [0, y_new_trajectory]

            # Calculate the vector
            vector = (x[1] - x[0], y[1] - y[0])

            # Calculate the magnitude of the vector
            magnitude = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
                # Calculate the unit vector
            try:
                unit_vector = (vector[0] / magnitude, vector[1] / magnitude)

                # New point will be origin and unit vector
                xx.append(unit_vector[0])
                yy.append(unit_vector[1])
            except:
                pass

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add an ellipse(for ground)
    ellipse = Ellipse(xy=(0, 0), width=4, height=5.5, edgecolor='blue', facecolor='green')
    ax.add_patch(ellipse)

    # # Add a colored square at the midpoint(for pitch)
    # square = Rectangle((-0.125, -0.7), 0.25, 1, facecolor=(0.3, 0.29, 0))
    # ax.add_patch(square)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Colors for each point
    colors = ['white'] + ['blue'] * (len(xx) - 1)

    # Plot the points
    ax.scatter(xx, yy, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot an arrow between the impact point to every (after impact points)
    for i in range(1, len(xx)):
        plt.annotate('', xy=(xx[i], yy[i]), xytext=(x[0], y[0]), arrowprops=dict(arrowstyle='->', color='yellow'))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # # Add text on the left and right side of the impact point
    # plt.text(0 - 1.5, 0, 'LEG SIDE', fontsize=12)
    # plt.text(0 + 0.7, 0, 'OFF SIDE', fontsize=12)

    #  # Add text on the left and right side of the impact point
    # if estimate_btasman_side(detections) == "RIGHT HANDED BTSMAN":
    #     plt.text(0 - 1.5, 0, 'OFF SIDE ', fontsize=12)
    #     plt.text(0 + 0.7, 0, 'LEG SIDE', fontsize=12)
    # else:
    #     plt.text(0 - 1.5, 0, 'LEG SIDE', fontsize=12)
    #     plt.text(0 + 0.7, 0, 'OFF SIDE', fontsize=12)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set the x-axis and y-axis limits
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Trajectories')

    # Display the plot
    return plt

def all_stats_2D(detectionss):
    # creating the figure
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # finding the bowling side
    bowling_side = estimate_bowling_side(detectionss[0])

    # Release Point
    (X, Y, Z) = estimate_release_point(bowling_side)

    # Bounce Point
    # Define the coordinates of the bounce points of all the vedios to plot
    x_bounce = [estimate_bounce_point(detection)[0] for detection in detectionss if
                estimate_bounce_point(detection)[0] is not None]
    y_bounce = [estimate_bounce_point(detection)[1] for detection in detectionss if
                estimate_bounce_point(detection)[1] is not None]

    # Impact Point
    # Define the coordinates of the impact points of all the vedios to plot
    x_impact = [estimate_impact_point(detection)[0] for detection in detectionss if
                estimate_impact_point(detection)[0] is not None]
    y_impact = [estimate_impact_point(detection)[1] for detection in detectionss if
                estimate_impact_point(detection)[1] is not None]

    # Trajectory Point
    # Define the coordinates of the impact points of all the vedios to plot
    x_trajectory = [estimate_trajectory(detection)[0] for detection in detectionss if
                    estimate_trajectory(detection)[0] is not None]
    y_trajectory = [estimate_trajectory(detection)[1] for detection in detectionss if
                    estimate_trajectory(detection)[1] is not None]

    # Points to be plot
    x = []
    y = []
    x.append(X)
    x.extend(x_bounce)
    x.extend(x_impact)
    x.extend(x_trajectory)
    y.append(Y)
    y.extend(y_bounce)
    y.extend(y_impact)
    y.extend(y_trajectory)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot lines to draw the uppper wicket
    # verticle lines
    y11_w1, y21_w1 = [CORNER_POINT_A[1] + 1, CORNER_POINT_A[1] + 50]
    plt.plot([0, 0], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w1, y21_w1], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w1, y21_w1], 'black', linewidth=3)
    # Horizontal Lines
    y12_w1, y22_w1 = [CORNER_POINT_A[1] + 52, CORNER_POINT_A[1] + 52]
    plt.plot([0 - 8, 0], [y12_w1, y22_w1], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w1, y22_w1], 'black', linewidth=3)

    # Plot lines to draw the lower wicket
    # verticle lines
    y11_w2, y21_w2 = [CORNER_POINT_C[1] + 1, CORNER_POINT_C[1] + 50]
    plt.plot([0, 0], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 - 10, 0 - 10], [y11_w2, y21_w2], 'black', linewidth=3)
    plt.plot([0 + 10, 0 + 10], [y11_w2, y21_w2], 'black', linewidth=3)
    # Horizontal Lines
    y12_w2, y22_w2 = [CORNER_POINT_C[1] + 52, CORNER_POINT_C[1] + 52]
    plt.plot([0 - 8, 0], [y12_w2, y22_w2], 'black', linewidth=3)
    plt.plot([0, 0 + 8], [y12_w2, y22_w2], 'black', linewidth=3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Draw the pitch and fill the color bw it
    polygon = plt.Polygon([(CORNER_POINT_A[0], CORNER_POINT_A[1]), (CORNER_POINT_B[0], CORNER_POINT_B[1]),
                           (CORNER_POINT_C[0], CORNER_POINT_C[1]), (CORNER_POINT_D[0], CORNER_POINT_D[1])],
                          facecolor=(138 / 255, 133 / 255, 109 / 255), edgecolor='red')
    ax.add_patch(polygon)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # # plot lines wicket to wicket
    # plt.plot([0-11,0-11], [CORNER_POINT_A[1], CORNER_POINT_C[1]], 'black', linewidth=0)
    # plt.plot([0+11,0+11], [CORNER_POINT_A[1], CORNER_POINT_C[1]], 'black', linewidth=0)

    # fill the area between the two vertical lines
    plt.fill_betweenx([CORNER_POINT_A[1], CORNER_POINT_C[1]], 0 - 11, 0 + 11, color='lightblue', alpha=0.3)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Colors for each point
    colors = ['green'] + (['black'] * (len(x_bounce))) + (['red'] * (len(x_impact))) + (['blue'] * (len(x_trajectory)))

    # Plot the points
    ax.scatter(x, y, c=colors)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # pixel/meter
    factor = 18.17
    # stups point
    stumpA = CORNER_POINT_A[1] + (1.22 * factor)
    stumpB = CORNER_POINT_B[1] + (1.22 * factor)
    # define the y values for every line
    y_values_A = [
        (CORNER_POINT_A[1]),
        stumpA - (2 * factor),
        stumpA - (4 * factor),
        stumpA - (6 * factor),
        stumpA - (7 * factor),
        stumpA - (8 * factor)
    ]

    y_values_B = [
        (CORNER_POINT_B[1]),
        stumpB - (2 * factor),
        stumpB - (4 * factor),
        stumpB - (6 * factor),
        stumpB - (7 * factor),
        stumpB - (8 * factor)
    ]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Initialize a variables to store  counts
    first = second = third = fourth = fifth = sixth = 0

    # check percentage
    for p in y_bounce:
        if y_values_A[0] > p and p > y_values_A[1]:
            first += 1
        elif y_values_A[1] > p and p > y_values_A[2]:
            second += 1
        elif y_values_A[2] > p and p > y_values_A[3]:
            third += 1
        elif y_values_A[3] > p and p > y_values_A[4]:
            fourth += 1
        elif y_values_A[4] > p and p > y_values_A[5]:
            fifth += 1
        else:
            sixth += 1

    # calculate the all percentages
    count = len(x_bounce)
    percentages = [int((x / count) * 100) for x in [first, second, third, fourth, fifth, sixth]]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Plot lines for the checking of ball
    line_x_min, line_x_max = CORNER_POINT_A[0] - 80, CORNER_POINT_B[0] + 150
    left_text_x = CORNER_POINT_A[0] - 40
    plt.plot([line_x_min, line_x_max], [y_values_A[1], y_values_B[1]], 'r-', linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 81, y_values_A[1] + 3, 'YORKER LENGTH (0-2m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[1] + 3, f'{percentages[0]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[2], y_values_B[2]], linestyle='dotted', linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[2] + 15, 'FULL LENGTH (2-4m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[2] + 15, f'{percentages[1]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[3], y_values_B[3]], linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 77, y_values_A[3] + 15, 'FULL LENGTH (4-6m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[3] + 15, f'{percentages[2]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[4], y_values_B[4]], linestyle='dotted', linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 80, y_values_A[4] + 5, 'GOOD LENGTH (6-7m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[4] + 5, f'{percentages[3]}%', ha='center', fontsize=6)

    plt.plot([line_x_min, line_x_max], [y_values_A[5], y_values_B[5]], linewidth=0.5, color='black')
    plt.text(CORNER_POINT_B[0] + 85, y_values_A[5] + 5, 'BACK OF LENGTH (7-8m)', ha='center', fontsize=6)
    plt.text(left_text_x, y_values_A[5] + 5, f'{percentages[4]}%', ha='center', fontsize=6)

    plt.text(CORNER_POINT_B[0] + 85, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, 'SHORT LENGTH (>8m)',
             ha='center', fontsize=6)
    plt.text(left_text_x, (CORNER_POINT_A[1] + (1.22 * factor)) - (12 * factor) + 5, f'{percentages[5]}%', ha='center',
             fontsize=6)

    # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the height and width scaling factors
    height_scale = 191
    extra_height = 20
    total_height = height_scale + extra_height
    width_scale = 141

    # Draw the head
    head = plt.Circle((0, height_scale - (0.15 * width_scale)), 0.15 * width_scale, color='black')
    ax.add_artist(head)

    # # Draw the body
    # body = plt.Line2D([0, 0], [height_scale*0.9, height_scale*0.2], color='black' ,linewidth=3)
    # ax.add_artist(body)

    # Draw the body
    plt.plot([0, 0], [height_scale * 0.9, height_scale * 0.2], color='black', linewidth=3)

    # # Draw the ARMS
    # left_arm = plt.Line2D([0, -0.2*width_scale], [height_scale*0.6, height_scale*0.4], color='black')
    # ax.add_artist(left_arm)
    # right_arm = plt.Line2D([0, 0.2*width_scale], [height_scale*0.6, height_scale*0.4], color='black')
    # ax.add_artist(right_arm)

    # Draw the ARMS
    # Right Arm
    plt.plot([0, -0.2 * width_scale], [height_scale * 0.6, height_scale * 0.4], color='black')
    # Left Arm
    plt.plot([0, 0.2 * width_scale], [height_scale * 0.6, height_scale * 0.4], color='black')

    # Draw the hands
    left_hand = plt.Circle((-0.2 * width_scale, height_scale * 0.4), 2, color='black')
    ax.add_artist(left_hand)
    right_hand = plt.Circle((0.2 * width_scale, height_scale * 0.4), 2, color='black')
    ax.add_artist(right_hand)

    # # Draw the LEGS
    # left_leg = plt.Line2D([0, -0.2*width_scale], [height_scale*0.2, 0], color='black')
    # ax.add_artist(left_leg)
    # right_leg = plt.Line2D([0, 0.2*width_scale], [height_scale*0.2, 0], color='black')
    # ax.add_artist(right_leg)

    # Draw the  LEGS
    # Right leg
    plt.plot([0, -0.2 * width_scale], [height_scale * 0.2, 0], color='black')
    # Left Leg
    plt.plot([0, 0.2 * width_scale], [height_scale * 0.2, 0], color='black')

    # Draw the foots
    left_hand = plt.Circle((-0.2 * width_scale, 0.2), 2, color='black')
    ax.add_artist(left_hand)
    right_hand = plt.Circle((0.2 * width_scale, 0.2), 2, color='black')
    ax.add_artist(right_hand)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Define the coordinates of the bounce points of all the vedios to plot
    x_bounce = [estimate_bounce_point(detection)[0] for detection in detectionss]
    y_bounce = [estimate_bounce_point(detection)[1] for detection in detectionss]

    # Impact Point
    # Define the coordinates of the impact points of all the vedios to plot
    x_impact = [estimate_impact_point(detection)[0] for detection in detectionss]
    y_impact = [estimate_impact_point(detection)[1] for detection in detectionss]

    # Trajectory Point
    # Define the coordinates of the impact points of all the vedios to plot
    x_trajectory = [estimate_trajectory(detection)[0] for detection in detectionss]
    y_trajectory = [estimate_trajectory(detection)[1] for detection in detectionss]

    for i in range(len(detectionss)):

        if x_bounce[i] is not None and y_bounce[i] is not None and x_impact[i] is not None and y_impact[i] is not None:
            # Plot an arrow between the release point and bounce point
            plt.annotate('', xy=(x_bounce[i], y_bounce[i]), xytext=(X, Y),
                         arrowprops=dict(arrowstyle='->', color='black'))

            # Plot an arrow between the bounce point and impact point
            plt.annotate('', xy=(x_impact[i], y_impact[i]), xytext=(x_bounce[i], y_bounce[i]),
                         arrowprops=dict(arrowstyle='->', color='black'))

            if x_trajectory[i] is not None and y_trajectory[i] is not None:
                # Plot an arrow between the imact point and after imact point
                plt.annotate('', xy=(x_trajectory[i], y_trajectory[i]), xytext=(x_impact[i], y_impact[i]),
                             arrowprops=dict(arrowstyle='->', color='black'))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set the x-axis and y-axis limits
    # plt.xlim(-width_scale, width_scale)
    plt.ylim(CORNER_POINT_C[1], total_height)
    # plt.axis('off')

    # Add axis labels and a title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Batch Pocessing of All Points')

    # # return the plot
    return plt





