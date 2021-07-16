class UnauthorizedError(Exception):
    pass

class InvalidFileNameError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass
    
errors = {
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
    },

    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "InvalidPasswordError": {
        "message": "Invalid password or email. Change password",
        "status": 401
    },
    "InvalidFileNameError": {
        "message": "Invalid file name error",
        "status": 400
    }
#    "InternalServerError": {
#        "message": "Something went wrong",
#        "status": 500
#    },
#    "EmailorNameAlreadyExistsError": {
#        "message": "User with given email or name address already exists",
#        "status": 400
#    },
  
}
