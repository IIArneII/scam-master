package rest

import (
	"net/http"
	"scam-master/internal/app/conversions"
	"scam-master/internal/pkg/openapi/restapi/operations"
	"scam-master/internal/pkg/openapi/restapi/operations/transactions"
)

func (svc *service) initTransactionsHandlers(api *operations.ScamMasterAPI) {
	api.TransactionsInitHandler = transactions.InitHandlerFunc(svc.initTransaction)
	api.TransactionsConfirmHandler = transactions.ConfirmHandlerFunc(svc.confirmTransaction)
}

func (svc *service) initTransaction(params transactions.InitParams) transactions.InitResponder {
	op := "Initialize funds transfer from card to card: "
	resp := transactions.NewInitDefault(http.StatusInternalServerError)

	err := svc.services.TransactionService.Init(params.HTTPRequest.Context(), conversions.TransactionFromRest(*params.Body))
	if err != nil {
		setAPIError(svc.l, op, err, resp)
		return resp
	}

	return transactions.NewInitNoContent()
}

func (svc *service) confirmTransaction(params transactions.ConfirmParams) transactions.ConfirmResponder {
	op := "Confirm the funds transfer with a confirmation code: "
	resp := transactions.NewConfirmDefault(http.StatusInternalServerError)

	err := svc.services.TransactionService.Confirm(params.HTTPRequest.Context(), conversions.СonfirmFromRest(*params.Body))
	if err != nil {
		setAPIError(svc.l, op, err, resp)
		return resp
	}

	return transactions.NewConfirmNoContent()
}
