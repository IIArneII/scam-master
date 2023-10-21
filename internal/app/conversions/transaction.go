package conversions

import (
	"scam-master/internal/app/entity"
	"scam-master/internal/pkg/openapi/models"
)

func TransactionFromRest(transaction models.Transaction) entity.Transaction {
	return entity.Transaction{
		TransactionID:       *transaction.TransactionID,
		SenderCardNumber:    *transaction.SenderCardNumber,
		Validity:            *transaction.Validity,
		CVC:                 *transaction.Cvc,
		RecipientCardNumber: *transaction.RecipientCardNumber,
		BankGateway:         BankFromRest(*transaction.BankGateway),
		SenderBank:          BankFromRest(*transaction.SenderBank),
		Amount:              *transaction.Amount,
	}
}

func СonfirmFromRest(transaction models.Сonfirm) entity.Confirm {
	return entity.Confirm{
		TransactionID:    *transaction.TransactionID,
		ConfirmationСode: *transaction.ConfirmationСode,
	}
}

func BankFromRest(bank string) entity.Bank {
	switch bank {
	case "tinkoff":
		return entity.Tinkoff
	default:
		panic("Unknown rest bank: " + bank)
	}
}
