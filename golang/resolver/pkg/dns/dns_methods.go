package dns

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const (
	RESOLV_CONF_PATH = "/etc/resolv.conf"
)

func LoadResolvConf(confPath string) ([]string, error) {
	if fd, err := os.OpenFile(confPath, os.O_RDONLY, 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		return nil, err

	} else {
		var scanner = bufio.NewScanner(fd)
		var items = make([]string, 0, 3)

		for scanner.Scan() {
			line := scanner.Text()

			if strings.HasPrefix(line, "nameserver") {
				if words := strings.Split(line, " "); words != nil {
					items = append(items, words[1])
				}
			}
		}

		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		}

		fd.Close()
		return items, nil
	}
}
