package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"os"
)

func main() {
	/*var args ArgList = ArgList{}
	args.parseArgs()
	fmt.Println("Args:", &args)*/

	var file FileLines = FileLines{}
	file.Open("/etc/fstab")
	defer file.Close()

	for {
		line, err := file.ReadLine()
		if err == io.EOF {
			break
		}

		fmt.Printf("%s\n", string(line))
	}
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
	self.input = flag.String("i", "", "Set domain/file.")
	self.inType = flag.String("t", "ADR", "Set type: ADR/NS/PTR/TXT")
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
