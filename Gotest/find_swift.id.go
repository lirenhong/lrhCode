package main

import (
	"bytes"
	"database/sql"
	"encoding/binary"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var wg sync.WaitGroup

var HOST = "http://192.168.138.80:9022"

var metaDataRootID string = ""

type Ret struct {
	ObId        string
	CusMetadata string
}

type VersionMetadata struct {
	Ver                           uint32
	ByteLen, VerLen, ClientTime   uint64
	UserID, FileName, VersionData string
}

func checkErr(err interface{}) {
	if err != nil {
		fmt.Println(err)
		os.Exit(0)
	}
}

func connectDB() *sql.DB {
	db, err := sql.Open("mysql", "Anyshare:asAlqlTkWU0zqfxrLTed@tcp(192.168.138.80:3320)/eofs?charset=utf8")
	checkErr(err)
	return db
}

func unpack(Param interface{}, buf *bytes.Buffer, n int) {
	tmp := bytes.NewReader(buf.Next(n))
	err := binary.Read(tmp, binary.BigEndian, Param)
	checkErr(err)
}

func unpackStringLength(Length uint32, buf *bytes.Buffer, n int) string {
	unpack(&Length, buf, n)
	x := int(Length)
	return string(buf.Next(x))
}

func readVersionMetadataBlob(blob string) *VersionMetadata {
	var vsm *VersionMetadata = new(VersionMetadata)
	buf := bytes.NewBuffer([]byte(blob))

	unpack(&vsm.ByteLen, buf, 8)
	unpack(&vsm.Ver, buf, 4)

	var length uint32
	vsm.UserID = unpackStringLength(length, buf, 4)
	vsm.FileName = unpackStringLength(length, buf, 4)

	if vsm.Ver >= 1 {
		unpack(&vsm.VerLen, buf, 8)
	}
	if vsm.Ver >= 2 {
		unpack(&vsm.ClientTime, buf, 8)
	}
	if vsm.Ver >= 3 {
		vsm.VersionData = unpackStringLength(length, buf, 4)
	}
	return vsm

}

func getObjectIDFullName(eofsCusor *sql.DB, objID string) string {
	if metaDataRootID == "" {
		row := eofsCusor.QueryRow("SELECT objectId FROM metadata WHERE parentId='00000000000000000000000000000000")
		err := row.Scan(&metaDataRootID)
		checkErr(err)
	}

	idx := objID
	cid := ""

	for {
		row := eofsCusor.QueryRow("SELECT parentId, name FROM metadata WHERE objectId=?", idx)
		err := row.Scan(&idx)
		checkErr(err)

		if idx == metaDataRootID {
			break
		}

		cid = idx
	}
	eofsCusor.Close()
	return cid
}

func Check(versionObejectID string) {
	var ret *Ret = new(Ret)
	var swiftAccount, swiftObject string

	eofsCusor := connectDB()
	rows, err := eofsCusor.Query("select objectId, custom_metadata from metadata where objectId=? and basic_attr=4", versionObejectID)
	checkErr(err)

	for rows.Next() {
		err = rows.Scan(&ret.ObId, &ret.CusMetadata)
		checkErr(err)
		vsm := readVersionMetadataBlob(ret.CusMetadata)
		if len(vsm.VersionData) == 64 {
			swiftAccount = vsm.VersionData[32:64]
			swiftObject = vsm.VersionData[0:32]
		} else {
			swiftAccount = getObjectIDFullName(eofsCusor, ret.ObId)
			swiftObject = ret.ObId
		}
		downLoadFile(swiftAccount, swiftObject, HOST, vsm.FileName, vsm.VerLen)
	}
}

func exists(fileName string) bool {
	_, err := os.Stat(fileName)
	if err == nil {
		return true
	}
	if os.IsNotExist(err) {
		return false
	}
	return true
}

func downLoadFile(swiftAccount, swiftObject, host, fileName string, dataLen uint64) {
	var totalSize int = 0
	absPath := fmt.Sprintf("C:\\Users\\lrh\\Desktop\\find_swift\\%s", fileName)

	//f, err := os.OpenFile(absPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0666)
	f, err := os.Create(absPath)
	checkErr(err)
	defer f.Close()

	for i := 0; ; i++ {
		URL := fmt.Sprintf("%s/v1/%s/db/%s-%d", host, swiftAccount, swiftObject, i)

		resp, err := http.Get(URL)
		checkErr(err)

		if resp.StatusCode != 200 {
			break
		}

		contentLen, _ := strconv.Atoi(resp.Header["Content-Length"][0])
		totalSize += contentLen

		bodyString, err := ioutil.ReadAll(resp.Body)
		checkErr(err)

		_, err = f.Write(bodyString)
		checkErr(err)
	}
	tmp := uint64(totalSize)
	if dataLen == tmp {
		fmt.Println("DownLoad %s Successfully!", fileName)
	} else {
		fmt.Println("Data Error!")
	}
	time.Sleep(2 * time.Second)
	fmt.Println("ok")
	defer wg.Done()

}

func main() {
	Ids := []string{"00543D35F12840CC97C961775EFB8820", "0012334C32B847DBA937857D71A8A65C", "00249307D6BE4A28BB167858E9B21D3B"}
	for _, v := range Ids {
		wg.Add(1)
		go Check(v)
	}
	wg.Wait()
}
