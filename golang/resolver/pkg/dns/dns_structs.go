package dns

import (
	"net"
)

type Domains struct {
	Resolver *net.Resolver
	DomList  []string
}
