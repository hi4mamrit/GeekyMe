"""
courses_rest_api.py (Creating a server using REST API)
Implementing GET,POST,PUT,DELETE methods for Different Courses

--> startup the server using "python app.py" in cmdline

Following Formats supported on Browsers and cmdline:-
--> To view available courses
    http://127.0.0.1:5000/courses/
    
--> To view a particular course using the index
    http://127.0.0.1:5000/courses/1
    
--> To add a new course
    curl -i -H "Content-Type: Application/json" -X POST http://127.0.0.1:5000/courses/add
    
--> To update Teacher of course using index
    curl -i -H "Content-Type: Application/json" -X POST http://127.0.0.1:5000/courses/update/2

--> To delete course using index    
    curl -i -H "Content-Type: Application/json" -X POST http://127.0.0.1:5000/courses/delete/2

#######
Install CURL:-
**********************
Download curl zip from https://curl.se/windows/
Extract the contents (if you have downloaded the correct version you should find curl.exe)
Place curl.exe in a folder where you keep your software (e.g. D:\software\curl\curl.exe)
To run curl from the command line
a) Right-hand-click on "My Computer" icon
b) Select Properties
c) Click 'Advanced system settings' link
d) Go to tab [Advanced] - 'Environment Variables' button
e) Under System variable select 'Path' and Edit button
f) Add a semicolon followed by the path to where you placed your curl.exe (e.g. ;D:\software\curl)

Now you can run from the command line by typing:
curl www.google.com
"""

#import the current file's path to sys.path
import sys,pathlib
cwd=str(pathlib.Path().resolve())
if cwd not in sys.path:
    sys.path.append(cwd)

def get_courses():
    #Creating a list of dictionaries related to course in json style

    master_list=[]
    course=dict()
    courses = ['Python','C++','Java','Unix']
    teachers = ['Python Rao','Chellam Rao','Java Rao','Unix Rao']
    ratings = [5,4,3,2]
    ids = [1,2,3,4]

    headers=['course_id','name','Teacher','Rating']
    for i,v in enumerate(zip(ids,courses,teachers,ratings)):
        master_list.append(dict(zip(headers,v)))

    return master_list

#REST API Related Code
from flask import Flask,jsonify

name='courses_rest_api'
app = Flask(name)  #Keeping the server name as file name

courses = get_courses()

#with app.route() , we create a custom URL with supported methods
@app.route('/')   # With this, I am routing to index page
def index():      # Making the index page for server
    #http://127.0.0.1:5000/   --> this is the index page.We are decorating this.

    return "Welcome to the Course api"


#Creating a custom URL to fetch all the courses available ,with GET method
@app.route('/courses/',methods=['GET'])  # With this, I am routing to courses page
#If you are creating URL like "course/<something>" , then all the parent URLs have to be "/course/" , '/course' <without ending /> will not work.
def get_courses():
    #http://127.0.0.1:5000/courses/ -> This is the courses page,We are decorating the GET method here

    return jsonify( {'Courses Available':courses} ) # sending the courses variable in a dictionary format mapped to name 'Courses'


#Creating a custom URL to fetch a particular course, by providing an index id , with GET method
@app.route('/courses/<int:ind_list_courses>' ,methods=['GET']) #-> With this, I am routing to courses page followed by an index tag
def get_course_via_id(ind_list_courses):   #decorator variable and function parameter should be same
    #http://127.0.0.1:5000/courses/1 -> This is the corresponding page for index 1 of course_list

    return jsonify( {'Requested Course via index':courses[ind_list_courses]} ) # courses is a list,we are fetching the item from provided index


#Creating a custom URL to add a new course ,with POST method, curl tool needed 
@app.route('/courses/add',methods=['POST'])  #-> With this, I am routing to "Add Course" page
def add_course():
    #http://127.0.0.1:5000/courses/ -> This is the courses page,We will observe the output here
    #curl -i -H "Content-Type: Application/json" -X POST http://127.0.0.1:5000/courses/add
    #run curl command and see courses page again
    
    course = {'course_id': 5, 'name': 'Perl', 'Teacher': 'Perl Rao', 'Rating': 1}
    courses.append(course)
    return jsonify( {'Course Created':course} ) # sending the courses variable in a dictionary format mapped to name 'Courses'


#Creating a custom URL to update Teacher of existing course ,with PUT method, curl tool needed 
@app.route('/courses/update/<int:ind_upd_courses>',methods=['PUT'])  #-> With this, I am routing to "Update Course" page
def update_course(ind_upd_courses):
    #http://127.0.0.1:5000/courses/ -> This is the courses page,We will observe the output here
    #curl -i -H "Content-Type: Application/json" -X PUT http://127.0.0.1:5000/courses/update/2
    #run curl command and see courses page again
    
    courses[ind_upd_courses]['Teacher'] = 'Amrit Rao'
    return jsonify( {'Course Updated':courses[ind_upd_courses]} ) # Updating the Teacher for provided index and displaying the updated course


#Creating a custom URL to Delete a course ,with DELETE method, curl tool needed
@app.route('/courses/delete/<int:ind_del_courses>',methods=['DELETE'])
def delete_course(ind_del_courses):
    #http://127.0.0.1:5000/courses/ -> This is the courses page,We will observe the output here
    #curl -i -H "Content-Type: Application/json" -X DELETE http://127.0.0.1:5000/courses/delete/2
    #run curl command and see courses page again

    deleted_course = courses.pop(ind_del_courses)
    return jsonify( {'Course Deleted':deleted_course} ) # Deleting the course for provided index and displaying that deleted course


#main function
if __name__=='__main__':
    #app.run(debug=True) --> is the dafault , but we can custom as below
    app.run(host="127.0.0.1", port=5000, threaded=True,debug=True)
