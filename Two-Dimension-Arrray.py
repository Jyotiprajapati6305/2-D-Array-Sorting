import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

class SortVisualizer:
    def __init__(self, array_2d):
        self.original_2d = np.array(array_2d)
        self.rows, self.cols = self.original_2d.shape
        self.flat_array = self.original_2d.flatten().copy()
        self.bubble_steps = []
        self.selection_steps = []
        
    def bubble_sort(self):
        """Generate steps for bubble sort"""
        arr = self.flat_array.copy()
        n = len(arr)
        
        for i in range(n - 1):
            for j in range(n - i - 1):
                self.bubble_steps.append({
                    'array': arr.copy(),
                    'comparing': [j, j + 1],
                    'sorted': list(range(n - i, n)),
                    'description': f'Comparing {arr[j]} and {arr[j+1]}'
                })
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.bubble_steps.append({
                        'array': arr.copy(),
                        'comparing': [j, j + 1],
                        'sorted': list(range(n - i, n)),
                        'description': f'Swapped: {arr[j]}, {arr[j+1]}'
                    })
        
        self.bubble_steps.append({
            'array': arr.copy(),
            'comparing': [],
            'sorted': list(range(n)),
            'description': 'Sorted!'
        })
        
        return self.bubble_steps
    
    def selection_sort(self):
        """Generate steps for selection sort"""
        arr = self.flat_array.copy()    
        n = len(arr)
        
        for i in range(n - 1):
            min_idx = i
            
            self.selection_steps.append({
                'array': arr.copy(),
                'comparing': [i],
                'sorted': list(range(i)),
                'description': f'Finding min from index {i}'
            })
            
            for j in range(i + 1, n):
                self.selection_steps.append({
                    'array': arr.copy(),
                    'comparing': [min_idx, j],
                    'sorted': list(range(i)),
                    'description': f'Comparing {arr[min_idx]} with {arr[j]}'
                })
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                self.selection_steps.append({
                    'array': arr.copy(),
                    'comparing': [i],
                    'sorted': list(range(i + 1)),
                    'description': f'Placed {arr[i]} at position {i}'
                })
        
        self.selection_steps.append({
            'array': arr.copy(),
            'comparing': [],
            'sorted': list(range(n)),
            'description': 'Sorted!'
        })
        
        return self.selection_steps
    
    def visualize_side_by_side(self, save_gif=False):
        """Create side-by-side animated visualization"""
        self.bubble_sort()
        self.selection_sort()
        
        # Make both have same number of steps for synchronized animation
        max_steps = max(len(self.bubble_steps), len(self.selection_steps))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        def draw_array(ax, step, title):
            ax.clear()
            
            arr = step['array']
            comparing = step['comparing']
            sorted_indices = step['sorted']
            desc = step['description']
            
            # Reshape array back to 2D for display
            arr_2d = arr.reshape(self.rows, self.cols)
            
            # Calculate cell size based on array dimensions
            cell_size = 0.7
            
            # Draw grid
            for i in range(self.rows):
                for j in range(self.cols):
                    flat_idx = i * self.cols + j
                    value = arr_2d[i, j]
                    
                  # Determine pastel color
                    if flat_idx in sorted_indices:
                        color = '#ABEBC6'   # pastel green
                    elif flat_idx in comparing:
                        color = '#F9E79F'   # pastel yellow
                    else:
                        color = '#A7C7E7'   # pastel blue

                    # Draw rectangle
                    x_pos = j * cell_size
                    y_pos = (self.rows - i - 1) * cell_size
                    rect = Rectangle((x_pos, y_pos), cell_size * 0.9, cell_size * 0.9, 
                                    facecolor=color, edgecolor='black', linewidth=1.5)
                    ax.add_patch(rect)
                    
                    # Add text
                    ax.text(x_pos + cell_size * 0.45, y_pos + cell_size * 0.45, str(value),
                           ha='center', va='center', fontsize=9, fontweight='bold')
            
            ax.set_xlim(-0.2, self.cols * cell_size)
            ax.set_ylim(-0.8, self.rows * cell_size)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Title
            ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
            
            # Description
            ax.text(self.cols * cell_size / 2, -0.4, desc, ha='center', fontsize=8,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        def draw_frame(step_idx):
            # Handle bubble sort
            if step_idx < len(self.bubble_steps):
                bubble_step = self.bubble_steps[step_idx]
            else:
                bubble_step = self.bubble_steps[-1]
            
            # Handle selection sort
            if step_idx < len(self.selection_steps):
                selection_step = self.selection_steps[step_idx]
            else:
                selection_step = self.selection_steps[-1]
            
            draw_array(ax1, bubble_step, f'Bubble Sort - Step {min(step_idx + 1, len(self.bubble_steps))}/{len(self.bubble_steps)}')
            draw_array(ax2, selection_step, f'Selection Sort - Step {min(step_idx + 1, len(self.selection_steps))}/{len(self.selection_steps)}')
            
        # Create animation
        anim = animation.FuncAnimation(fig, draw_frame, frames=max_steps,
                                      interval=500, repeat=True)
        
        # Add main title
        fig.suptitle('2D Array Sorting: Bubble vs Selection', fontsize=15, fontweight='bold', y=0.96)
        
        # Add legend
        legend_elements = [
             Rectangle((0, 0), 1, 1, fc='#A7C7E7', ec='black', label='Unsorted'),
                Rectangle((0, 0), 1, 1, fc='#F9E79F', ec='black', label='Comparing'),
            Rectangle((0, 0), 1, 1, fc='#ABEBC6', ec='black', label='Sorted')
        ]

        fig.legend(handles=legend_elements, loc='lower center', 
                  ncol=3, fontsize=9, bbox_to_anchor=(0.5, 0.01))
        
        if save_gif:
            anim.save('sorting_comparison_2d.gif', writer='pillow', fps=2)
            print("Animation saved as sorting_comparison_2d.gif")
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.show()
        
        return anim


# Example usage
if __name__ == "__main__":
    # Create a larger 2D array (6x6)
    # Generate random 6x6 array with numbers 1–99
    array_2d = np.random.randint(1, 100, (6, 6))

    # array_2d = [
    #     [89, 34, 56, 12, 78, 45],
    #     [23, 67, 91, 15, 38, 72],
    #     [29, 84, 51, 66, 41, 95],
    #     [18, 63, 27, 80, 33, 59],
    #     [42, 74, 19, 86, 53, 31],
    #     [68, 25, 92, 47, 14, 76]
    # ]
    
    print("Original 2D Array (6x6):")
    print(np.array(array_2d))
    print("\nFlattened for sorting:", np.array(array_2d).flatten())
    print(f"\nTotal elements: {len(np.array(array_2d).flatten())}")
    print("\nStarting side-by-side visualization...")
    print("Close the window to exit.\n")
    
    visualizer = SortVisualizer(array_2d)
    visualizer.visualize_side_by_side(save_gif=False)
