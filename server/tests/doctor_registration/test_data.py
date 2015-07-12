from datetime import date

current_date = date.today()
DATE_FORMAT = '%Y-%m-%d'

ENDPOINTS = {
    'home':'/doctor_registration/'
}

TEST_REGISTER_DOCTOR = {
    'doctors_name':'Frankenstein',
    'specialist_name':'death',
    'work_hours': 9999
}

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


REGISTER_DOCTOR_RETURN_ATTRIBUTES = [
    'doctors_name',
    'specialist_name',
    'work_hours',
    'registration_date'
]
