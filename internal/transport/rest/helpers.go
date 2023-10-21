package rest

import (
	"errors"
	"net/http"
	"scam-master/internal/app"
	"scam-master/internal/pkg/openapi/models"

	"github.com/go-openapi/swag"
	"go.uber.org/zap"
)

type errorSetter interface {
	SetPayload(payload *models.Error)
	SetStatusCode(code int)
}

var errorMapping = map[error]int{
	app.ErrBadRequest: http.StatusBadRequest,
	app.ErrForbidden:  http.StatusForbidden,
	app.ErrNotFound:   http.StatusNotFound,
}

func setAPIError(l *zap.SugaredLogger, op string, err error, responder interface{}) {
	r, ok := responder.(errorSetter)
	if !ok {
		return
	}

	statusCode, exists := getStatusCodeForError(err)

	msg := err.Error()
	if !exists {
		statusCode = http.StatusInternalServerError
		msg = "Internal server error"

		l.Errorln(op, err)
	}

	r.SetPayload(&models.Error{Code: swag.Int32(int32(statusCode)), Message: swag.String(msg)})
	r.SetStatusCode(statusCode)
}

func getStatusCodeForError(err error) (int, bool) {
	for knownErr, code := range errorMapping {
		if errors.Is(err, knownErr) {
			return code, true
		}
	}
	code, exists := errorMapping[err]
	return code, exists
}
