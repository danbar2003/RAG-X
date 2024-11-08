# RAG-X

KEY=put-your-key python3 main.py /home/loani/projects/google-ctf-main/2021/quals/pwn-tridroid/ flag

# Result

```
Name: method_desc_heap_address
Type: variable
File Path: /home/loani/projects/google-ctf-main/2021/quals/pwn-tridroid/challenge/exploit/exploit.py
Snippet:
bridge.manageStack(password, 'push', hex('showFlag'));
        method_name_heap_address = leak_top_element_address();
        bridge.manageStack(password, 'push', hex('()V'));
        method_desc_heap_address = leak_top_element_address();

        // leak stack addresses
        bridge.manageStack(password, 'push', '');

====================================================================================================
Name: stack_ret_address
Type: variable
File Path: /home/loani/projects/google-ctf-main/2021/quals/pwn-tridroid/challenge/exploit/exploit.py
Snippet:
bridge.manageStack(password, 'push', '');
        bridge.manageStack(password, 'modify', '');
        stack_canary_address = unpack(unhex(bridge.manageStack(password, 'top', '')));
        stack_ret_address = stack_canary_address + 0x8;
        bridge.manageStack(password, 'pop', '');

        // leak stack canary on the stack

====================================================================================================
```
