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

$hostname = Get-AnsibleParam -obj $params -name "hostname" -type "str" -failifempty $true
$zone = Get-AnsibleParam -obj $params -name "zone" -type "str" -failifempty $true
$ipaddr = Get-AnsibleParam -obj $params -name "ipaddr" -type "str" -default ""
$timetolive = Get-AnsibleParam -obj $params -name "timetolive" -type "str" -default "01:00:00"
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

if ($state -eq 'present' -and $ipaddr -eq "") {
    Fail-Json $result "ipaddr can not be blank if state = present"
}

try {
    $exists = Get-DnsServerResourceRecord -ZoneName $zone -Name $hostname -ErrorAction SilentlyContinue
    if ($state -eq 'present') {
        if ($exists) {
            $ip = $exists.RecordData.IPv4Address.IPAddressToString
            # Check if we need to update the Entry
            if ($ip -ne $ipaddr) {
                if (-not $check_mode) {
                    Remove-DnsServerResourceRecord -ZoneName $zone -RRType "A" -Name $hostname -Force
                    Add-DnsServerResourceRecordA -Name "$hostname"    `
                            -ZoneName "$zone" `
                            -IPv4Address "$ipaddr" `
                            -AllowUpdateAny `
                            -AgeRecord `
                            -TimeToLive $timetolive
                }
                $result.changed = $true
                $result.msg = "DNS A Record: Updated: ($ip) >> ($ipaddr)"
            } else {
                # Record exists and doesn't need to be updated
                $result.msg = "DNS A Record: Present: $hostname ($ipaddr)"
            }
        } else {
            if (-not $check_mode) {
                Add-DnsServerResourceRecordA -Name "$hostname"    `
                        -ZoneName "$zone" `
                        -IPv4Address "$ipaddr" `
                        -AllowUpdateAny `
                        -AgeRecord `
                        -TimeToLive $timetolive
            }
            $result.changed = $true
            $result.msg = "DNS A Record: Added: $hostname ($ipaddr)"
        }
    } else {
        if ($exists) {
            if (-not $check_mode) {
                Remove-DnsServerResourceRecord -ZoneName $zone -RRType "A" -Name $hostname -Force
            }
            $result.changed = $true
            $result.msg = "DNS A Record: Removed: $hostname ($ipaddr)"
        } else {
            $result.msg = "DNS A Record: Absent: $hostname ($ipaddr)"
        }
    }
}
catch {
    Fail-Json $result $_.Exception.Message
}

Exit-Json $result