# ThriftUStore_Users
 
### Admin user account:
Username: zz3105@columbia.edu <br>
Password: zz3105

### Google Oauth url 
https://user-microservice-402518.ue.r.appspot.com/users/google/login/

### Command to deploy to the google app engine:
``gcloud app deploy ``

### Before deployment Checklist:



1. Change ``settings.py`` file:
   - Set ``SITE_ID = 2`` to enable google oauth2.
   - Set ``os.environ['SMARTY_WEBSITE_DOMAIN'] = "user-microservice-402518.ue.r.appspot.com"`` to enable external address check api.

2. After updating the local database, you need to connect to the cloud database and do migration as well.
3. Before testing the API gateway, make sure the IAP is turned on, but once turned on, only restricted user can access the api
4. hello function
   - Set