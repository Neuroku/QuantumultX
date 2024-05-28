function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || dnsDomainIs(host, ".local")) {
        return "DIRECT";
    }
    var directAddresses = [
//        { ip: "10.0.0.0", mask: "255.0.0.0" },
        { ip: "127.0.0.0", mask: "255.0.0.0" },
        { ip: "172.16.0.0", mask: "255.240.0.0" },
        { ip: "192.168.0.0", mask: "255.255.0.0" },
        { ip: "224.0.0.0", mask: "255.255.255.0" },
        { ip: "172.20.10.2", mask: "255.255.255.255" }, 
        { ip: "172.20.10.3", mask: "255.255.255.255" },
        { ip: "169.254.0.0", mask: "255.255.0.0" },
        { ip: "127.20.10.0", mask: "255.255.255.0" }
    ];
    var resolvedIP = dnsResolve(host);
    for (var i = 0; i < directAddresses.length; i++) {
        if (isInNet(resolvedIP, directAddresses[i].ip, directAddresses[i].mask)) {
            return "DIRECT";
        }
    }
    return "SOCKS5 172.20.10.1:7890";
}
