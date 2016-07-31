import usocket
#import network
#esp = network.WLAN(network.STA_IF)
#esp.active(True)
#esp.connect('madagscar','lillianEMMA')
class Response:
    
    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None
    
    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None
    
    @property
    def content(self):
        if self._cached is None:
            self._cached = self.raw.read()
            self.raw.close()
            self.raw = None
        return self._cached
    
    @property
    def text(self):
        return str(self.content, self.encoding)
    
    def json(self):
        import ujson
        return ujson.loads(self.content)

# class Http:

def request(method, url, data=None, json=None, headers={}, stream=None):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)
    
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    
#    print("addres {0}:{1} | proto {2} | path {3}".format(host, port, proto, path))
    ai = usocket.getaddrinfo(host, port)
    # print(ai)
    addr = ai[0][-1]
    s = usocket.socket()
    # print(addr)
    s.connect(addr)
    if proto == "https:":
        s = ussl.wrap_socket(s)
    s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
    if not "Host" in headers:
        s.write(b"Host: %s\r\n" % host)
    # Iterate over keys to avoid tuple alloc
    for k in headers:
        s.write(k)
        s.write(b": ")
        s.write(headers[k])
        s.write(b"\r\n")
    if json is not None:
        assert data is None
        import ujson
        data = ujson.dumps(json)
    if data:
        s.write(b"Content-Length: %d\r\n" % len(data))
    s.write(b"\r\n")
    # print(str(data))
    if data:
        s.write(str(data))
    
    l = s.readline()
    protover, status, msg = l.split(None, 2)
    status = int(status)
    #print(protover, status, msg)

    # Added redirect support
    if status in range(300, 309):
        return self.request(method, url, data, json, headers, stream)

    while True:
        l = s.readline()
        if not l or l == b"\r\n":
            break
        #print(line)
        if l.startswith(b"Transfer-Encoding:"):
            if b"chunked" in line:
                raise ValueError("Unsupported " + l)
        elif l.startswith(b"Location:"):
            raise NotImplementedError("Redirects not yet supported")
    
    resp = Response(s)
    resp.status_code = status
    resp.reason = msg.rstrip()
    resp.close()
    return resp


# @classmethod
def head(url, **kw):
    return request("HEAD", url, **kw)

# @classmethod
def get(url, **kw):
    return request("GET", url, **kw)

# @classmethod    
def post(url, **kw):
    return request("POST", url, **kw)

# @classmethod
def put(url, **kw):
    return request("PUT", url, **kw)

# @classmethod 
def patch(url, **kw):
    return request("PATCH", url, **kw)

# @classmethod
def delete(url, **kw):
    return request("DELETE", url, **kw)

# @classmethod
def test():
    r = (post('http://192.168.1.76:3000/sensors/1/readings.json', 
        json={'reading': {'value': 99}}, 
        headers={'Content-Type':'application/json'}))
    # print(r.status_code)
    return r
