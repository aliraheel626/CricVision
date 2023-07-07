# %matplotlib notebook
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.interpolate import interp1d
import pandas as pd


from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D


from library import open_video,detect,estimate_bowling_side,estimate_release_point,estimate_bounce_point,estimate_impact_point,estimate_trajectory

# to read detections from the csv files
# detections=pd.read_csv(f'detections/7.2.23/{4}.csv')
# vid = open_video("4.mp4")
# detections = detect(vid)


BATSMAN_HEIGHT=191
CORNER_POINT_A=(-140,0,0)
CORNER_POINT_B=(140,0,0)
CORNER_POINT_C=(166, -321,0)
CORNER_POINT_D=(-166, -321,0)


def animation3D(detections, gif_file):
    bowling_side=estimate_bowling_side(detections)

    (x_release_point,y_release_point,z_relaese_point) = estimate_release_point(bowling_side)

    (x_bounce,y_bounce) = estimate_bounce_point(detections)
    (x_bounce,y_bounce,z_bounce) = (x_bounce,y_bounce,0)

    (x_impact,y_impact) = estimate_impact_point(detections)
    (x_impact,y_impact,z_impact) = (x_impact,0,y_impact)

    (x_trajectory,y_trajectory) = estimate_trajectory(detections)
    (x_trajectory,y_trajectory,z_trajectory) = (x_trajectory,0,y_trajectory)


    x = [x_release_point, x_bounce, x_impact, x_trajectory]
    y = [y_release_point, y_bounce, y_impact, y_trajectory]
    z = [z_relaese_point, z_bounce, z_impact, z_trajectory]


    # Interpolating to generate 100 intermediate points between the four points
    num_points = 50
    x_interp = interp1d(np.arange(len(x)), x, kind='linear')
    y_interp = interp1d(np.arange(len(y)), y, kind='linear')
    z_interp = interp1d(np.arange(len(z)), z, kind='linear')
    t_interp = np.linspace(0, len(x)-1, num_points)

    x_new = x_interp(t_interp)
    y_new = y_interp(t_interp)
    z_new = z_interp(t_interp)

    # Setting up Data Set for Animation
    dataSet = np.array([x_new, y_new, z_new])
    numDataPoints = len(t_interp)


    def animate_func(num):
            ax.clear()  # Clears the figure to update the line, point,# title, and axes

            # Updating Trajectory Line (num+1)
            ax.plot3D(dataSet[0, :num+1], dataSet[1, :num+1],dataSet[2, :num+1], c='black', linestyle='dotted')
            
            # Updating Point Location
            if num >= 0 and num <= 16: 
                ax.scatter(dataSet[0, num], dataSet[1, num], dataSet[2, num],c='blue', marker='o')
            elif num >= 16 and num <= 33: 
                ax.scatter(dataSet[0, num], dataSet[1, num], dataSet[2, num],c='black', marker='o')
            else:
                 ax.scatter(dataSet[0, num], dataSet[1, num], dataSet[2, num],c='red', marker='o')

            # -----------------------------------------------------------------------------------



            # Release Point
            ax.plot3D(x_release_point, y_release_point, z_relaese_point,c='blue', marker='o')
            
            # Bounce Point
            ax.plot3D(x_bounce, y_bounce, z_bounce,c='black', marker='o')
            
            # Impact Point
            ax.plot3D(x_impact, y_impact, z_impact,c='red', marker='o')
            
            # After Impact Point
            ax.plot3D(x_trajectory, y_trajectory, z_trajectory,c='green', marker='o')

    

            # -----------------------------------------------------------------------------------
    
            # Draw rectangle
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
            ax.plot([x[0], x[1]], [y[0], y[1]], [z[0], z[1]], 'r')
            ax.plot([x[1], x[2]], [y[1], y[2]], [z[1], z[2]], 'r')
            ax.plot([x[2], x[3]], [y[2], y[3]], [z[2], z[3]], 'r')
            ax.plot([x[3], x[0]], [y[3], y[0]], [z[3], z[0]], 'r')

            # To fill the piching line
            polygon = [corner_points]
            poly = Poly3DCollection(polygon, alpha=0.5)
            poly.set_color((128/255,128/255,128/255))
            ax.add_collection3d(poly)

            

            # -----------------------------------------------------------------------------------

            
            # To fill the piching line
            pitching_line = [
                (-11,0,0),
                (11,0,0),
                (11,-321,0),
                (-11,-321,0)
            ]
        
            polygon = [pitching_line]
            poly = Poly3DCollection(polygon, alpha=0.5)
            poly.set_color((65/255,105/255,225/255))
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
            plt.plot([CORNER_POINT_A[0], CORNER_POINT_B[0]+150], [y_values_A[1], y_values_B[1]], 'r-' , linewidth=1.5 , color='black')
            ax.text(CORNER_POINT_B[0]+81, y_values_A[1]+3, 0, 'YORKER LENGTH (0-2m)', color='black', fontsize=6 )

            plt.plot([CORNER_POINT_A[0]-2, CORNER_POINT_B[0]+150], [y_values_A[2], y_values_B[2]], linestyle='dotted', linewidth=1.5, color='black')
            ax.text(CORNER_POINT_B[0]+77, y_values_A[2] + 15, 0, 'FULL LENGTH (2-4m)', color='black', fontsize=6 )

            plt.plot([CORNER_POINT_A[0]-5, CORNER_POINT_B[0]+150], [y_values_A[3], y_values_B[3]], linewidth=1.5 , color='black')
            ax.text(CORNER_POINT_B[0]+77, y_values_A[3] + 15, 0, 'FULL LENGTH (4-6m)', color='black', fontsize=6 )

            plt.plot([CORNER_POINT_A[0]-6, CORNER_POINT_B[0]+150], [y_values_A[4], y_values_B[4]], linestyle='dotted', linewidth=1.5, color='black')
            ax.text(CORNER_POINT_B[0]+80, y_values_A[4] + 5, 0, 'GOOD LENGTH (6-7m)', color='black', fontsize=6 )

            plt.plot([CORNER_POINT_A[0]-8, CORNER_POINT_B[0]+150], [y_values_A[5], y_values_B[5]], linewidth=1.5 , color='black')
            ax.text(CORNER_POINT_B[0]+85, y_values_A[5] + 5,0, 'BACK OF LENGTH (7-8m)', color='black', fontsize=6 )

            ax.text(CORNER_POINT_B[0]+85, (CORNER_POINT_A[1]+(1.22*factor))-(12*factor) + 5,0, 'SHORT LENGTH (>8m)', color='black', fontsize=6 )

            # -----------------------------------------------------------------------------------

            # Define the height and width scaling factors
            height_scale = 191
            extra_height = 20  
            total_height = height_scale + extra_height
            width_scale = 141

            # Draw the head
            # Set the position and size of the circle
            center = (0, 0, height_scale-(0.15*width_scale))
            radius = 0.15*width_scale
            # Create a 3D circle
            # Create a 3D circle
            theta = np.linspace(0, 2 * np.pi, 100)
            x = center[0] + radius * np.cos(theta)
            y = np.full_like(theta, center[1]) 
            z = center[2] + radius * np.sin(theta)
            # Plot the circle in 3D
            ax.plot(x, y, z, color='black')


        # Draw the body
            ax.plot([0, 0],[0,0], [height_scale-(0.3*width_scale), height_scale*0.2], linewidth=1.5 , color='black')

            # Draw the ARMS
            # Right Arm
            ax.plot([0, 20],[0,0], [150, 100],  linewidth=1.5 , color='black')
            # Left Arm
            ax.plot([0, -20],[0,0], [150, 100], linewidth=1.5 , color='black')


            # Draw the  legs
            # Right leg
            ax.plot([0, 20],[0,0], [50, 0], linewidth=1.5 , color='black')
            # Left Leg
            ax.plot([0, -20],[0,0], [50, 0], linewidth=1.5 , color='black')

            #  Setting Axes Limits
            ax.set_xlim3d(-166-10, 166+10)
            ax.set_ylim3d(-321-10, 0)
            ax.set_zlim3d(0,200)

            
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

            ax.set_box_aspect([2.5, 4.5, 1])

    # P# Plotting the Animation
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    line_ani = animation.FuncAnimation(fig, animate_func, interval=100,
                                    frames=numDataPoints)
    # anim = plt.show()
    # plt.savefig("ani.svg")
    # line_ani.save("animation.fig")
    # return anim
    # plt.show()
    # Save the animation as a GIF file
    line_ani.save(gif_file, writer='pillow')


# matplotlib.use('TkAgg')
# iii(detections)
# ani.show()



