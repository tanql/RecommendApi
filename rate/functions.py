import math

def sim(person1,person2):
    bothRatings = {}
    for item in dictionary[person1]:
        if item in dictionary[person2]:
            bothRatings[item] = 1

    amountOfRatings = len(bothRatings)
    if amountOfRatings == 0:
         return 0

     # Add up all the preferences of each user
    person1_preferences_sum = sum([dictionary[person1][item] for item in bothRatings])
    person2_preferences_sum = sum([dictionary[person2][item] for item in bothRatings])

     # Sum up the squares of preferences of each user
    person1_square_preferences_sum = sum([pow(dictionary[person1][item],2) for item in bothRatings])
    person2_square_preferences_sum = sum([pow(dictionary[person2][item],2) for item in bothRatings])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([dictionary[person1][item] * dictionary[person2][item] for item in bothRatings])

   # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/amountOfRatings)
    denominator_value = math.sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/amountOfRatings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/amountOfRatings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value/denominator_value
        return r

