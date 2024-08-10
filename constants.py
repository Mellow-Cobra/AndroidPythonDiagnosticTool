
NOT_AVAILABLE = "not available"
MHZ = "MHz"
CELSIUS = "Celsius"


# Platform
LINUX = 'Linux'
WIN = 'Windows'

# Results
PASS = 'pass'
FAIL = 'fail'



# CPU Diagnostic Limits
MAX_TEMPERATURE_LIMIT_C = 75.0
MIN_TEMPERATURE_LIMIT = 18.0
CPU_THROTTLE_OT = "cpu_throttle_overtemp"
CPU_NO_THROTTLE = "cpu_no_throttle"
CPU_TEMP_SAFE = "cpu_temperature_safe"
HIGH_FREQUENCY = "high_frequency"
LOW_FREQUENCY = "low_frequency"
CPU_IN_SPEC = "cpu_in_frequency_bound"
CPU_FREQ_NOT_IN_SPEC = "cpu_frequency_out_of_bound"
CPU_TEMPERATURE_DIAGNOSTIC_HEADER = ['CPU', 'MAX_TEMPERATURE_LIMIT_C', 'TEMPERATURE_READOUT', 'MIN_TEMPERATURE_LIMIT_C',
                                     'UNITS', 'DIAGNOSTIC_STATUS', 'DIAGNOSTIC_TEST_RESULT']
CPU_FREQUENCY_DIAGNOSTIC_HEADER = ['CPU', 'MIN_FREQUENCY', 'FREQUENCY_READOUT', 'MAX_FREQUENCY', 'UNITS',
                                   'DIAGNOSTIC_STATUS', 'DIAGNOSTIC_TEST_RESULT']

