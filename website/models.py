from pymongo import MongoClient

client = MongoClient("mongodb+srv://laundryService:1GgWU0SRJgMDVdnP@mydatabase.xwidf.mongodb.net/?retryWrites=true&w=majority")

db = client['test']

# schema_validators = {
#    "$jsonSchema" : {
#                "bsonType": "object",
#                "required": ["name","email","password"],
#                "properties": {
#                   "name": {
#                      "bsonType": "string",
#                      "description": "must be a string and is required"
#                   },
#                   "email": {
#                      "bsonType": "string",
#                      "description": "must be a string"
#                   },
#                   "password": {
#                      "bsonType": "binData",
#                      "description": "must be a string "
#                   }
#                }
               
#             }
# }

schema_validators_for_employees = {
   "$jsonSchema" : {
               "bsonType": "object",
               "required": ["Emp_id","Name","Email","Phone","Dob","Salary","Designation"],
               "properties": {
                  "Emp_id": {
                     "bsonType": "string",
                     "description": "must be a string of 16 chars and is required"
                  },
                  "Name": {
                     "bsonType": "string",
                     "minimum": "3",
                     "maximum": "50",
                     "description": "must be a string and is required"
                  },
                  "Email": {
                     "bsonType": "regex",
                     "description": "must be a string"
                  },
                  "Phone": {
                     "bsonType": "int",
                     "minimum": "10",
                     "maximum": "10",
                     "description": "must be a string "
                  },
                  "Dob":{
                     "bsonType": "date",
                     "description": "must be a date object",
                  },
                  "Salary": {
                     "bsonType": "float",
                     "description": "must be a float",
                  },
                  "Designation": {
                     "bsonType": "string",
                     "description": "must be a string and   is required",
                  },
               }
               
            }
}

try:
   # db.create_collection("admin",validator=schema_validators)
   db.create_collection("admin2")
   db.create_collection("employeeDetails",validator= schema_validators_for_employees)
except Exception as e:
   print(e)


# db.command("callMod",validator=schema_validators)
adminCol = db["admin2"]
# adminCol = db["employeeDetails"]
employeeCol = db["employeeDetails"]


