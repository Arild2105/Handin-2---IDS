import cv2
import numpy as np
from PIL import Image
from keras import models
import tensorflow as tf
import requests
import re
import time

def intro():
    print("Hello. I'm gonna help you find some meals today :D")
    print("Right now I can only help you find meals containing salt or cucumbers but later I will learn a lot more :D")
    print("Are you ready to find a meal?")

    answer = input()
    answer_lowerCase = answer.lower()

    if answer_lowerCase == "yes":
        print("Alright. Let's GO!")
        recognize_food_item()
    
    elif answer_lowerCase == "no":
        print("Okay.")
        user_ends_conversation()

    else:
        print("\nplease answer yes or no")
        intro()

def predicted_food():

    if final_guess == 0:

        print("\nIt looked to me like you were holding salt. Is this correct?")
        correct_answer = input()
        correct_answer_lowerCase = correct_answer.lower() 

        if correct_answer_lowerCase == "yes":
            
            meals_with_salt = (requests.get("https://themealdb.com/api/json/v1/1/filter.php?i=salt")).json()
            list_meal_with_salt = meals_with_salt["meals"]

            for meal_salt in list_meal_with_salt:
                print("\n")
                print(meal_salt["strMeal"])
                print(meal_salt["strMealThumb"])
            
            choose_the_meal()

        elif correct_answer_lowerCase == "no":
            recognize_food_item()
        
        else:
            print("\nplease answer yes or no.")
            predicted_food()
        

    elif final_guess == 1:

        print("\nIt looked to me like you were holding cucumber. Is this correct?")
        correct_answer = input()
        correct_answer_lowerCase = correct_answer.lower() 

        if correct_answer_lowerCase == "yes":

            meals_with_cucumber = (requests.get("https://themealdb.com/api/json/v1/1/filter.php?i=Cucumber")).json()
            list_meals_with_cucumber = meals_with_cucumber["meals"]

            for meal_cucumber in list_meals_with_cucumber:
                print("\n")
                print(meal_cucumber["strMeal"])
                print(meal_cucumber["strMealThumb"])

            choose_the_meal()
        
        elif correct_answer_lowerCase == "no":
            recognize_food_item()
        
        else:
            print("\nplease answer yes or no.")
            predicted_food()

def recognize_food_item():
    
    global final_guess

    model = models.load_model('C:/Users/louis/Desktop/IDS_handin_2/converted_keras/keras_model_saltCucumber.h5')
    video = cv2.VideoCapture(0)

    start_time = time.time()
    seconds = 3
    elapsed_time = 0

    while elapsed_time < seconds:
        
        elapsed_time = time.time() - start_time
        _, frame = video.read()

                #Convert the captured frame into RGB
        im = Image.fromarray(frame, 'RGB')

                #Resizing into dimensions you used while training
        im = im.resize((224,224))
        img_array = np.array(im)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = (img_array.astype(np.float32) / 127.0) - 1

                #Calling the predict function using keras
        prediction = model.predict(img_array)
        print(prediction)
        labels = ['salt', 'cucumber']

        guess_ingredient = max(prediction[0])
        print(guess_ingredient)
        final_guess = (list(prediction[0])).index(guess_ingredient)
        print(labels[final_guess])

        cv2.imshow("Prediction", frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    predicted_food()

    return final_guess

def choose_the_meal():
    
    ingredients = ["strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5", "strIngredient6", "strIngredient7"]

    if final_guess == 0:
     
        print("\nType in a searchword or meal below.")

        try:
            choose_meals = input()
            choose_meals_lowerCase = choose_meals.lower()

            if choose_meals_lowerCase in '':
                choose_meals_no_space = re.sub('','%',choose_meals_lowerCase)

            chosen_meal = (requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s=" + choose_meals_lowerCase)).json()
            chosen_meal_from_list = chosen_meal["meals"]
            for meal in chosen_meal_from_list: 
                print("\n")
                print(meal["strMeal"])
                print(meal["strMealThumb"])
                print(meal["strCategory"])
                print(meal["strArea"])

            print("\nThese are all the meals containing your searchword. Which one do you want?")

            final_answer = input()
            final_answer_lowerCase = final_answer.lower()

            if final_answer_lowerCase in '':
                choose_meals_no_space = re.sub('','%',choose_meals_lowerCase)

            chosen_final_meal = (requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s=" + final_answer_lowerCase)).json()
            chosen_final_meal_from_list = chosen_final_meal["meals"]
            for final_meal in chosen_final_meal_from_list:
                print("\n")
                print(final_meal["strMeal"])
                print(final_meal["strMealThumb"])
                print(final_meal["strCategory"])
                print(final_meal["strArea"])
                print(final_meal["strInstructions"])
                for i in ingredients:
                    print(meal[i]) 

            natural_end_to_conversation()             

        except TypeError: 
            print("\nThis meal does not exists. Please try again")
            choose_the_meal() 

    elif final_guess == 1:
      
        print("\nType in a searchword or meal below.")

        try:
            choose_meals = input()
            choose_meals_lowerCase = choose_meals.lower()

            if choose_meals_lowerCase in '':
                choose_meals_no_space = re.sub('','%',choose_meals_lowerCase)
            chosen_meal = (requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s=" + choose_meals_lowerCase)).json()

            chosen_meal_from_list = chosen_meal["meals"]
            for meal in chosen_meal_from_list:
                print("\n")
                print(meal["strMeal"])
                print(meal["strMealThumb"])
                print(meal["strCategory"])
                print(meal["strArea"])

            print("\nThis/these are the meals containing your searchword. Which one do you want?")

            final_answer = input()
            final_answer_lowerCase = final_answer.lower()

            if final_answer_lowerCase in '':
                choose_meals_no_space = re.sub('','%',choose_meals_lowerCase)

            chosen_final_meal = (requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s=" + final_answer_lowerCase)).json()
            chosen_final_meal_from_list = chosen_final_meal["meals"]
            for final_meal in chosen_final_meal_from_list:
                print("\n")
                print(final_meal["strMeal"])
                print(final_meal["strMealThumb"])
                print(final_meal["strCategory"])
                print(final_meal["strArea"])
                print(final_meal["strInstructions"])
                for i in ingredients:
                    print(meal[i])
                    
            natural_end_to_conversation()                

        except TypeError: 
            print("\nThis meal does not exists. Please try again")
            choose_the_meal() 

def user_ends_conversation():
    print("\nAre you sure you don't want me to help you find a meal today?")

    goodbye_or_not = input()
    goodbye_or_not_lowerCase = goodbye_or_not.lower()

    if goodbye_or_not_lowerCase == "yes":
        print("\nAlright. Bye bye")
    elif goodbye_or_not_lowerCase == "no":
        print("\nGreat! let's start from the beginning then :D")
        intro()
    else:
        print("\nplease answer yes or no")
        user_ends_conversation()

def natural_end_to_conversation():
    print("\nis this the meal you wanted?")
    final_answer = input()
    final_answer_lowerCase = final_answer.lower()

    if final_answer_lowerCase == "yes":
        print("\nGreat! I hope you enjoy your meal :D Bye")
    
    elif final_answer_lowerCase == "no":
        print("\nI'm sorry about that")
        choose_the_meal()
    
    else:
        print("\nPlease answer yes or no.")
        natural_end_to_conversation()


intro()