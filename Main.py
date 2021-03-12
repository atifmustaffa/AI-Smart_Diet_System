"""
Smart Diet System
Version 1.0
Artificial Intelligence Project
KICT-IIUM
"""

import time;
import os;
import math;

# Import external python files - classes
from classes.User import User;
from classes.Report import Report;
from classes.Food import Food;

# Main method initialization
def main():
	#os.system("cls");
	# Welcome Message
	print("\n"
		"####################################\n"
		"#                                  #\n"
		"#   Welcome to Smart Diet System   #\n"
		"#                                  #\n"
		"####################################\n"
		"      'Keep your body healhty'      \n");

	print("Loading apps...");
	time.sleep(0.5);

	# Open normal user view
	normal_user_view();

def normal_user_view():
	# Start conversation with user
	user_name = input("\nHello there. Can you tell us your name? : ");
	response = input("Hi " + user_name + ",\nTo calculate your daily calories, we need some information about you. Is that okay with you? y/n ");
	if response.lower() == 'y':
		# Proceed with user details, else ask user to exit apps
		# The loops(incorrect_input) are for bulletproof answer.
		incorrect_input = True;
		while(incorrect_input):
			age = input("Your age: ");
			if age.isdigit():
				age = int(age);
				break;
			else:
				print("\n>> Invalid input. Please re-enter.\n");
		while(incorrect_input):
			gender = input("Your gender (m - male, f - female): ");
			if gender == 'f' or gender == 'm':
				break;
			else:
				print("\n>> Invalid input. Please re-enter.\n");
		while(incorrect_input):
			height = input("Your height (in centimeter, cm): ");
			if height.replace(".", "").isdigit():
				height = float(height);
				break;
			else:
				print("\n>> Invalid input. Please re-enter.\n");
		while(incorrect_input):
			weight = input("Your weight (in kilogram, kg): ");
			if weight.replace(".", "").isdigit():
				weight = float(weight);
				break;
			else:
				print("\n>> Invalid input. Please re-enter.\n");
		while(incorrect_input):
			weight_goal = input("Your weight goal after a week (in kilogram, kg) *Enter your current weight to maintain weight*: ");
			if weight_goal.replace(".", "").isdigit():
				weight_goal = float(weight_goal);
				# Maximum weight different is 10kg per week
				if abs(weight_goal - weight) > 0.91:
					print("\n>> Irrelevant weight goal (max: +/- 0.91kg). Please re-enter.\n");
				else:
					break;
			else:
				print("\n>> Invalid input. Please re-enter.\n");
		while(incorrect_input):
			activity_level = int(input("\nYour activity level:\n" +
				"1 - Sedentary (Little exercise, desk job)\n" +
				"2 - Lightly active (Light exercise, sports 1-3 days/week)\n" +
				"3 - Moderately active (Moderate exercise, sports 3-5 days/week)\n" +
				"4 - Very active (Hard exercise, sports 6-7 days/week)\n"
				"5 - Extra active (Hard daily exercise, sports and physical labor job or 2 times training per day)\n"));
			if activity_level >= 1 and activity_level <= 5:
				break;
			else:
				print("\n>> Invalid input. Please re-enter.");

		# Create user_details object and add to list
		users.append(User(user_name, age, gender.lower(), height, weight, weight_goal, activity_level));
		user_index = len(users)-1; # Indicating last element of list

		print("Generating report...\n");
		time.sleep(0.8);

		# Print user details, final calories report and suggested meals
		print(
			"User Details\n"
			"===========================================");		
		# Print user details (user in last element in the list-recently added)
		users[user_index].printUserDetails();

		# Calculate bmi, determine BMI Status and display result
		print(
			"Your BMI is " + str("%.1f" % users[user_index].getBMI()) + " and your weight status is " + users[user_index].getBMIStatus() + "\n\n"
			"Calories Report\n"
			"===========================================");
		# Calculate normal daily calories(maintain weight)
		daily_calories = users[user_index].getDailyCalories();
		print("Daily calories you need to maintain your current weight is " + str("%d" % daily_calories));
		# Determine goal lose/gain weight, display weight change and new calories value
		# Maintain weight(diff = 0) prints nothing
		diff = users[user_index].getWeightDiff();
		daily_calories_change = users[user_index].getCaloriesChange();
		if diff < 0:
			# Lose weight 'diff' kg -ve value
			print("Daily calories you need to lose weight (" + str("%.2f" % abs(diff)) + "kg/week) is " + str("%d" % daily_calories_change));
		elif diff > 0:
			# Gain weight 'diff' kg +ve value
			print("Daily calories you need to gain weight (" + str("%.2f" % abs(diff)) + "kg/week) is " + str("%d" % daily_calories_change));
		
		calories_each_meal = daily_calories_change/3;
		meal_report = getSuggestedMeal(calories_each_meal)
		# Print the meals with the closest total calories of 3meals
		print("\n"
			"Suggested meal\n"
			"===========================================\n" +
			meal_report
			);

		# Generate full report and print to file
		r = Report(users, user_index, meal_report);
		r.printToFile();

	response = input("Thank you for using Smart Diet System\nStart over? y/n ");
	if response.lower() == 'y':
		main();
	else:
		print("Exitting...")
		time.sleep(0.5);
		return 0;

