// Copyright © 2018 NAME HERE <EMAIL ADDRESS>
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"net"
	"net/http"

	"github.com/raghur/fuzzy-denite/lib"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

var port string
var size int
var usegrpc bool

// serverCmd represents the server command
var serverCmd = &cobra.Command{
	Use:   "server",
	Short: "Start in server mode on the specified port",
	Run: func(cmd *cobra.Command, args []string) {
		if !usegrpc {
			lib.CreateServer(size)
			log.Infof("starting on %s", port)
			http.ListenAndServe("localhost:"+port, nil)
		} else {
			lis, err := net.Listen("tcp", ":"+port)
			if err != nil {
				log.Fatalf("failed to listen: %v", err)
			}
			svr := lib.CreateGRPCServer(20)
			log.Infof("starting GRPC on %s", port)
			if err := svr.Serve(lis); err != nil {
				log.Fatalf("failed to serve: %v", err)
			}
		}
	},
}

func init() {
	RootCmd.AddCommand(serverCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// serverCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	serverCmd.Flags().StringVarP(&port, "port", "p", "9009", "port to run the server on")
	serverCmd.Flags().IntVarP(&size, "size", "s", 20, "Size of the cache")
	serverCmd.Flags().BoolVar(&usegrpc, "grpc", false, "Use a grpc server")
}
