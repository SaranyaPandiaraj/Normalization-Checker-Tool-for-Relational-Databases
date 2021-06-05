######################### Normalization Checker Tool For Relational Databases #############################

#### Pre-Requisite #####

Tools to install : Python, MySQL, Google Chrome

#### Install the below Import Modules for Python from the python terminal

>>  pip install <module_name>
>> (For example pip install flask)

(flask, sys, mysql.connector, tabulate, os, csv, io, pandas, numpy, IPython.display, HTML, IPython.display, Decomp,re,itertools, functools)

#### How to Run the Program

>> First Download the Project Code Folder in your system.

>> Navigate to Project Code Folder from your terminal

>> Go to the respective location where app.py file is present   
   (For Example : cd /Users/sara/Desktop/SJSU/Data 225/Project Code)

>> Run the below command in the terminal

   python app.py

Once you run the above command, you should get something like below in the terminal :

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 156-589-807


>> Navigate to the Google Chrome Browser and type the below server link and press enter

http://127.0.0.1:5000/

>> The Normalization Checker Tool will display in the browser

The tool has a Readme Section which will tell you how to use the Tool.

#### Folder Structure

### Static Folder

Static Folder contains the below folders

** CSS -  Contains cascading styling sheet files 
** Files - Contains the Input Files
** Images - Contains HTML Images & Slides Images
** Output - Contains the Output files

### Templates Folder

The HTML files are placed in the templates folder.

For each section in the tool, a separate HTML is created where the inputs are entered 
and outputs are generated based on the inputs provided.



