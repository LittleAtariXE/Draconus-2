
class DefaultWormVariable:
    def __init__(self, builder: object):
        self.conf = builder
        self.variables = self._build_variables()
    

    def _build_variables(self) -> dict:
        dvar = {
            "IP_ADDR" : self.conf.ip,
            "SOCKET_ENCODE" : self.conf.tcp_socket_format,
            "SOCKET_RAW_LEN" : self.conf.tcp_socket_raw_len
        }

        return dvar