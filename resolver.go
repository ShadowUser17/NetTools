package main

import (
	"bufio"
	"flag"
	"fmt"
	"net"
	"os"
)

func main() {
	var args ArgList = ArgList{}
	args.parseArgs()

	/*var resolver DomResolver = DomResolver{}
	resolver.setValue(*args.input)*/

}

/*
 Parse Args...
*/
type ArgList struct {
	input  *string
	output *string
	isFile *bool
	isInit bool
}

func (self *ArgList) initArgs() {
	self.input = flag.String("i", "", "Set domain/ip/file.")
	self.output = flag.String("o", "", "Set output file.")
	self.isFile = flag.Bool("f", false, "Source is file.")

	self.isInit = true
}

func (self *ArgList) parseArgs() {
	if self.isInit == false {
		self.initArgs()
	}

	flag.Parse()
}

func (self *ArgList) showArgs() string {
	return fmt.Sprintf(
		"{%s} {%s} {%t}", *self.input, *self.output, *self.isFile,
	)
}

/*
Read file...
*/
type FileReader struct {
	fname string
	fptr  *os.File
	frdr  *bufio.Reader
}

func (self *FileReader) Open(fname string) {
	var err error

	self.fname = fname
	self.fptr, err = os.Open(self.fname)
	if err != nil {
		panic(err)
	}

	self.frdr = bufio.NewReader(self.fptr)
}

func (self *FileReader) Close() {
	self.fptr.Close()
}

func (self *FileReader) ReadLine() ([]byte, error) {
	line, _, err := self.frdr.ReadLine()
	return line, err
}

/*
Resolve domain...
*/
type DomResolver struct {
	domAddr string
	isAddr  bool
	results []string
}

func (self *DomResolver) setValue(val string) {
	if ip := net.ParseIP(val); ip != nil {
		self.domAddr = val
		self.isAddr = true
	} else {
		self.domAddr = val
		self.isAddr = false
	}
}

func (self *DomResolver) printResults() {
	for it := 0; it < len(self.results); it++ {
		fmt.Printf("%s\n", self.results[it])
	}
}

func (self *DomResolver) Resolve() {
	if self.isAddr {
		res, err := net.LookupHost(self.domAddr)
		if err != nil {
			panic(err)
		}
		self.results = res

	} else {
		res, err := net.LookupAddr(self.domAddr)
		if err != nil {
			panic(err)
		}
		self.results = res
	}
}

/*
Write file...
*/
type FileWriter struct {
	fname string
	fptr  *os.File
}

func (self *FileWriter) Open(fname string) {
	var err error

	self.fname = fname
	self.fptr, err = os.Open(self.fname)
	if err != nil {
		panic(err)
	}
}

func (self *FileWriter) Close() {
	self.fptr.Close()
}

func (self *FileWriter) Write(items []string) {
	for it := 0; it < len(items); it++ {
		self.fptr.Write([]byte(items[it]))
	}
}
