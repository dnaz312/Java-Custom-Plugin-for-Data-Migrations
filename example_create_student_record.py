from appian_locust import AppianTaskSet
from locust import HttpUser, task
from datetime import date
import urllib3

from appian_locust.utilities import loadDriverUtils

utls = loadDriverUtils()
utls.load_config()

urllib3.disable_warnings()
 
 
class GetReportsTaskSet(AppianTaskSet):
    @task
    def visit_reports(self):
        ui_form = self.appian.visitor.visit_site(site_name = "ai-testing", page_name = "selection-navigation")

        # click button
        ui_form.click_card_layout_by_index(1)
        # click back button
        ui_form.click(label = "Back")



class UserActor(HttpUser):
    tasks = [GetReportsTaskSet]
    config = utls.c
    auth = config['auth']
    host = "https://" + config['host_address']
    
