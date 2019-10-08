import session
from widgets import ENG

session.create_user('raghav')
session.delete_user('raghav')
session.create_user('raghav')
session.add_widget('raghav','eng')

widget_path = session.check_widget('raghav','eng')
eng = ENG(widget_path,20)
eng.run()
