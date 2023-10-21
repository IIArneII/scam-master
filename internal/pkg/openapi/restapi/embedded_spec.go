// Code generated by go-swagger; DO NOT EDIT.

package restapi

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"encoding/json"
)

var (
	// SwaggerJSON embedded version of the swagger document used at generation time
	SwaggerJSON json.RawMessage
	// FlatSwaggerJSON embedded flattened version of the swagger document used at generation time
	FlatSwaggerJSON json.RawMessage
)

func init() {
	SwaggerJSON = json.RawMessage([]byte(`{
  "consumes": [
    "application/json"
  ],
  "produces": [
    "application/json"
  ],
  "schemes": [
    "http"
  ],
  "swagger": "2.0",
  "info": {
    "description": "Bank transfer system",
    "title": "scam-master",
    "version": "1.0.0"
  },
  "paths": {
    "/confirm-transaction": {
      "post": {
        "description": "Confirm the funds transfer with a confirmation code.",
        "tags": [
          "Transactions"
        ],
        "summary": "Confirm transaction",
        "operationId": "Confirm",
        "parameters": [
          {
            "name": "body",
            "in": "body",
            "schema": {
              "$ref": "#/definitions/%D0%A1onfirm"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "OK"
          },
          "400": {
            "$ref": "#/responses/BadRequest"
          },
          "404": {
            "$ref": "#/responses/NotFound"
          },
          "default": {
            "$ref": "#/responses/InternalError"
          }
        }
      }
    },
    "/health-check": {
      "get": {
        "description": "Checking the server health status.",
        "tags": [
          "Standard"
        ],
        "summary": "Health check",
        "operationId": "HealthCheck",
        "responses": {
          "200": {
            "description": "OK",
            "schema": {
              "type": "object",
              "properties": {
                "ok": {
                  "type": "boolean"
                }
              }
            }
          }
        }
      }
    },
    "/init-transaction": {
      "post": {
        "description": "Initialize funds transfer from card to card.",
        "tags": [
          "Transactions"
        ],
        "summary": "Init transaction",
        "operationId": "Init",
        "parameters": [
          {
            "name": "body",
            "in": "body",
            "schema": {
              "$ref": "#/definitions/Transaction"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "OK"
          },
          "400": {
            "$ref": "#/responses/BadRequest"
          },
          "default": {
            "$ref": "#/responses/InternalError"
          }
        }
      }
    }
  },
  "definitions": {
    "Error": {
      "type": "object",
      "required": [
        "code",
        "message"
      ],
      "properties": {
        "code": {
          "description": "Either same as HTTP Status Code OR \u003e= 600",
          "type": "integer",
          "format": "int32"
        },
        "message": {
          "type": "string"
        }
      }
    },
    "Transaction": {
      "type": "object",
      "required": [
        "transactionID",
        "senderCardNumber",
        "validity",
        "cvc",
        "recipientCardNumber",
        "bankGateway",
        "senderBank",
        "amount"
      ],
      "properties": {
        "amount": {
          "description": "Amount in kopecks (RUB * 10^2)",
          "type": "integer",
          "format": "int64",
          "minimum": 1
        },
        "bankGateway": {
          "description": "The bank through which the funds will be transferred",
          "type": "string",
          "enum": [
            "tinkoff"
          ]
        },
        "cvc": {
          "type": "string",
          "pattern": "^\\d{3}$",
          "example": "111"
        },
        "recipientCardNumber": {
          "type": "string",
          "pattern": "^\\d{16}$",
          "example": "1111111111111111"
        },
        "senderBank": {
          "description": "Sender's card bank",
          "type": "string",
          "enum": [
            "tinkoff"
          ]
        },
        "senderCardNumber": {
          "type": "string",
          "pattern": "^\\d{16}$",
          "example": "1111111111111111"
        },
        "transactionID": {
          "type": "string"
        },
        "validity": {
          "type": "string",
          "pattern": "^\\d{4}$",
          "example": "0101"
        }
      }
    },
    "Сonfirm": {
      "type": "object",
      "required": [
        "transactionID",
        "confirmationСode"
      ],
      "properties": {
        "confirmationСode": {
          "type": "string"
        },
        "transactionID": {
          "type": "string"
        }
      }
    }
  },
  "responses": {
    "BadRequest": {
      "description": "Bad request",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    },
    "Forbidden": {
      "description": "Forbidden",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    },
    "InternalError": {
      "description": "Internal error",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    },
    "NotFound": {
      "description": "Not found",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    }
  }
}`))
	FlatSwaggerJSON = json.RawMessage([]byte(`{
  "consumes": [
    "application/json"
  ],
  "produces": [
    "application/json"
  ],
  "schemes": [
    "http"
  ],
  "swagger": "2.0",
  "info": {
    "description": "Bank transfer system",
    "title": "scam-master",
    "version": "1.0.0"
  },
  "paths": {
    "/confirm-transaction": {
      "post": {
        "description": "Confirm the funds transfer with a confirmation code.",
        "tags": [
          "Transactions"
        ],
        "summary": "Confirm transaction",
        "operationId": "Confirm",
        "parameters": [
          {
            "name": "body",
            "in": "body",
            "schema": {
              "$ref": "#/definitions/%D0%A1onfirm"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "OK"
          },
          "400": {
            "description": "Bad request",
            "schema": {
              "$ref": "#/definitions/Error"
            }
          },
          "404": {
            "description": "Not found",
            "schema": {
              "$ref": "#/definitions/Error"
            }
          },
          "default": {
            "description": "Internal error",
            "schema": {
              "$ref": "#/definitions/Error"
            }
          }
        }
      }
    },
    "/health-check": {
      "get": {
        "description": "Checking the server health status.",
        "tags": [
          "Standard"
        ],
        "summary": "Health check",
        "operationId": "HealthCheck",
        "responses": {
          "200": {
            "description": "OK",
            "schema": {
              "type": "object",
              "properties": {
                "ok": {
                  "type": "boolean"
                }
              }
            }
          }
        }
      }
    },
    "/init-transaction": {
      "post": {
        "description": "Initialize funds transfer from card to card.",
        "tags": [
          "Transactions"
        ],
        "summary": "Init transaction",
        "operationId": "Init",
        "parameters": [
          {
            "name": "body",
            "in": "body",
            "schema": {
              "$ref": "#/definitions/Transaction"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "OK"
          },
          "400": {
            "description": "Bad request",
            "schema": {
              "$ref": "#/definitions/Error"
            }
          },
          "default": {
            "description": "Internal error",
            "schema": {
              "$ref": "#/definitions/Error"
            }
          }
        }
      }
    }
  },
  "definitions": {
    "Error": {
      "type": "object",
      "required": [
        "code",
        "message"
      ],
      "properties": {
        "code": {
          "description": "Either same as HTTP Status Code OR \u003e= 600",
          "type": "integer",
          "format": "int32"
        },
        "message": {
          "type": "string"
        }
      }
    },
    "Transaction": {
      "type": "object",
      "required": [
        "transactionID",
        "senderCardNumber",
        "validity",
        "cvc",
        "recipientCardNumber",
        "bankGateway",
        "senderBank",
        "amount"
      ],
      "properties": {
        "amount": {
          "description": "Amount in kopecks (RUB * 10^2)",
          "type": "integer",
          "format": "int64",
          "minimum": 1
        },
        "bankGateway": {
          "description": "The bank through which the funds will be transferred",
          "type": "string",
          "enum": [
            "tinkoff"
          ]
        },
        "cvc": {
          "type": "string",
          "pattern": "^\\d{3}$",
          "example": "111"
        },
        "recipientCardNumber": {
          "type": "string",
          "pattern": "^\\d{16}$",
          "example": "1111111111111111"
        },
        "senderBank": {
          "description": "Sender's card bank",
          "type": "string",
          "enum": [
            "tinkoff"
          ]
        },
        "senderCardNumber": {
          "type": "string",
          "pattern": "^\\d{16}$",
          "example": "1111111111111111"
        },
        "transactionID": {
          "type": "string"
        },
        "validity": {
          "type": "string",
          "pattern": "^\\d{4}$",
          "example": "0101"
        }
      }
    },
    "Сonfirm": {
      "type": "object",
      "required": [
        "transactionID",
        "confirmationСode"
      ],
      "properties": {
        "confirmationСode": {
          "type": "string"
        },
        "transactionID": {
          "type": "string"
        }
      }
    }
  },
  "responses": {
    "BadRequest": {
      "description": "Bad request",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    },
    "Forbidden": {
      "description": "Forbidden",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    },
    "InternalError": {
      "description": "Internal error",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    },
    "NotFound": {
      "description": "Not found",
      "schema": {
        "$ref": "#/definitions/Error"
      }
    }
  }
}`))
}