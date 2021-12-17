package dns

import (
	"context"
	"net"
	"strconv"
)

func NewResolver(server string, port int) *net.Resolver {
	return &net.Resolver{
		PreferGo: true,
		Dial: func(ctx context.Context, network, address string) (net.Conn, error) {
			var netDial = net.Dialer{}
			var netAddr = server + ":" + strconv.Itoa(port)
			return netDial.DialContext(ctx, network, netAddr)
		},
	}
}
