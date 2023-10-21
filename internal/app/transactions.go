package app

import (
	"context"
	"scam-master/internal/app/entity"
)

type (
	TransactionService interface {
		Init(ctx context.Context, transaction entity.Transaction) error
		Confirm(ctx context.Context, confirm entity.Confirm) error
	}
)
