import { FC } from 'react';
import { Skeleton } from '../ui/skeleton';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '../ui/card';
import { Badge } from '../ui/badge';
import { Check, X } from 'lucide-react';

interface PaymentData {
  payment_id?: number;
  message?: string;
  payment?: {
    amount: {
      value: string;
      currency: string;
    };
    counterparty: {
      type: string;
      value: string;
      name: string;
    };
    description: string;
  };
  detail?: string;
}

interface Props {
  isReadonly: boolean;
  result?: PaymentData;
  args?: any; // Replace with actual type
}

export const CreatePayment: FC<Props> = ({ isReadonly, result, args }) => {
  if (!result) {
    return <Skeleton className="h-80 w-full max-w-sm" />;
  }

  if (result.detail) {
    return (
      <Card className="max-w-sm">
        <CardHeader className="pb-3">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg">Payment Details</CardTitle>
            <Badge
              variant="outline"
              className="bg-red-100 text-red-800 flex items-center gap-1"
            >
              <X className="h-3 w-3" />
              Error
            </Badge>
          </div>
          <CardDescription>{result.detail}</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="max-w-sm">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg">Payment Details</CardTitle>
          {result.message && (
            <Badge
              variant="outline"
              className="bg-green-100 text-green-800 flex items-center gap-1"
            >
              <Check className="h-3 w-3" />
              Success
            </Badge>
          )}
        </div>
        <CardDescription>
          {result.payment_id && `Payment ID: ${result.payment_id}`}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {result.payment && (
          <>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Amount</span>
              <span className="font-medium">
                {result.payment.amount.value} {result.payment.amount.currency}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Recipient</span>
              <span className="font-medium">
                {result.payment.counterparty.name}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Contact</span>
              <span className="text-sm">
                {result.payment.counterparty.value}
              </span>
            </div>

            <div className="pt-2 border-t">
              <span className="text-muted-foreground text-sm">Description</span>
              <p className="mt-1">{result.payment.description}</p>
            </div>
          </>
        )}
      </CardContent>
      <CardFooter className="bg-muted/50 text-xs text-muted-foreground pt-3">
        {result.message}
      </CardFooter>
    </Card>
  );
};

interface GetPaymentProps {
  isReadonly: boolean;
  result?: any;
  args?: any; // Replace with actual type
}

// GetPayment component to display a single payment's details
export const GetPayment: FC<GetPaymentProps> = ({
  isReadonly,
  result,
  args,
}) => {
  if (!result) {
    return <Skeleton className="h-80 w-full max-w-sm" />;
  }

  if (result.detail) {
    return (
      <Card className="max-w-sm">
        <CardHeader className="pb-3">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg">Payment Details</CardTitle>
            <Badge
              variant="outline"
              className="bg-red-100 text-red-800 flex items-center gap-1"
            >
              <X className="h-3 w-3" />
              Error
            </Badge>
          </div>
          <CardDescription>{result.detail}</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="max-w-sm">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg">Payment Details</CardTitle>
          {result.message && (
            <Badge
              variant="outline"
              className="bg-green-100 text-green-800 flex items-center gap-1"
            >
              <Check className="h-3 w-3" />
              View
            </Badge>
          )}
        </div>
        <CardDescription>
          {result.payment_id && `Payment ID: ${result.payment_id}`}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {result.payment && (
          <>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Amount</span>
              <span className="font-medium">
                {result.payment._amount._value}{' '}
                {result.payment._amount._currency}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Recipient</span>
              <span className="font-medium">
                {
                  result.payment._counterparty_alias.label_monetary_account
                    ._display_name
                }
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Contact</span>
              <span className="text-sm">
                {
                  result.payment._counterparty_alias.label_monetary_account
                    ._iban
                }
              </span>
            </div>

            <div className="pt-2 border-t">
              <span className="text-muted-foreground text-sm">Description</span>
              <p className="mt-1">{result.payment._description}</p>
            </div>
          </>
        )}
      </CardContent>
      <CardFooter className="bg-muted/50 text-xs text-muted-foreground pt-3">
        {result.message}
      </CardFooter>
    </Card>
  );
};

interface ListPaymentsProps {
  isReadonly: boolean;
  result?: { detail?: string; payments?: any[] };
  args?: any;
}

export const ListPayments: FC<ListPaymentsProps> = ({
  isReadonly,
  result,
  args,
}) => {
  if (!result) {
    return <Skeleton className="h-60 w-full max-w-sm" />;
  }

  // Check if result has a detail property (error)
  if (result && typeof result === 'object' && 'detail' in result) {
    return (
      <Card className="max-w-sm">
        <CardHeader className="pb-3">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg">Payments</CardTitle>
            <Badge
              variant="outline"
              className="bg-red-100 text-red-800 flex items-center gap-1"
            >
              <X className="h-3 w-3" />
              Error
            </Badge>
          </div>
          <CardDescription>{result.detail}</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  // If it's a success response with payments array in result.payments
  const payments = result.payments || [];
  const needsScrolling = payments.length > 5;

  // Create a function to format the footer text
  const getFooterText = () => {
    if (payments.length === 0) {
      return 'No payments available';
    }
    const suffix = payments.length !== 1 ? 's' : '';
    return `Showing ${payments.length} payment${suffix}`;
  };

  return (
    <Card className="max-w-sm">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg">Payments</CardTitle>
          <Badge variant="outline" className="flex items-center gap-1">
            {payments.length} {payments.length === 1 ? 'Payment' : 'Payments'}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        {payments.length === 0 ? (
          <div className="text-center text-muted-foreground py-4">
            No payments found
          </div>
        ) : (
          <div
            className={
              needsScrolling
                ? 'h-60 overflow-y-auto pr-1 scrollbar-thin'
                : 'h-auto'
            }
          >
            <div className="space-y-2">
              {payments.map((payment, index) => (
                <div
                  key={`payment-${payment._id_ || index}-${Date.now()}`}
                  className="text-sm p-3 rounded-md bg-muted/50 hover:bg-muted transition-colors"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-medium">
                      {payment._amount?._value} {payment._amount?._currency}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      ID: {payment._id_}
                    </span>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-xs">
                      {
                        payment._counterparty_alias?.label_monetary_account
                          ?._display_name
                      }
                    </span>
                    <Badge variant="outline" className="text-xs h-5">
                      {payment._payment_arrival_expected._status || 'COMPLETED'}
                    </Badge>
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground overflow-hidden text-ellipsis whitespace-nowrap">
                    {payment._description}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter className="bg-muted/50 text-xs text-muted-foreground pt-3">
        {getFooterText()}
      </CardFooter>
    </Card>
  );
};
