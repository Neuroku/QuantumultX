import re
import ipaddress

# 定义优先级
PRIORITY_ORDER = {
    "host-keyword": 0,
    "host-suffix": 1,
    "host": 2,
    "ip-asn": 3,
    "ip-cidr": 4,
    "ip6-cidr": 5,
}


def remove_duplicates(rules):
    return list(set(rules))


def is_subdomain(domain1, domain2):
    return domain1.endswith("." + domain2)


def sort_rules(rules):
    # 按照优先级和域名字典顺序排序
    return sorted(rules, key=lambda rule: (
        PRIORITY_ORDER.get(rule.split(', ')[0], 100),  # 根据类型的优先级排序
        rule.split(', ')[1]  # 按照域名的字典顺序排序
    ))


def optimize_rules(rule_blocks, deleted_log_file):
    optimized_blocks = []

    with open(deleted_log_file, 'w') as log_file:
        for block in rule_blocks:
            header = block['header']
            rules = block['rules']

            # 先排序规则
            rules = sort_rules(rules)

            optimized_rules = []
            rules = remove_duplicates(rules)

            host_keyword_rules = [rule for rule in rules if rule.split(', ')[0] == "host-keyword"]

            # 首先检查所有 host-keyword 规则之间是否有包含关系
            for i, keyword_rule in enumerate(host_keyword_rules):
                keyword = keyword_rule.split(', ')[1].strip()
                for j, other_keyword_rule in enumerate(host_keyword_rules):
                    if i != j and keyword in other_keyword_rule.split(', ')[1]:
                        log_file.write(
                            f"Rule '{keyword_rule}' is redundant and removed due to being contained within '{other_keyword_rule}'.\n")
                        rules.remove(keyword_rule)
                        break

            for rule in rules:
                try:
                    rule_type, domain, action = [item.strip() for item in rule.split(',')]
                except ValueError:
                    log_file.write(f"Skipping invalid rule format: {rule}\n")
                    continue

                redundant = False

                # 如果存在 host-keyword 规则，检查当前规则是否被 host-keyword 包含
                for host_keyword_rule in host_keyword_rules:
                    keyword = host_keyword_rule.split(', ')[1].strip()
                    if keyword in domain and rule != host_keyword_rule:  # 确保不删除自己
                        log_file.write(
                            f"Rule '{rule}' is redundant and removed due to being contained within '{host_keyword_rule}'.\n")
                        redundant = True
                        break

                if redundant:
                    continue

                for opt_rule in optimized_rules:
                    opt_type, opt_domain, opt_action = [item.strip() for item in opt_rule.split(',')]

                    # # IP CIDR 包含逻辑优化
                    # if rule_type.startswith("ip") and opt_type.startswith("ip"):
                    #     try:
                    #         ip_net = ipaddress.ip_network(domain)
                    #         opt_ip_net = ipaddress.ip_network(opt_domain)
                    #
                    #         if opt_ip_net.supernet_of(ip_net):
                    #             log_file.write(
                    #                 f"Rule '{rule}' is redundant and removed due to being contained within '{opt_rule}'.\n")
                    #             redundant = True
                    #             break
                    #         elif ip_net.supernet_of(opt_ip_net):
                    #             log_file.write(
                    #                 f"Rule '{opt_rule}' is redundant and removed due to being contained within '{rule}'.\n")
                    #             optimized_rules.remove(opt_rule)
                    #             continue
                    #
                    #     except ValueError:
                    #         continue

                    # Host 规则优化逻辑
                    if (rule_type == "host" and opt_type == "host-suffix") or \
                            (rule_type == "host-suffix" and opt_type == "host") or \
                            (rule_type == opt_type and (rule_type.startswith("host"))):

                        if is_subdomain(domain, opt_domain):
                            log_file.write(
                                f"Rule '{rule}' is redundant and removed due to being contained within '{opt_rule}'.\n")
                            redundant = True
                            break
                        elif is_subdomain(opt_domain, domain):
                            log_file.write(
                                f"Rule '{opt_rule}' is redundant and removed due to being contained within '{rule}'.\n")
                            optimized_rules.remove(opt_rule)
                            continue

                if not redundant:
                    optimized_rules.append(rule)

            optimized_blocks.append({
                'header': header,
                'rules': optimized_rules
            })

    return optimized_blocks


def read_rules_from_file(filename):
    rule_blocks = []
    current_block = {'header': None, 'rules': []}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                # Save the previous block and start a new one
                if current_block['header'] is not None:
                    rule_blocks.append(current_block)
                current_block = {'header': line, 'rules': []}
            elif line:
                current_block['rules'].append(line)

        # Add the last block
        if current_block['header'] is not None:
            rule_blocks.append(current_block)

    return rule_blocks


def write_rules_to_file(filename, rule_blocks):
    with open(filename, 'w') as f:
        for block in rule_blocks:
            f.write(f"{block['header']}\n")
            sorted_rules = sort_rules(block['rules'])  # 确保输出时再按顺序排序
            for rule in sorted_rules:
                f.write(f"{rule}\n")
            f.write("\n")  # Add a newline between rule blocks


if __name__ == "__main__":
    input_filename = "/home/kechang/Project/domainCheck/rule"
    output_filename = "/home/kechang/Project/domainCheck/out_rule"
    deleted_log_filename = "/home/kechang/Project/domainCheck/deleted_rule"

    # 读取规则文件
    rule_blocks = read_rules_from_file(input_filename)

    # 执行规则优化并将日志输出到文件
    if rule_blocks:
        optimized_rule_blocks = optimize_rules(rule_blocks, deleted_log_filename)

        # 写入优化后的规则到输出文件
        write_rules_to_file(output_filename, optimized_rule_blocks)

        print(f"Optimized rules have been written to {output_filename}.")
        print(f"Deleted rules have been logged in {deleted_log_filename}.")
    else:
        print(f"Error: No rules found in the file '{input_filename}'.")