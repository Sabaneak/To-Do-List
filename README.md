# To-Do List
This Flask RESTful-API is utilised for the very simple yet essential requirements to manage our tasks in an efficient manner.  

## Features:
These are the simple features the API provides for user convenience:  
1. __User Sign-In and Login__ : This Flask-RESTful API ensures user security and privacy. Upon registering, a confirmation email will be sent to your email address. Upon clicking the link, your credentials will be registered and you can use the app.  
2.__Secure features__: All endpoints require a JWT token, ensuring the API can not be accesed unless you have logged in and subsequently, logged out.  
3.__List of Users by ID__: A user may view the details of another user by ID. Passwords however, are not displayed.  
4.__Refresh tokens__: Certain features such as deleting tasks are locked and require you to refresh your token to access.  
5.__Creating tasks__: Tasks can be created with fields: Name, Category and Status.  
6.__Editing and Deleting tasks__: Tasks can be changed from pending to completed or non-important to important based on Name of Task.  
7.__Displaying tasks__: Individual tasks can be displayed based on name, as well as comprehensive list of tasks with two seperate endpoints.  

##List of Endpoints:
*__'/register'__  
*__'/user/<int:user_id>'__  
*__'/login'__  
*__'/logout'__  
*__'/refresh'__  
*__'/user_confirm/<int:user_id>'__  

*__'/tasks'__  
*__'/tasks/<string:name>'__   
    *Add  
    *Edit  
    *Delete  
*__'/tasks/all'__  

##Softwares used
The API was written using the Flask framework of Python.  
Mailing was performed with the help of MailGun.  
The API was tested with Postman.  
Some of the packages used include:  
*flask  
*requests  
*flask-restful  
*flask-jwt-extended  
*flask-cors  
*marshmallow  
*flask-sqlalchemy  
*flask-marshmallow  
*marshmallow-sqlalchemy  


       
