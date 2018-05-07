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
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/sahilm/fuzzy"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

var pattern string
var inputFile string
var highlight bool

// matchCmd represents the match command
var matchCmd = &cobra.Command{
	Use:   "match",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		log.Debug("match called")
		log.Debug(pattern)
		log.Debug(inputFile)
		var dataBytes []byte
		var err error
		if inputFile == "-" {
			dataBytes, err = ioutil.ReadAll(os.Stdin)
		} else {
			dataBytes, err = ioutil.ReadFile(inputFile)
		}
		if err != nil {
			panic(err)
		}

		data := strings.Split(string(dataBytes), "\n")
		matches := fuzzy.Find(pattern, data)
		for _, match := range matches {
			if !highlight {
				fmt.Println(match.Str)
			} else {
				var output strings.Builder
				for i := 0; i < len(match.Str); i++ {
					if contains(i, match.MatchedIndexes) {
						output.WriteString(fmt.Sprintf("\033[1m%s\033[0m", string(match.Str[i])))
					} else {
						output.WriteString(string(match.Str[i]))
					}
				}
				fmt.Println(output.String())
			}
		}
	},
}

func contains(needle int, haystack []int) bool {
	for _, i := range haystack {
		if needle == i {
			return true
		}
	}
	return false
}
func init() {
	RootCmd.AddCommand(matchCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// matchCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	matchCmd.Flags().StringVarP(&pattern, "pattern", "p", "", "pattern to match on")
	matchCmd.MarkFlagRequired("pattern")
	matchCmd.Flags().StringVarP(&inputFile, "input", "i", "-", "Input file with line separated input; '-' means use stdio")
	matchCmd.Flags().BoolVarP(&highlight, "highlight", "l", true, "highlight matches")
}
