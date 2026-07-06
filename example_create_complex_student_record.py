from appian_locust import AppianTaskSet
from locust import HttpUser, task
from datetime import date, timedelta
import random

from appian_locust.utilities import loadDriverUtils

utls = loadDriverUtils()
utls.load_config()


class RecordsTaskSet(AppianTaskSet):

    first_name_array = ["Albert", "Antonio", "Ben", "Chris", "Cole", "Dayton", "Greg", "Lamar", "Mitchell", "Peter", "Richard", "Steven", "Tim", "William"]
    last_name_array = ["Smith","Johnson","Williams","Jones","Brown","Davis","Miller","Wilson","Moore","Taylor"]
    college_array = ["University of Alabama", "Cornell", "University of Maryland", "Virginia Tech", "Harvard", "University of Michigan", "Marquette", "Boise State", "University of Indiana", "Texas Tech"]
    subject_array = ["Biology", "Chemistry", "Calculus", "Physics", "Literature", "Engineering", "Philosophy"]
    num_choices = 6

    

    START_DATE = date(1990,1,1)
    END_DATE = date(2007,12,31)

    def generate_random_date(self):
        time_between_dates = self.END_DATE - self.START_DATE
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = self.START_DATE + timedelta(days=random_number_of_days)
        return random_date
                     

    @task(2)
    def create_new_student(self):

        #Generate a random birthday
        random_birthday = self.generate_random_date()

        # Navigate to Student Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Students")

        # Click on "New Student" Record List Action
        record_list_uiform.click_record_list_action(label="New Student")

        # Fill in new Student information with randomized values
        record_list_uiform.fill_text_field(label="First Name", value = random.choice(self.first_name_array))
        record_list_uiform.fill_text_field(label="Last Name", value = random.choice(self.last_name_array))

        record_list_uiform.fill_text_field(label="University/College", value = random.choice(self.college_array))
        record_list_uiform.select_dropdown_item(label="Favorite Subject", choice_label = random.choice(self.subject_array))

        record_list_uiform.fill_date_field(label="Birthday", date_input = random_birthday)
        record_list_uiform.select_radio_button_by_label(label="Favorite Food", index = random.randrange(self.num_choices))

        # Create Student!
        try:
            record_list_uiform.click_button(label="Create")

        except Exception as e:
            print(e)

    

    @task(1)
    def get_admin_page(self):
        self.appian.visitor.visit_admin("AdminConsoleUI")


class UserActor(HttpUser):
    tasks = [RecordsTaskSet]
    config = utls.c
    auth = config['auth']
    host = "https://" + config['host_address']




    


    



