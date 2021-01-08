import matplotlib.pyplot as pyp
import matplotlib.animation as animation

#Creating new figure
figure = pyp.figure()

#Creating subplot with 1 row, 1 column, and index 1 meaning single subplot
subplot = figure.add_subplot(1, 1, 1)

def animation_function(i):

    cpu_data = open("D:\\netapp\\3_build_graph\\cpu.txt").readlines()

    x = []

    for each_value in cpu_data:
        if len(each_value) > 1:
            x.append(float(each_value))

    #Clearing/Refreshing the figure to avoid overwriting for each new poll (every 10 seconds)
    subplot.clear()

    #Plotting the values in the list
    subplot.plot(x)

#Using the figure, the function and polling interval of 10000ms (10 seconds) to build the graph
graph_animation = animation.FuncAnimation(figure, animation_function, interval = 10000)

#Displaying the grapgh to the screen
pyp.show()

