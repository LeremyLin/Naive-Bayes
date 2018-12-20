import time
import numpy as np
import csv

for j in range(num_of_feature):
         if file[i][j*2]=='0' and file[i][2*num_of_feature+1]=='0':
            vector[j][0][0]+=1
         elif file[i][j*2]=='0' and file[i][2*num_of_feature+1]=='1':
            vector[j][0][1]+=1
         elif file[i][j*2]=='1' and file[i][2*num_of_feature+1]=='0':  
            vector[j][1][0]+=1
         elif file[i][j*2]=='1' and file[i][2*num_of_feature+1]=='1':
            vector[j][1][1]+=1


def main():
        
   NB('simple-train.txt','simple-test.txt')
   NB('vote-train.txt','vote-test.txt')
   NB('heart-train.txt','heart-test.txt')

# Implement the estimation and prediction
def NB(fileName1,fileName2):
   # Count the total number of y in estimation
   count_y_0 = 0
   count_y_1 = 0

   # Read the data
   file = open(fileName1,'r',
               encoding="utf8").read().splitlines()

   # Record the number of input feature
   num_of_feature = int(file[0])

   # Record the number of data
   length = len(file)

   # Store the total amount of ith vector with the
   # number of input feature and the corresponding output y
   vector = [[[0,0],[0,0]] for i in range(num_of_feature)]
   
   # Loop total number of vector
   for i in range(0,length):

      # Ignore the information about the input data
      if i==0 or i==1:
         continue

      # Count the number of output y with 0 or 1
      if file[i][2*num_of_feature+1]=='0':
         count_y_0+=1
      else:
         count_y_1+=1

      # Store the total amount of ith vector with the
      # number of input feature and the corresponding output y
      for j in range(num_of_feature):
         if file[i][j*2]=='0' and file[i][2*num_of_feature+1]=='0':
            vector[j][0][0]+=1
         elif file[i][j*2]=='0' and file[i][2*num_of_feature+1]=='1':
            vector[j][0][1]+=1
         elif file[i][j*2]=='1' and file[i][2*num_of_feature+1]=='0':  
            vector[j][1][0]+=1
         elif file[i][j*2]=='1' and file[i][2*num_of_feature+1]=='1':
            vector[j][1][1]+=1

   # Count the probability of specific y = 1 or y = 0
   y_0_p = (count_y_0)/(count_y_0+count_y_1)
   y_1_p = (count_y_1)/(count_y_0+count_y_1)


   # Variable to store the prior
   p_prior = [[[0,0],[0,0]] for i in range(num_of_feature)]
   
   # The only difference between Laplace and MLE
   # ith feature with number of x and number of y
   for i in range(num_of_feature):
      p_prior[i][0][0] = (vector[i][0][0]+1)/(vector[i][0][0] +
                                            vector[i][1][0]+2)
      p_prior[i][1][0] = (vector[i][1][0]+1)/(vector[i][0][0] +
                                            vector[i][1][0]+2)
      p_prior[i][0][1] = (vector[i][0][1]+1)/(vector[i][0][1] +
                                            vector[i][1][1]+2)
      p_prior[i][1][1] = (vector[i][1][1]+1)/(vector[i][0][1] +
                                            vector[i][1][1]+2)


   #Prediction start
   e_count_y_0 = 0
   e_count_y_1 = 0

   # Open the test file
   fileTest = open(fileName2,'r',
                   encoding="utf8").read().splitlines()

   # The number of feature in test file
   num_of_feature = int(fileTest[0])

   # The number of vector in test file
   length = len(fileTest)

   # Count the amount of correct prediction
   global corrct_0_predict
   correct_0_predict = 0
   global correct_1_predict
   correct_1_predict = 0

   # Loop the length
   for i in range(0,length):

      if i==0 or i==1:
         continue

      # Store the value of each feature in each vector
      specific_feature = []

      # Add the value of feature to the variable
      for j in range(num_of_feature):
         specific_feature.append(int(fileTest[i][j*2]))

      # Count the posterior of predicted output
      py_0 = 1
      py_1 = 1

      # Loop the feature
      for t in range(num_of_feature):
         # Times probability of each input value given y
         py_0 *= p_prior[t][specific_feature[t]][0]
         py_1 *= p_prior[t][specific_feature[t]][1]

      # Store the total amount of each y=0 and y=1
      if fileTest[i][2*num_of_feature+1]=='0':
         e_count_y_0 += 1
      else:
         e_count_y_1 += 1

      # Times the value with the probability of y_0 or y_1
      py_0 *= y_0_p
      py_1 *= y_1_p

      # Store the larger output value
      predict_y = 0

      # Judege the prediction and output the larger one
      if py_0 > py_1:
              
         predict_y = 0
      else:
         predict_y = 1

      # Count the number of correct for each case
      if fileTest[i][2*num_of_feature+1]=='0':
         if predict_y == 0:
            correct_0_predict+=1
      else:    
         if predict_y ==1:
            correct_1_predict+=1
   
   print(fileName2)
   print("For Laplace:")
   print("Case0: tested", e_count_y_0, "correctly classified",
         correct_0_predict)
   print("Case1: tested", e_count_y_1, "correctly classified",
         correct_1_predict)
   print("Overall: tested",e_count_y_0 + e_count_y_1,
         "correctly classified",correct_0_predict + correct_1_predict)
   print("Accuracy =", float((correct_0_predict+
                      correct_1_predict)/(e_count_y_0 + e_count_y_1)))
   print("\n")

if __name__ == '__main__':
        main()
