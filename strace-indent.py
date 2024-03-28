#!/usr/bin/env python3

def indent_string(level: int) -> str:
    return level * "  "

def indent_line(line: str) -> str:
    new_line = ""
    indent_level = 0

    it = iter(line)

    while True:
        c = next(it, None)
        if c == None:
            break

        if c in "[{(":
            indent_level += 1
            new_line += c
            new_line += "\n" + indent_string(indent_level)
        elif c in "]})":
            indent_level -= 1
            new_line += "\n" + indent_string(indent_level)
            new_line += c
        elif c == ",":
            new_line += c
            new_line += "\n" + indent_string(indent_level)
        elif c == " ":
            continue
        elif c == "=":
            new_line += " = "
        elif c == "\"":
            new_line += c
            while True:
                c = next(it, "\"")

                new_line += c
                if c == "\"":
                    break

        else:
            new_line += c

    return new_line

print(indent_line('sendmsg(4, {msg_name={sa_family=AF_NETLINK, nl_pid=0, nl_groups=00000000}, msg_namelen=12, msg_iov=[{iov_base=[{nlmsg_len=52, nlmsg_type=RTM_GETLINK, nlmsg_flags=NLM_F_REQUEST, nlmsg_seq=1711641587, nlmsg_pid=0}, {ifi_family=AF_UNSPEC, ifi_type=ARPHRD_NETROM, ifi_index=0, ifi_flags=0, ifi_change=0}, [[{nla_len=8, nla_type=IFLA_EXT_MASK}, RTEXT_FILTER_VF|RTEXT_FILTER_SKIP_STATS], [{nla_len=11, nla_type=IFLA_IFNAME}, "wlp2s0"]]], iov_len=52}], msg_iovlen=1, msg_controllen=0, msg_flags=0}, 0) = 52'))
