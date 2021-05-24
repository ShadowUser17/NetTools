package main

import (
	"bufio"
	"flag"
	"fmt"
	"net"
	"os"
)

func main() {
	/*var args ArgList = ArgList{}
	args.parseArgs()
	fmt.Println("Args:", &args)*/

	/*var file FileLines = FileLines{}
	file.Open("/etc/fstab")
	defer file.Close()

	for {
		line, err := file.ReadLine()
		if err == io.EOF {
			break
		}

		fmt.Printf("%s\n", string(line))
	}*/

	var resolver DomResolver = DomResolver{}
	resolver.setValue("139.162.152.136")
	resolver.domType = "PTR"
	resolver.Resolve()
	resolver.printRes()
}

/*
 Parse Args...
*/
type ArgList struct {
	input  *string
	inType *string
	isFile *bool
	isInit bool
}

func (self *ArgList) initArgs() {
	self.input = flag.String("i", "", "Set domain/ip/file.")
	self.inType = flag.String("t", "ADR", "Set type: ADR/NS/PTR")
	self.isFile = flag.Bool("f", false, "Source is file.")
	self.isInit = true
}

func (self *ArgList) parseArgs() {
	if self.isInit == false {
		self.initArgs()
	}

	flag.Parse()
}

func (self *ArgList) String() string {
	return fmt.Sprintf(
		"{%s} {%s} {%t}", *self.input, *self.inType, *self.isFile,
	)
}

/*
Read file...
*/
type FileLines struct {
	fname string
	fptr  *os.File
	frdr  *bufio.Reader
}

func (self *FileLines) Open(fname string) {
	var err error

	self.fname = fname
	self.fptr, err = os.Open(self.fname)
	if err != nil {
		panic(err)
	}

	self.frdr = bufio.NewReader(self.fptr)
}

func (self *FileLines) Close() {
	self.fptr.Close()
}

func (self *FileLines) ReadLine() ([]byte, error) {
	line, _, err := self.frdr.ReadLine()
	return line, err
}

/*
Resolve domain...
*/
type DomResolver struct {
	domName string
	domAddr string
	domType string
	results []string
}

func (self *DomResolver) setValue(val string) {
	if ip := net.ParseIP(val); ip != nil {
		self.domAddr = val
	} else {
		self.domName = val
	}
}

func (self *DomResolver) printRes() {
	for it := 0; it < len(self.results); it++ {
		fmt.Printf("%s\n", self.results[it])
	}
}

func (self *DomResolver) nsToStrings(items []*net.NS) {
	for it := 0; it < len(items); it++ {
		self.results = append(self.results, items[it].Host)
	}
}

func (self *DomResolver) Resolve() {
	switch self.domType {
	case "ADR":
		res, err := net.LookupHost(self.domName)
		if err != nil {
			panic(err)
		}
		self.results = res

	case "PTR":
		res, err := net.LookupAddr(self.domAddr)
		if err != nil {
			panic(err)
		}
		self.results = res

	case "NS":
		res, err := net.LookupNS(self.domName)
		if err != nil {
			panic(err)
		}
		self.nsToStrings(res)

	default:
		fmt.Printf("WTF? {%s}\n", self.domType)
	}
}
