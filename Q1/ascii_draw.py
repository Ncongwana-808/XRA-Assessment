# Function to draw a rectangle of given width and height using a specified character
def draw_rectangle(width, height, char):
    while True: 
        try: # Loop until valid inputs are provided
            if width < 3 or height  < 3:
                print("!!Error , Width and height must be at greater than 2.")                  
                width = int(input("enter the width you want to draw "))
                height = int(input("enter the height you want to draw "))
                continue
            
            char = input("choose any character you would like to use to draw ")  
            if len(char) != 1: # Ensure only a single character is used
                print("Please enter a single character.")
                continue
            break # Exit the loop if all inputs are valid          
        
        except ValueError:
            print(" Invalid input. Please enter numeric values for width and height.")
            
    for j in range(height): # Loop through each row
        for i in range(width):# Loop through each column
            if(j == 0 or j == height - 1 or i == 0 or i == width - 1):# Check if it's a border position
                print(char, end="")# Print the character for borders
            else:
                print(" ", end="")
        print()# Move to the next line after each row

#call the function to execute
draw_rectangle(0, 0, '')