def getSuggestedMeal(cal):
	text = "";

	# Breakfast Foods
	minDiff = 9999999;
	for i in range(0, len(breakfast)):
		totalCal = 0;
		for j in range(0, len(breakfast[i])):
			if (i == 0 and j == 0) or breakfast[i][j]:
				totalCal += float(foods[breakfast[i][j]].calories);
		if abs(totalCal-cal) < minDiff:
			minDiff = abs(totalCal-cal);
			bset = i;
			bsetCal = totalCal;

	text += "Breakfast:\n";
	for j in range(0, len(breakfast[bset])):
		text += "\n"
		if (bset == 0 and j == 0) or breakfast[bset][j]:
			text += "  Meal Name " +str(j+1) + "  : " + foods[breakfast[bset][j]].name + "\n"
			text += "  Amount       : " + foods[breakfast[bset][j]].amount + "\n"
			text += "  Calories     : " + foods[breakfast[bset][j]].calories + "\n"
	text += "  Total Breakfast Calories : " + str("%.1f" % (bsetCal)) + "\n\n"

	# Lunch Foods
	minDiff = 9999999;
	for i in range(0, len(lunch)):
		totalCal = 0;
		for j in range(0, len(lunch[i])):
			if (i == 0 and j == 0) or lunch[i][j]:
				totalCal += float(foods[lunch[i][j]].calories);
		if abs(totalCal-cal) < minDiff:
			minDiff = abs(totalCal-cal);
			lset = i;
			lsetCal = totalCal;

	text += "Lunch:\n";
	for j in range(0, len(lunch[lset])):
		text += "\n"
		if (lset == 0 and j == 0) or lunch[lset][j]:
			text += "  Meal Name " +str(j+1) + "  : " + foods[lunch[lset][j]].name + "\n"
			text += "  Amount       : " + foods[lunch[lset][j]].amount + "\n"
			text += "  Calories     : " + foods[lunch[lset][j]].calories + "\n"
	text += "  Total Lunch Calories : " + str("%.1f" % (lsetCal)) + "\n\n"

	# Dinner Foods
	minDiff = 9999999;
	for i in range(0, len(dinner)):
		totalCal = 0;
		for j in range(0, len(dinner[i])):
			if (i == 0 and j == 0) or dinner[i][j]:
				totalCal += float(foods[dinner[i][j]].calories);
		if abs(totalCal-cal) < minDiff:
			minDiff = abs(totalCal-cal);
			dset = i;
			dsetCal = totalCal;

	text += "Dinner:\n";
	for j in range(0, len(dinner[dset])):
		text += "\n"
		if (dset == 0 and j == 0) or dinner[dset][j]:
			text += "  Meal Name " +str(j+1) + "  : " + foods[dinner[dset][j]].name + "\n"
			text += "  Amount       : " + foods[dinner[dset][j]].amount + "\n"
			text += "  Calories     : " + foods[dinner[dset][j]].calories + "\n"
	text += "  Total Dinner Calories : " + str("%.1f" % (dsetCal)) + "\n"
	totalMealCal = math.ceil(bsetCal + lsetCal + dsetCal);
	text += "=============================\n"
	text += "Total Calories : " +str(totalMealCal) + "\n"
	text += "=============================";
	return text;


############ END OF METHODS INITIALIZATION ############

# Initialize list of users
users = [];
foods = [];

# List for grouping meals
breakfast = [[0 for x in range(3)] for y in range(8)];
lunch = [[0 for x in range(3)] for y in range(8)];
dinner = [[0 for x in range(3)] for y in range(8)];

# Load database from file
reports_file_path = "files/reports.txt";
users_file_path = "files/users.txt";
foods_file_path = "files/foods.txt";

# Checks existing files, create file if file not exists
if not os.path.exists(reports_file_path):
	print("File '" + reports_file_path + "' is not exists");

if not os.path.exists(foods_file_path):
	print("File '" + foods_file_path + "' is not exists");
else:
	# Read foods data fom ext file
	f = open(foods_file_path, "r");
	lines = f.read().splitlines();

	# Each food has 5 attribute, so divide all lines by 5
	count = 0; # foods count
	bc = 0; # bfast count
	lc = 0; # lunch count
	dc = 0; # dinner count
	for y in range(0, int(len(lines)/5)):
		y *= 5;
		foods.append(Food(lines[y], lines[y+1], lines[y+2], lines[y+3]));

		#Grouping of type of meals, into specific array
		lastChar = foods[count].meal_type[len(foods[count].meal_type)-1];
		if y/5 == int(len(lines)/5)-1: # Prevent invalid next char
			nxtLastChar = "9";
		else:
			nxtLastChar = lines[y+5][len(lines[y+5])-1];

		if "breakfast" in foods[count].meal_type:
			breakfast[int(lastChar)-1][bc] = count;
			if int(nxtLastChar) > int(lastChar): # Reset bcount for nxtchar != char(different set), else inc bc by 1
				bc = 0;
			else:
				bc += 1;
		elif "lunch" in foods[count].meal_type:
			lunch[int(lastChar)-1][lc] = count;
			if int(nxtLastChar) > int(lastChar):
				lc = 0;
			else:
				lc += 1;
		else:
			dinner[int(lastChar)-1][dc] = count;
			if int(nxtLastChar) > int(lastChar):
				dc = 0;
			else:
				dc += 1;
		count += 1;

# Start program by calling main method
main();
