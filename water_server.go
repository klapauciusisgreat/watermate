package main

import (
  "net/http"
  "os"
  "time"
  "fmt"
  "encoding/json"
  "bufio"
)
var f os.File

func check(e error) {
    if e != nil {
        panic(e)
    }
}

type Payload struct {
    Pulses int
    Random int
    Checksum int
}

func handler(w http.ResponseWriter, r *http.Request){
  var p Payload
  fmt.Println("time: %s", time.Now().Format(time.UnixDate))

  err := json.NewDecoder(r.Body).Decode(&p)
  if err != nil {
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  fmt.Println("Payload: %+v", p)

  w2 := bufio.NewWriter(f)
  
  _, err = fmt.Fprintf(w2, "time: %s", time.Now().Format(time.UnixDate))
  check(err)

  _, err = fmt.Fprintf(w2, "Payload: %+v", p)
  check(err)

  w2.Flush()
}

func main() {

  f, err := os.Create("/home/USER/water")
  check(err)
  defer f.Close()

  http.HandleFunc("/", handler)
  http.ListenAndServe("0.0.0.0:7777", nil)
}
