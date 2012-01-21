from campaign_status_controller import *
from person_controller import *
from donation_controller import *
         
purser  =    [
                    ('/campaign/([^/]+)?', CampaignStatusController),
                    ('/person', PersonController),
                    ('/donation', DonationController),
             ]
