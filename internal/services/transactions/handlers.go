package transactions

import (
	"context"
	"scam-master/internal/app/entity"
)

func (s *transactionsService) Init(ctx context.Context, transaction entity.Transaction) error {
	return nil
}

func (s *transactionsService) Confirm(ctx context.Context, confirm entity.Confirm) error {
	return nil
}
