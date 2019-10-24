from widgets.EyeBlink.EyeBlink import EyeBlink
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import config

config.reset_filter_states()
mod = EyeBlink('./test_data',name="SingleBlinks",trails=60)
mod.run_browser()
print("READY")
mod.run_real_time()
