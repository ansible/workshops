# Validating Network State

We can also automate checking the results.  Using the [eos_command](http://docs.ansible.com/ansible/latest/eos_command_module.html) to ping the loopback addresses of each switch, and then using the [assert module](http://docs.ansible.com/ansible/latest/assert_module.html) we can make sure we have full reachability.  Check out the following playbook:

We can simply ping each loopback address
```yaml
- name: CHECK CONNECTIVITY
  hosts: network
  tasks:
    - name: Test reachability from all devices to all devices
      eos_command:
        commands:
          - "ping 172.16.0.1"
          - "ping 172.16.0.2"
          - "ping 172.16.0.3"
          - "ping 172.16.0.4"
      register: ping_result
```

Then we want to check the results using the assert module.  Remember that since we issued 4 commands, we will have a list of 4 results.  Our list will be numbered from stdout[0] through stdout[3] since computers start counting from 0.

```
    - name: assert test results
      assert:
        that:
          - "'172.16.0.1' in ping_result.stdout[0]"
          - "' 0% packet loss' in ping_result.stdout[0]"
          - "'172.16.0.2' in ping_result.stdout[1]"
          - "' 0% packet loss' in ping_result.stdout[1]"
          - "'172.16.0.3' in ping_result.stdout[2]"
          - "' 0% packet loss' in ping_result.stdout[2]"
          - "'172.16.0.4' in ping_result.stdout[3]"
          - "' 0% packet loss' in ping_result.stdout[3]"
```

To run the playbook use the `ansible-playbook` command.  

```
[vagrant@ansible linklight]$ ansible-playbook assert.yml
```

The full playbook is provided here [validate.yml](validate.yml)

## Complete
You have completed Exercise 03.

[Return to training-course](../README.md)
