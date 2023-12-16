
'''

Author: Idris Seidu

'''

import matplotlib.pyplot as plt
import numpy as np

# Import the QPcontroller class from the CLF_CBF_QP_Controller file
from CLF_CBF_QP_Controller import QPcontroller


def create_chessboard(ax):
    board_size = (12, 8)  # 12 rows, 8 columns
    square_size = 2.4
    text_color = '#4169E1'  # Light color for the text
    font_size = 8  # Adjust font size as needed
    column_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    row_labels = ['1', '2', '3', '4', '5', '6', '7', '8']

    # Iterate over the rows and columns to draw the squares and add text labels
    for x in range(board_size[0]):
        for y in range(board_size[1]):
            color = 'white' if (x + y) % 2 == 0 else 'grey'
            if x < 2 or x >= 10:  # Extra space for captured pieces
                color = 'lightgrey'
            rect = plt.Rectangle([y * square_size, x * square_size], square_size, square_size, color=color)
            ax.add_patch(rect)

            # Add text label for the square number, starting from bottom right
            if x >= 2 and x < 10:  # Add labels only for the main 8x8 board
                square_number = (11 - x) * 8 + y
                ax.text(y * square_size + square_size / 2, x * square_size + square_size / 2, str(square_number),
                        horizontalalignment='center', verticalalignment='center', 
                        color=text_color, fontsize=font_size)

    # Add column labels (A, B, C, etc.) below the board
    for i, label in enumerate(column_labels):
        ax.text(i * square_size + square_size / 2, -square_size / 2, label, 
                horizontalalignment='center', verticalalignment='center', 
                color=text_color, fontsize=font_size)
    row_label_color = '#FF0000'  # Example: Red color for row labels
    row_label_font_size = 10
    # Add row labels (1, 2, 3, etc.) to the right of the board
    for i, label in enumerate(row_labels):
    # The y position is shifted by 2 squares up from the bottom
        ax.text(board_size[1] * square_size + square_size / 2, (i + 2) * square_size + square_size / 2, label,
                horizontalalignment='center', verticalalignment='center',
                color=row_label_color, fontsize=row_label_font_size)

    ax.set_xlim([0, board_size[1] * square_size + square_size])
    ax.set_ylim([-square_size, board_size[0] * square_size])
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(0, board_size[1] * square_size, square_size))
    ax.set_yticks(np.arange(0, board_size[0] * square_size, square_size))
    ax.grid(which='both')
    ax.axis('on')  # Turn off axis lines and labels if needed



def positions_are_close(pos1, pos2, tol=1e-6):
    """ Check if two positions are close enough considering a tolerance level. """
    return abs(pos1[0] - pos2[0]) < tol and abs(pos1[1] - pos2[1]) < tol

def plot_pieces(ax, obs_info, moving_piece_info=None):
    piece_colors = {
        'King': 'orange',
        'Queen': 'red',
        'Rook': 'blue',
        'Bishop': 'green',
        'Knight': 'goldenrod',
        'Pawn': 'purple'
    }

    # Plot all pieces except the moving piece
    for piece in obs_info:
        if moving_piece_info and positions_are_close(piece['position'], moving_piece_info['position']):
            continue  # Skip the moving piece for now

        color = piece_colors[piece['type']]
        edgecolor = 'black' if piece['player'] == 'Player2' else color
        linewidth = 2 if piece['player'] == 'Player2' else 0
        circle = plt.Circle(piece['position'], piece['radius'], color=color, ec=edgecolor, lw=linewidth, alpha=0.8)
        ax.add_patch(circle)

    # Plot the moving piece if it's defined
    if moving_piece_info:
        color = piece_colors[moving_piece_info['type']]
        edgecolor = 'black' if moving_piece_info['player'] == 'Player2' else color
        linewidth = 2 if moving_piece_info['player'] == 'Player2' else 0
        circle = plt.Circle(moving_piece_info['position'], moving_piece_info['radius'], color=color, ec=edgecolor, lw=linewidth, alpha=0.8)
        ax.add_patch(circle)


"""
This function creates the configuration of chess pieces on the board. 
You can adjust the 'position', 'radius', 'type', and 'player' attributes for each piece as desired.

The 'position' attribute refers to the location of the piece on the chessboard, 
expressed as coordinates derived from 'grid_positions'. 
'grid_positions[16]' to 'grid_positions[79]' represent the squares of the standard 8x8 chessboard.
'grid_positions[0]' to 'grid_positions[15]' are designated for Player 1's captured pieces, 
while 'grid_positions[80]' to 'grid_positions[95]' are for Player 2's captured pieces.

The 'radius' attribute determines the size of the piece's representation on the board.
The 'type' attribute can be any of the standard chess pieces: 'Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', or 'King'.
The 'player' attribute indicates which player the piece belongs to, either 'Player1' or 'Player2'.

Adjust these attributes to set up custom chessboard configurations for simulation or visualization purposes.
"""

