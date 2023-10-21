package rest

import (
	"net"
	"net/http"
	"strings"

	"github.com/felixge/httpsnoop"
	"github.com/powerman/structlog"
	"go.uber.org/zap"
)

type middlewareFunc func(http.Handler) http.Handler

func makeLogger(basePath string, l *zap.SugaredLogger) middlewareFunc {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			l.Infow("incoming", "remote_addr", r.RemoteAddr, "http_status", "", "method", r.Method, "func", strings.TrimPrefix(r.URL.Path, basePath))

			next.ServeHTTP(w, r)
		})
	}
}

func recovery(next http.Handler, l *zap.SugaredLogger) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			const code = http.StatusInternalServerError
			switch err := recover(); err := err.(type) {
			default:
				l.Errorw("panic", "http_status", code, "err", err, structlog.KeyStack, structlog.Auto)
				w.WriteHeader(code)
			case nil:
			case net.Error:
				l.Errorw("panic", "http_status", code, "err", err)
				w.WriteHeader(code)
			}
		}()

		next.ServeHTTP(w, r)
	})
}

func makeAccessLog(basePath string, l *zap.SugaredLogger) middlewareFunc {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			m := httpsnoop.CaptureMetrics(next, w, r)

			if m.Code < 500 {
				l.Infow("handled", "http_status", m.Code)
			} else {
				l.Infow("failed to handle", "http_status", m.Code)
			}
		})
	}
}

func noCache(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Expires", "0")
		w.Header().Set("Cache-Control", "no-cache, no-store, must-revalidate")
		w.Header().Set("Pragma", "no-cache")
		next.ServeHTTP(w, r)
	})
}
