package app

import "errors"

var (
	ErrNotFound   = errors.New("entity not found")
	ErrForbidden  = errors.New("access denied")
	ErrBadRequest = errors.New("no fields to update")
)