def create_specific_pieces(moving_piece_info=None):
    # Calculate the center positions of squares in an 8x8 grid
    grid_positions = [(x * 2.4 + 1.2, y * 2.4 + 1.2) for y in range(11, -1, -1) for x in range(8)]

    # Assign pieces for a game in progress, including some captured pieces
    all_pieces = [
        # Example configuration for active pieces on the board
        #Player 1 pieces
        {'position': grid_positions[20], 'radius': 0.5, 'type': 'Rook', 'player': 'Player1'},  # E8
        {'position': grid_positions[22], 'radius': 0.5, 'type': 'King', 'player': 'Player1'},  # G8
        {'position': grid_positions[25], 'radius': 0.5, 'type': 'Bishop', 'player': 'Player1'},  # B7
        {'position': grid_positions[28], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  # E7
        {'position': grid_positions[29], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  # F7
        {'position': grid_positions[30], 'radius': 0.5, 'type': 'Bishop', 'player': 'Player1'},  # G7
        {'position': grid_positions[31], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  # H7
        {'position': grid_positions[32], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  # A6
        {'position': grid_positions[33], 'radius': 0.5, 'type': 'Queen', 'player': 'Player1'}, # B6 
        {'position': grid_positions[38], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'}, # G6
        {'position': grid_positions[41], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  # B5
        {'position': grid_positions[51], 'radius': 0.5, 'type': 'Rook', 'player': 'Player1'},  # D4
        {'position': grid_positions[54], 'radius': 0.5, 'type': 'Knight', 'player': 'Player1'},  # G4
        #Captured Player 1 pieces
        {'position': grid_positions[80], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  
        {'position': grid_positions[81], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player1'},  
        {'position': grid_positions[82], 'radius': 0.5, 'type': 'Knight', 'player': 'Player1'},  

        # Player 2 pieces
        {'position': grid_positions[56], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  # A3
        {'position': grid_positions[58], 'radius': 0.5, 'type': 'Knight', 'player': 'Player2'},  # C3
        {'position': grid_positions[59], 'radius': 0.5, 'type': 'Bishop', 'player': 'Player2'},  # D3
        {'position': grid_positions[60], 'radius': 0.5, 'type': 'Bishop', 'player': 'Player2'},  # E3
        {'position': grid_positions[65], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  # B2
        {'position': grid_positions[66], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  # C2
        {'position': grid_positions[69], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  # F2
        {'position': grid_positions[70], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  # G2
        {'position': grid_positions[71], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'}, # H2
        {'position': grid_positions[74], 'radius': 0.5, 'type': 'Queen', 'player': 'Player2'},  # C1
        {'position': grid_positions[75], 'radius': 0.5, 'type': 'Rook', 'player': 'Player2'},  # D1
        {'position': grid_positions[76], 'radius': 0.5, 'type': 'Rook', 'player': 'Player2'},  # E1
        {'position': grid_positions[78], 'radius': 0.5, 'type': 'King', 'player': 'Player2'},  # G1
        #captured Player 2 pieces
        {'position': grid_positions[0], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  
        {'position': grid_positions[1], 'radius': 0.5, 'type': 'Pawn', 'player': 'Player2'},  
        {'position': grid_positions[2], 'radius': 0.5, 'type': 'Knight', 'player': 'Player2'},  
       
    ]
    if moving_piece_info:
        pieces = [piece for piece in all_pieces if not positions_are_close(piece['position'], moving_piece_info['position'])]
    else:
        pieces = all_pieces

    return pieces
def move_piece_to_goal(moving_piece, goal_position, obs_info):
    obstructing_piece = None
    new_position = None
    for piece in obs_info:
        if positions_are_close(piece['position'], goal_position):
            player = piece['player']
            captured_area = grid_positions[80:96] if player == 'Player1' else grid_positions[0:16]
            for captured_position in captured_area:
                if not any(positions_are_close(other_piece['position'], captured_position) for other_piece in obs_info):
                    obstructing_piece = piece
                    new_position = captured_position
                    piece['position'] = captured_position
                    break
            break
    return obstructing_piece, new_position

def chess_notation_to_index(note):
    # Chess board columns (files) and rows (ranks)
    columns = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    rows = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

    col, row = note[0], note[1]
    index = rows[row] * 8 + columns[col]+16
    return grid_positions[index]



def lookup_piece_info_by_notation(notation):
    all_pieces = create_specific_pieces()

    # Mapping from notation to grid position
    columns = "ABCDEFGH"
    rows = "87654321"

    if len(notation) == 2 and notation[0] in columns and notation[1] in rows:
        col = columns.index(notation[0])
        row = rows.index(notation[1])
        # Adjust the index to start from 16
        index = row * 8 + col + 16
        # Find the piece at the given position
        for piece in all_pieces:
            if positions_are_close(piece['position'], grid_positions[index]):
                return piece

    return None

# This is the main execution block which only runs if the script is executed directly (not imported)

# The variables 'moving_piece_notation' and 'goal_notation' are key to this simulation.
# 'moving_piece_notation' specifies the chess piece you want to move, identified by its position in standard chess notation.
# 'goal_notation' represents the target square to which the piece should move, also in standard chess notation.
# If the target square ('goal_notation') is already occupied by another piece, it implies a capture. 
# In such a scenario, the captured piece is relocated to a designated area for captured pieces, 
# which is visually represented by light grey squares on the periphery of the chessboard.
# Adjust these two variables to simulate different moves and captures on the chessboard.

if __name__ == "__main__":
    # Initialize the QPcontroller
    R1 = QPcontroller()

    # Generate grid positions for a chessboard of size 12x8
    grid_positions = [(x * 2.4 + 1.2, y * 2.4 + 1.2) for y in range(11, -1, -1) for x in range(8)]

    # Define the starting and goal positions in chess notation
    moving_piece_notation = 'G8'  # Starting position
    goal_notation = 'B2'          # Target position

    # Retrieve information about the moving piece based on its notation
    moving_piece_info = lookup_piece_info_by_notation(moving_piece_notation)
    if moving_piece_info is None:
        # Handle the case where no piece is found at the given notation
        raise ValueError(f"No piece found at {moving_piece_notation}.")

    # Convert the goal notation to a position on the grid
    goal = chess_notation_to_index(goal_notation)

    # Extract the current position of the moving piece
    x_current = moving_piece_info['position']

    # Define colors for different types of chess pieces
    piece_colors = {
        'King': 'orange', 'Queen': 'red', 'Rook': 'blue',
        'Bishop': 'green', 'Knight': 'goldenrod', 'Pawn': 'purple'
    }

    # Set the target goal for the QPcontroller
    R1.set_goal(goal)

    # Create the chessboard and plot the initial positions of the pieces
    fig, ax = plt.subplots(figsize=(10, 8))
    create_chessboard(ax)  # Function to draw the chessboard
    obs_info = create_specific_pieces(moving_piece_info)  # Gather info about all pieces on the board
    plot_pieces(ax, obs_info, moving_piece_info)  # Function to plot pieces on the board
    ax.scatter(*goal, s=30, color='green')  # Highlight the goal position

    # Check if there's a piece obstructing the goal position and move it if necessary
    obstructing_piece, new_position = move_piece_to_goal(moving_piece_info, goal, obs_info)
    if obstructing_piece:
        # Move the obstructing piece to a new position
        obstructing_piece['position'] = new_position
        # Redraw the chessboard with the updated positions
        ax.clear()
        create_chessboard(ax)
        plot_pieces(ax, obs_info, None)

    # Plot the moving piece at its starting position
    color = piece_colors[moving_piece_info['type']]
    edgecolor = 'black' if moving_piece_info['player'] == 'Player2' else color
    linewidth = 2 if moving_piece_info['player'] == 'Player2' else 0
    initial_circle = plt.Circle(moving_piece_info['position'], moving_piece_info['radius'], color=color, ec=edgecolor, lw=linewidth, alpha=0.8)
    ax.add_patch(initial_circle)

    # Simulate and plot the path for the moving piece
    for i in range(100):
        # Generate the next control action and update the position of the moving piece
        _, target_vel, target_pose = R1.generate_control(x_current, obs_info)
        x_current = target_pose

        # Plot the pieces, excluding the currently moving piece
        plot_pieces(ax, obs_info, None)

        # Plot the moving piece at its updated position
        color = piece_colors[moving_piece_info['type']]
        edgecolor = 'black' if moving_piece_info['player'] == 'Player2' else color
        linewidth = 2 if moving_piece_info['player'] == 'Player2' else 0
        circle = plt.Circle(x_current, moving_piece_info['radius'], color=color, ec=edgecolor, lw=linewidth, alpha=0.8)
        ax.add_patch(circle)

        # Draw the plot and pause briefly to visualize the movement
        plt.draw()
        plt.pause(0.1)

    # Show the final plot
    plt.show()
