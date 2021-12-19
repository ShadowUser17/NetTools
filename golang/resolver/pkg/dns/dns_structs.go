package dns

import (
	"context"
	"net"
	"strconv"
)

const (
	DEFAULT_RESOLVER_ADDR = "127.0.0.1"
	DEFAULT_RESOLVER_PORT = 53
)

type Domains struct {
	Resolver *net.Resolver
	DomList  map[string]string
}

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

func NewDomains() *Domains {
	var dom = Domains{
		Resolver: NewResolver(DEFAULT_RESOLVER_ADDR, DEFAULT_RESOLVER_PORT),
		DomList:  make(map[string]string),
	}

	return &dom
}
