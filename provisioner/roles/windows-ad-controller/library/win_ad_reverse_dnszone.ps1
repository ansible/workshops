#!powershell
# This file is part of Ansible
#
# Copyright 2018, Jimmy Conner <jconner@redhat.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# WANT_JSON
# POWERSHELL_COMMON

$params = Parse-Args $args -supports_check_mode $true

$subnet = Get-AnsibleParam -obj $params -name "subnet" -type "str" -failifempty $true
$zonename = Get-AnsibleParam -obj $params -name "zonename" -type "str" -failifempty $true
$state = Get-AnsibleParam -obj $params -name "state" -type "str" -validateset "present","absent" -default "present"

$check_mode = Get-AnsibleParam -obj $params -name "_ansible_check_mode" -type "bool" -default $false

$result = @{
    changed = $false
    msg = ""
}

# Determine if AD Domain is setup
try {
    $domain = get-addomain
} catch {
    $errormsg = $_.Exception.Message
    Fail-Json $result "AD Domain not setup: $errormsg"
}

try {
    $exists = $false
    $zones = Get-DnsServerZone
    foreach ($zone in $zones) {
        if ($zone.ZoneName -eq $zonename) {
            $exists = $true
        }
    }

    if ($state -eq "present") {
        if ($exists) {
            # Record exists and doesn't need to be updated
            $result.msg = "DNS Zone: Present: $zonename"
        } else {
            if (-not $check_mode) {
                Add-DnsServerPrimaryZone -NetworkId "$subnet" -DynamicUpdate Secure -ReplicationScope Domain
            }
            $result.changed = $true
            $result.msg = "DNS Zone: Added: $zonename ($subnet)"
        }
    } else {
        if ($exists) {
            if (-not $check_mode) {
                Remove-DnsServerZone -Name "$zonename" -Force
            }
            $result.changed = $true
            $result.msg = "DNS Zone: Removed: $zonename"
        } else {
            $result.msg = "DNS Zone: Absent: $zonename"
        }
    }
} catch {
    Fail-Json $result $_.Exception.Message
}

Exit-Json $result