Post_data_fileds  = ['title', 'description']
stringcheck = r"^[a-z]{5,20}$"
pass_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
field_regex = r"(.|\s)*\S(.|\s)*"
mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,5}\b'
data_fields = ['first_name', 'gender', 'birth_date','email', 'phone_no', 'address' , 'password', 'confirm_password']
