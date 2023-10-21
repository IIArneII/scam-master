package main

//go:generate rm -rf ./internal/pkg/openapi/restapi ./internal/pkg/openapi/client ./internal/pkg/openapi/models
//go:generate swagger generate server -t ./internal/pkg/openapi/ -f ./internal/pkg/openapi/swagger.yaml --strict-responders --strict-additional-properties --exclude-main
//go:generate swagger generate client -t ./internal/pkg/openapi/ -f ./internal/pkg/openapi/swagger.yaml --strict-responders --strict-additional-properties
