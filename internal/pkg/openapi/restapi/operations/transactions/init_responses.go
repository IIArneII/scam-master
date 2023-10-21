// Code generated by go-swagger; DO NOT EDIT.

package transactions

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"net/http"

	"github.com/go-openapi/runtime"
	"github.com/go-openapi/runtime/middleware"

	"scam-master/internal/pkg/openapi/models"
)

// InitNoContentCode is the HTTP code returned for type InitNoContent
const InitNoContentCode int = 204

/*
InitNoContent OK

swagger:response initNoContent
*/
type InitNoContent struct {
}

// NewInitNoContent creates InitNoContent with default headers values
func NewInitNoContent() *InitNoContent {

	return &InitNoContent{}
}

// WriteResponse to the client
func (o *InitNoContent) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.Header().Del(runtime.HeaderContentType) //Remove Content-Type on empty responses

	rw.WriteHeader(204)
}

func (o *InitNoContent) InitResponder() {}

// InitBadRequestCode is the HTTP code returned for type InitBadRequest
const InitBadRequestCode int = 400

/*
InitBadRequest Bad request

swagger:response initBadRequest
*/
type InitBadRequest struct {

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewInitBadRequest creates InitBadRequest with default headers values
func NewInitBadRequest() *InitBadRequest {

	return &InitBadRequest{}
}

// WithPayload adds the payload to the init bad request response
func (o *InitBadRequest) WithPayload(payload *models.Error) *InitBadRequest {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the init bad request response
func (o *InitBadRequest) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *InitBadRequest) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(400)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

func (o *InitBadRequest) InitResponder() {}

/*
InitDefault Internal error

swagger:response initDefault
*/
type InitDefault struct {
	_statusCode int

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewInitDefault creates InitDefault with default headers values
func NewInitDefault(code int) *InitDefault {
	if code <= 0 {
		code = 500
	}

	return &InitDefault{
		_statusCode: code,
	}
}

// WithStatusCode adds the status to the init default response
func (o *InitDefault) WithStatusCode(code int) *InitDefault {
	o._statusCode = code
	return o
}

// SetStatusCode sets the status to the init default response
func (o *InitDefault) SetStatusCode(code int) {
	o._statusCode = code
}

// WithPayload adds the payload to the init default response
func (o *InitDefault) WithPayload(payload *models.Error) *InitDefault {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the init default response
func (o *InitDefault) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *InitDefault) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(o._statusCode)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

func (o *InitDefault) InitResponder() {}

type InitNotImplementedResponder struct {
	middleware.Responder
}

func (*InitNotImplementedResponder) InitResponder() {}

func InitNotImplemented() InitResponder {
	return &InitNotImplementedResponder{
		middleware.NotImplemented(
			"operation authentication.Init has not yet been implemented",
		),
	}
}

type InitResponder interface {
	middleware.Responder
	InitResponder()
}
