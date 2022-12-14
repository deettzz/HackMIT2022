# Data handling
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
# Model
from sklearn import linear_model
# Cross-validation, training and splitting
from sklearn.model_selection import KFold
# Measuring metrics
from sklearn.metrics import mean_squared_error
# GUI
import tkinter as tk

""" DOCUMENTATION:
GUI INPUT:
- alcohol percentage
- residual sugar percentage
MODEL OUTPUT:
- wine quality
"""

## GUI FUNCTIONS ##
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas1.create_polygon(points, **kwargs, smooth=True)

predicted_label = tk.Label
def values():
    # first input variable from GUI
    global alcPercInput
    alcPercInput = entry1.get()
    global sugPercInput
    sugPercInput = entry2.get()
    # Features, Input:
    resultsBox = round_rectangle(130, 250, 470, 300, fill="#d9a5b1")
    y_predicted = str(round(model.predict([[alcPercInput, sugPercInput]])[0], 2))
    y_predicted = 'Wine Quality: '+y_predicted+' on a scale of 1 to 10.'
    predicted_label = tk.Label(root, fg="white", font=('futura', 12), text=y_predicted, bg="#d9a5b1")
    canvas1.create_window(300, 275, window=predicted_label)

## OPEN NECESSARY FILES
# Path to prev dir contains this file
dir = os.path.abspath(os.path.dirname(__file__))
# -> open data file with this directory
data_file_address = os.path.join(dir, "WineQuality-Red.csv")
# -> open gradient2.PNG file with this directory
BG_address = os.path.join(dir, "Pictures/wineBG.PNG")
# -> open wordArt.PNG file with this directory
wordArt_address = os.path.join(dir, "Pictures/wordArt.PNG")

## READ AND DEFINE DATA VARIABLES
df = pd.read_csv(data_file_address)
# Independent variables
X = df[['alcohol', 'residual sugar']]
# Dependent variable
y = df['quality']

## CREATE MODEL
# Utilize sklearn to define model
model = DecisionTreeClassifier()
# Cross-validation, split into training and testing data as well
kf = KFold(n_splits=3, shuffle=True, random_state=None)
for train_index, test_index in kf.split(X):
    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]
    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]
    model.fit(X_train, y_train)
# Additional Information on Fit of Model
# print('Intercept: \n', regr.intercept_)
# print('Coefficients: \n', regr.coef_)

## MODEL METRICS
y_pred = model.predict(X_test)
acc_score = accuracy_score(y_test,y_pred)
#print(y_test, y_pred)
print('Accuracy OF MODEL:', acc_score)

## GUI
# Initialize GUI
root= tk.Tk()
canvas1 = tk.Canvas(root, width = 600, height = 400)
root.resizable(False, False)
canvas1.pack()
# Size and background color of output GUI
background=tk.PhotoImage(file=BG_address)
background=background.subsample(2,2)
canvas1.create_image(300, 200, image = background)
# Round edges of output GUI
rect = round_rectangle(100, 105, 500, 350, fill="#302A28")
# Add title to output GUI
root.title("Wine About It!")
titleArt=tk.PhotoImage(file=wordArt_address)
titleArt=titleArt.subsample(5,5)
canvas1.create_image(300, 55, image = titleArt)
# Add final equation of model to output GUI
# Intercept of equation
#print_intercept = 'Model Intercept: '+str(round(model.intercept_, 4)) # sklearn function to derive intercept
#canvas1.create_text(300, 360, fill="white", font=('futura', 10),text=print_intercept, justify='center')
# Coefficients of equation
#coefs_rounded = [round(num, 4) for num in list(model.coef_)]
#print_coefs = 'Coefficients: '+ str(coefs_rounded) # sklearn function to derive intercept
#canvas1.create_text(300, 380, fill="white", font=('futura', 10),text=print_coefs, justify='center')
# Create entry box to collect input joke
# First ind variable
canvas1.create_text(300, 130, fill="white",font=('futura', 10), text='Enter Alcohol Percentage of Wine: ')
entry1 = tk.Entry(root, bd=0) # create 1st entry box
canvas1.create_window(300, 245, width=350, window=entry1)
# Second ind variable
canvas1.create_text(300, 215, fill="white",font=('futura', 10), text='Enter Residual Sugar Percentage of Wine: ')
entry2 = tk.Entry(root, bd=0) # create 1st entry box
canvas1.create_window(300, 170, width=350, window=entry2)
# Button inputs datapoint (joke and parsed input from joke) to model and displays output
model_output_button = tk.Button(root, font=('futura'),text='Get Wine Quality!', bd=0,command=values)
canvas1.create_window(300, 325, window=model_output_button)
# Continue looping over script with GUI input
root.mainloop()
