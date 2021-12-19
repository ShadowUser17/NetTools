package dns_test

import (
	"github.com/ShadowUser17/NetTools/golang/resolver/pkg/dns"

	"testing"
)

func TestLoadResolvConf(t *testing.T) {
	if items, err := dns.LoadResolvConf(dns.RESOLV_CONF_PATH); err != nil {
		t.Errorf("Error: %v\n", err)

	} else {
		for it := range items {
			t.Logf("Nameserver: %s\n", items[it])
		}
	}
}
