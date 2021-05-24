package main

import (
	"flag"
	"fmt"
)

func main() {
	var args ArgList = ArgList{}
	args.parseArgs()
	fmt.Println("Args:", args.String())
}

type ArgList struct {
	input  *string
	inType *string
	isFile *bool
	isInit bool
}

func (arg *ArgList) initArgs() {
	arg.input = flag.String("i", "", "Set domain/file.")
	arg.inType = flag.String("t", "ADR", "Set type: ADR/NS/PTR/TXT")
	arg.isFile = flag.Bool("f", false, "Source is file.")
	arg.isInit = true
}

func (arg *ArgList) parseArgs() {
	if arg.isInit != true {
		arg.initArgs()
	}

	flag.Parse()
}

func (arg *ArgList) String() string {
	return fmt.Sprintf(
		"{%s} {%s} {%t}", *arg.input, *arg.inType, *arg.isFile,
	)
}
