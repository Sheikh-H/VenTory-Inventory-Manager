# def input_validator(data, form):
#     forbidden_charcaters = ["<", ">", "{", "}", "[", "]"]
#     new_user_fields = {
#         "title",
#         "fname",
#         "sname",
#         "email",
#         "role",
#         "password",
#         "confirm",
#     }
#     new_business_fields = {"name", "address", "telephone", "email"}

#     if form == "new business":
#         for section, fields in data.items():
#             for key, value in fields.items():
#                 for char in value:
#                     if char in forbidden_charcaters:
#                         return False, "Malicious data detected, please use valid entries!"

#             if section == "business":
#                 for key, value in data.items():
#                     if key not in new_business_fields:
#                         return False, "Please use form fields only!"
#                     if key == 'name':


#             if section == "user":
#                 for key, value in data.items():
#                     if key not in new_user_fields:
#                         return False, "Please use form fields only!"

#             if fields['password'] != fields['confirm']:
#                 return False, 'Password mismatch, please enter your password again'

#             if len(fields['password']) < 15 or len(fields['confirm']) < 15:
#                 return False, "Passswords must be more than 15 characters"


#     return True, None
