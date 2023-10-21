package entity

type (
	Transaction struct {
		TransactionID       string
		SenderCardNumber    string
		Validity            string
		CVC                 string
		RecipientCardNumber string
		BankGateway         Bank
		SenderBank          Bank
		Amount              int64
	}

	Confirm struct {
		TransactionID    string
		ConfirmationСode string
	}

	Bank string
)

const (
	Tinkoff Bank = "tinkoff"
)
