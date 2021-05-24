package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"net"
	"os"
)

func main() {
	var args ArgList = ArgList{}
	args.ParseArgs()

	var resolver DomResolver = DomResolver{}

	if *args.isFile {
		var reader FileReader = FileReader{}
		err := reader.Open(*args.input)

		if err != nil {
			panic(err)
		}

		for {
			line, err := reader.ReadLine()

			if err == io.EOF {
				break
			}

			resolver.SetValue(line)
			err = resolver.Resolve()

			if err != nil {
				continue
			}

			resolver.PrintResults()
		}

		reader.Close()

	} else {
		resolver.SetValue(*args.input)
		err := resolver.Resolve()

		if err == nil {
			resolver.PrintResults()
		}
	}
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

func (self *ArgList) InitArgs() {
	self.input = flag.String("i", "", "Set domain/ip/file.")
	self.isFile = flag.Bool("f", false, "Source is file.")

	self.isInit = true
}

func (self *ArgList) ParseArgs() {
	if self.isInit == false {
		self.InitArgs()
	}

	flag.Parse()
}

func (self *ArgList) ShowArgs() string {
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
	ferr  error
}

func (self *FileReader) Open(fname string) error {
	self.fname = fname
	self.fptr, self.ferr = os.Open(self.fname)

	if self.ferr != nil {
		return self.ferr
	}

	self.frdr = bufio.NewReader(self.fptr)
	return nil
}

func (self *FileReader) Close() error {
	self.ferr = self.fptr.Close()
	return self.ferr
}

func (self *FileReader) ReadLine() (string, error) {
	line, _, err := self.frdr.ReadLine()
	return string(line), err
}

/*
Resolve domain...
*/
type DomResolver struct {
	domAddr string
	isAddr  bool
	results []string
}

func (self *DomResolver) SetValue(val string) {
	if ip := net.ParseIP(val); ip != nil {
		self.domAddr = val
		self.isAddr = false

	} else {
		self.domAddr = val
		self.isAddr = true
	}
}

func (self *DomResolver) PrintResults() {
	for it := 0; it < len(self.results); it++ {
		fmt.Printf("%s\n", self.results[it])
	}
}

func (self *DomResolver) Resolve() error {
	if self.isAddr {
		res, err := net.LookupHost(self.domAddr)

		if err != nil {
			return err
		}

		self.results = res

	} else {
		res, err := net.LookupAddr(self.domAddr)

		if err != nil {
			return err
		}

		self.results = res
	}

	return nil
}
