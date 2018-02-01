package main

import (
	"bufio"
	"fmt"
	"io"
	"os/exec"
)

func main() {
	command := "curl"
	params := []string{"-X", "GET", "http://192.168.138.80:9022/v1/4ECC18C5C7824E45BDE949F24DDE6255/db/E4B1C17F60784E4CBADA9ED79A21EF58-0"}
	//执行cmd命令: ls -l
	execCommand(command, params)
}

func execCommand(commandName string, params []string) bool {
	cmd := exec.Command(commandName, params...)

	//显示运行的命令
	fmt.Println(cmd.Args)

	stdout, err := cmd.StdoutPipe()

	if err != nil {
		fmt.Println(err)
		return false
	}

	cmd.Start()

	reader := bufio.NewReader(stdout)

	//实时循环读取输出流中的一行内容
	for {
		line, err2 := reader.ReadString('\n')
		if err2 != nil || io.EOF == err2 {
			break
		}
		fmt.Println(line)
	}

	cmd.Wait()
	return true
}
