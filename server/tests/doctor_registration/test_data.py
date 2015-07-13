from datetime import date

current_date = date.today()
DATE_FORMAT = '%Y-%m-%d'

TEST_EXPECTED_RETURN_DOCTOR = {
    'id':1,
    'doctors_name':'Frankenstein',
    'work_hours':9999,
    'registration_date':current_date.strftime(DATE_FORMAT)
}

TEST_EXPECTED_RETURN_SPECIALIST = {
    'id':1,
    'specialist_name':'death'
}

INITIALIZE_DOCTOR_REGISTATION = [
    {
        'doctors_name':'David Parr',
        'specialist_name':'awesome doc',
        'work_hours':40
    },
    {
        'doctors_name':'Felicia Parr',
        'specialist_name':'nerd',
        'work_hours':5
    },
    {
        'doctors_name':'Dr. Mario',
        'specialist_name':'Infectious Disease Specialist',
        'work_hours': 999
    },
    {
        'doctors_name':'Dr. Luigi',
        'specialist_name':'Infectious Disease Specialist',
        'work_hours':999
    }

]

TEST_REGISTER_DOCTOR_FRANK = {
    'doctors_name':'Frankenstein',
    'specialist_name':'death',
    'work_hours': 9999
}

TEST_DUBLICATE_REGISTER_DOCTOR_MARIO = {
    'doctors_name':'Dr. Mario',
    'specialist_name':'Infectious Disease Specialist',
    'work_hours': 999
}


ENDPOINTS = {
    'home':'/doctor_registration/',
    'add_doctor':'/doctor_registration/create/'
}
