from widgets.EyeBlink.EyeBlink import EyeBlink
import config

config.reset_filter_states()
mod = EyeBlink('./jaja')
mod.run_real_time()
