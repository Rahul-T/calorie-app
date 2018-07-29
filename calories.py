# -*- coding: utf-8 -*-
"""
Main file for Calories App
Author: Rahul Tholakapalli
"""

from flask import Flask, render_template, request, url_for, redirect;
import mysql.connector;
import re;
    



app = Flask(__name__)
@app.route("/")
def main():
    cnx = mysql.connector.connect(user='root', password='Static r4in',
                              host='localhost',
                              database='Calories')
    result = retrieveData(cnx)
    cnx.close()
    return render_template('main.html', result=result)

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    cnx = mysql.connector.connect(user='root', password='Static r4in',
                              host='localhost',
                              database='Calories')    
    result = retrieveData(cnx)
    if request.method == 'POST':
        f = request.form
        
        #Validate input
        index = 0
        for value in f.getlist("date"):
            flag = int(f.getlist("flag")[index])
            if flag == 1:
                date = f.getlist("date")[index]
                
                r = re.compile('\d{4}-\d{2}-\d{2}')
                if r.match(date) is None:
                    cnx.close() 
                    errorMessage = "Make sure all dates are in the following format: YYYY-MM-DD"
                    return render_template('edit.html', result = result, errorMessage = errorMessage)
                
                try:
                    calories = int(f.getlist("calories")[index])
                    carbs = int(f.getlist("carbs")[index])
                    protein = int(f.getlist("protein")[index])
                    fat = int(f.getlist("fat")[index])
                    weight = float(f.getlist("weight")[index])
                except:
                    cnx.close()
                    errorMessage = "All values must be non-negative integers for the date " + date
                    return render_template('edit.html', result = result, errorMessage = errorMessage)
                
                if calories < 0 or carbs < 0 or protein < 0 or fat < 0 or weight < 0:
                    cnx.close() 
                    errorMessage = "All values must be non-negative integers for the date " + date
                    return render_template('edit.html', result = result, errorMessage = errorMessage)
                
            index += 1
        
        #If data for a specific row is changed, insert/update that row in database
        index = 0
        for value in f.getlist("date"):
            flag = int(f.getlist("flag")[index])
            if flag == 1:
                date = f.getlist("date")[index]
                calories = int(f.getlist("calories")[index])
                carbs = int(f.getlist("carbs")[index])
                protein = int(f.getlist("protein")[index])
                fat = int(f.getlist("fat")[index])
                weight = float(f.getlist("weight")[index])
                insertData(cnx, date, calories, carbs, protein, fat, weight)
                result = retrieveData(cnx)
            index += 1
    
    cnx.close()    
    return render_template('edit.html', result = result)


def retrieveData(cnx):
    cursor = cnx.cursor()
    cursor.execute("""SELECT trackDate, calories, carbs, protein, fat, weight, 0 flag 
                   FROM calorieCounter ORDER BY trackDate DESC""")
    result = cursor.fetchall()
    return result
    
def insertData(cnx, date, calories, carbs, protein, fat, weight):
    cursor = cnx.cursor()
    cursor.execute("""INSERT INTO calorieCounter(trackDate, calories, carbs, protein, fat, weight)
        VALUES(%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE calories = %s, carbs = %s, 
        protein = %s, fat = %s, weight = %s """, 
        (date, calories, carbs, protein, fat, weight, calories, carbs, protein, fat, weight))
    cnx.commit()
    return



