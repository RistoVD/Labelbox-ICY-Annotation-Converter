import labelbox
import configparser

# Read from configfile.ini
config_object = configparser.ConfigParser()
config_object.read('configfile.ini')
data = config_object['Data']
project_key = data['project']
password = data['api-key']
start_date = data['start_date']
end_date = data['end_date']

# import a list of labels
lb = labelbox.Client(api_key=password)
project = lb.get_project(project_key)
labels = project.export_labels(download=True, start=start_date, end=end_date)





