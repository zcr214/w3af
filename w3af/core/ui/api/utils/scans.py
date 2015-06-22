"""
scans.py

Copyright 2015 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
from w3af.core.ui.api.db.master import SCANS, ScanInfo
from w3af.core.controllers.w3afCore import w3afCore


def get_scan_info_from_id(scan_id):
    return SCANS.get(scan_id, None)


def get_new_scan_id():
    return len(SCANS.keys())


def create_temp_profile(scan_profile):
    """
    Writes the scan_profile to a file

    :param scan_profile: The contents of a profile configuration
    :return: The scan profile file name and the directory where it was created
    """
    raise NotImplementedError


def start_scan_helper(target_urls, scan_profile):
    """
    Create a new instance of w3afCore, save it to SCANS and run core.start()

    :param scan_profile: The contents of a profile configuration
    :return: The instance of w3afCore.
    """
    scan_profile_file_name, profile_path = create_temp_profile(scan_profile)

    scan_info = ScanInfo()
    SCANS[get_new_scan_id()] = scan_info
    scan_info.w3af_core = w3af_core = w3afCore()
    scan_info.target_urls = target_urls

    try:
        target_options = w3af_core.target.get_options()
        target_option = target_options['target']
        
        target_option.set_value(target_urls)
        w3af_core.target.set_options(target_options)

        w3af_core.profiles.use_profile(scan_profile_file_name,
                                       workdir=profile_path)
        w3af_core.plugins.init_plugins()
        w3af_core.verify_environment()
        w3af_core.start()
    except Exception, e:
        scan_info.exception = e
        w3af_core.stop()
    finally:
        scan_info.finished = True

