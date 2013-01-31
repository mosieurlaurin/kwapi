# -*- coding: utf-8 -*-
#
# Author: François Rossigneux <francois.rossigneux@inria.fr>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import subprocess
import time

from driver import Driver


class Ipmi(Driver):
    """Driver for IPMI cards."""

    def __init__(self, probe_ids, **kwargs):
        """Initializes the IPMI driver.

        Keyword arguments:
        probe_ids -- list containing the probes IDs
                     (a wattmeter monitor sometimes several probes)
        kwargs -- keyword (device) defining the device to read (/dev/ttyUSB0)

        """
        Driver.__init__(self, probe_ids, kwargs)

    def run(self):
        """Starts the driver thread."""
        while not self.stop_request_pending():
            measurements = {}
            measurements['w'] = self.get_watts()
            self.send_measurements(self.probe_ids[0], measurements)
            time.sleep(1)

    def get_watts(self):
        """Returns the power consumption."""
        command = 'ipmitool '
        command += '-S ' + kwargs.get('cache_file') + ' '
        command += '-I ' + kwargs.get('interface') + ' '
        command += '-H ' + kwargs.get('host') + ' '
        command += '-U ' + kwargs.get('username', 'root') + ' '
        command += '-P ' + kwargs.get('password') + ' '
        command += 'sensor reading "System Level" | cut -f2 -d"|"'
        output, error = subprocess.Popen(command,
                                         shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT
                                         ).communicate()
        return int(output)
