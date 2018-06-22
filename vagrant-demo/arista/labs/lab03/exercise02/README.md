# Exercise 02 - Configuring OSPF Routing

For this exercise we are going to configure [OSPF routing](https://en.wikipedia.org/wiki/Open_Shortest_Path_First) using the [eos_config](http://docs.ansible.com/ansible/latest/eos_config_module.html) module.  We are going to put every interface into area 0.

## Modify the template to add ospf

First we need to add the OSPF commands `ip ospf area 0.0.0.0` and `ip network point-to-point` at the interface level.  We can simply add these commands into our loop:

```
{% for interface in nodes[inventory_hostname] -%}
interface {{interface}}
{% if "Loopback" not in interface %}
    no switchport
    ip ospf network point-to-point
    ip ospf area 0.0.0.0
{% endif %}
    ip address {{nodes[inventory_hostname][interface]}}
{% endfor %}
```

We also need to enable `ip routing`, configure the OSPF process itself, the `router-id`, and advertise the Loopback address into OSPF. We want to use the loopback address as the router-id, but we need to remove the subnet (`/32`).  We can do this a variety of ways, but one of the best ways is to take advantage of the ipaddr filter.  There is [documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters_ipaddr.html) and a [variety of examples](https://github.com/network-automation/ipaddr_filter) but for our case we want to use `ipaddr("address")` which will cut off the subnet:

```
{{"172.16.0.1/32" | ipaddr("address")}}
```
would generate `172.16.0.1`

Lets append the following to our template.
```
!
ip routing
!
router ospf 1
    router-id {{ nodes[inventory_hostname].Loopback1 | ipaddr("address") }}
    network {{nodes[inventory_hostname].Loopback1}} area 0.0.0.0
```

The full template is provided here: [ospf.j2](ospf.j2)

# Looking at the results

Use the `show ip ospf neigh` command to look for OSPF neighborship adjacencies

```
leaf01#show ip ospf neigh
Neighbor ID     VRF      Pri State                  Dead Time   Address         Interface
172.16.0.2      default  0   FULL                   00:00:30    172.16.200.17   Ethernet3
172.16.0.1      default  0   FULL                   00:00:29    172.16.200.1    Ethernet2
```

Check the route table with the `show ip route` command.  There should be a route for 172.16.0.1, 172.16.0.2, 172.16.0.3 and 172.16.0.4 which represent the 4 devices:

```
leaf01#show ip route

VRF: default
Codes: C - connected, S - static, K - kernel,
       O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
       E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
       N2 - OSPF NSSA external type2, B I - iBGP, B E - eBGP,
       R - RIP, I L1 - IS-IS level 1, I L2 - IS-IS level 2,
       O3 - OSPFv3, A B - BGP Aggregate, A O - OSPF Summary,
       NG - Nexthop Group Static Route, V - VXLAN Control Service,
       DH - Dhcp client installed default route

Gateway of last resort is not set

 C      10.0.2.0/24 is directly connected, Management1
 O      172.16.0.1/32 [110/20] via 172.16.200.1, Ethernet2
 O      172.16.0.2/32 [110/20] via 172.16.200.17, Ethernet3
 C      172.16.0.3/32 is directly connected, Loopback1
 O      172.16.0.4/32 [110/30] via 172.16.200.1, Ethernet2
                               via 172.16.200.17, Ethernet3
 C      172.16.200.0/30 is directly connected, Ethernet2
 O      172.16.200.4/30 [110/20] via 172.16.200.1, Ethernet2
 C      172.16.200.16/30 is directly connected, Ethernet3
 O      172.16.200.20/30 [110/20] via 172.16.200.17, Ethernet3
 C      192.168.0.0/24 is directly connected, Ethernet1
```

## Complete
You have completed Exercise 02.

[Return to training-course](../README.md)
