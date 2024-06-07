function FindProxyForURL(url, host) {
    if (/(^127\.)|(^192\.168\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)/.test(dnsResolve(host))) {
        return "DIRECT";
    }

    var appleDomains = [
        "akadns.net",
        "apple.com",
        "aaplimg.com",
        "qtlcdn.com",
        "akamai.net",
        "akamaiedge.net",
        "ks-cdn.com",
        "ksyuncdn.com",
        "applemusic.com",
        "blobstore.apple.com",
        "music.apple.com",
        "aod.itunes.apple.com",
        "aod-ssl.itunes.apple.com",
        "audio.itunes.apple.com",
        "audio-ssl.itunes.apple.com",
        "mvod.itunes.apple.com",
        "streamingaudio.itunes.apple.com",
        "split.io"
    ];

    for (var i = 0; i < appleDomains.length; i++) {
        if (shExpMatch(host, "*" + appleDomains[i]) || shExpMatch(url, "*" + appleDomains[i])) {
            // return "PROXY 172.20.10.1:7891";
            return "DIRECT";
        }
    }

    return "SOCKS5 172.20.10.1:7890";
}
