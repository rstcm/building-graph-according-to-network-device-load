import matplotlib.pyplot as pyp
import matplotlib.animation as animation

#Creating new figure
figure = pyp.figure()

#Creating subplot with 1 row, 1 column, and index 1 meaning single subplot
subplot = figure.add_subplot(1, 1, 1)
pyp.plot([1.2, 3.2, 4.5, 0.2, 0, 4.4])
pyp.show()