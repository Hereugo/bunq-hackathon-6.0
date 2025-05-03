// filepath: /Users/nomomon/Desktop/Projects/bunq-hackathon-6.0/frontend/components/bunq/request-inquiries.tsx
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

interface RequestInquiryData {
  inquiry_id?: number;
  message?: string;
  inquiry?: {
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
  result?: RequestInquiryData;
  args?: any; // Replace with actual type
}

export const CreateRequestInquiry: FC<Props> = ({
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
            <CardTitle className="text-lg">Payment Request</CardTitle>
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
          <CardTitle className="text-lg">Payment Request</CardTitle>
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
          {result.inquiry_id && `Request ID: ${result.inquiry_id}`}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {result.inquiry && (
          <>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Amount</span>
              <span className="font-medium">
                {result.inquiry.amount.value} {result.inquiry.amount.currency}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Recipient</span>
              <span className="font-medium">
                {result.inquiry.counterparty.name}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Contact</span>
              <span className="text-sm">
                {result.inquiry.counterparty.value}
              </span>
            </div>

            <div className="pt-2 border-t">
              <span className="text-muted-foreground text-sm">Description</span>
              <p className="mt-1">{result.inquiry.description}</p>
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

interface GetRequestInquiryProps {
  isReadonly: boolean;
  result?: any;
  args?: any;
}

export const GetRequestInquiry: FC<GetRequestInquiryProps> = ({
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
            <CardTitle className="text-lg">Payment Request Details</CardTitle>
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
          <CardTitle className="text-lg">Payment Request Details</CardTitle>
          <Badge variant="outline" className="flex items-center gap-1">
            <Check className="h-3 w-3" />
            View
          </Badge>
        </div>
        <CardDescription>
          {result.inquiry_id && `Request ID: ${result.inquiry_id}`}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {result.inquiry && (
          <>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Amount</span>
              <span className="font-medium">
                {result.inquiry._amount_inquired._value}{' '}
                {result.inquiry._amount_inquired._currency}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Recipient</span>
              <span className="font-medium">
                {
                  result.inquiry._counterparty_alias.label_monetary_account
                    ._display_name
                }
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-muted-foreground">Status</span>
              <span className="font-medium">{result.inquiry._status}</span>
            </div>

            <div className="pt-2 border-t">
              <span className="text-muted-foreground text-sm">Description</span>
              <p className="mt-1">{result.inquiry._description}</p>
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

interface ListRequestInquiriesProps {
  isReadonly: boolean;
  result?: { detail?: string; inquiries?: any[] };
  args?: any;
}

export const ListRequestInquiries: FC<ListRequestInquiriesProps> = ({
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
            <CardTitle className="text-lg">Payment Requests</CardTitle>
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

  const inquiries = Array.isArray(result.inquiries) ? result.inquiries : [];
  const needsScrolling = inquiries.length > 5;

  // Create a function to format the footer text to avoid nested ternary
  const getFooterText = () => {
    if (inquiries.length === 0) {
      return 'No payment requests available';
    }

    const suffix = inquiries.length !== 1 ? 's' : '';
    return `Showing ${inquiries.length} payment request${suffix}`;
  };

  return (
    <Card className="max-w-sm">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg">Payment Requests</CardTitle>
          <Badge variant="outline" className="flex items-center gap-1">
            {inquiries.length} {inquiries.length === 1 ? 'Request' : 'Requests'}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        {inquiries.length === 0 ? (
          <div className="text-center text-muted-foreground py-4">
            No payment requests found
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
              {inquiries.map((inquiry, index) => (
                <div
                  key={`inquiry-${inquiry._id_ || index}-${Date.now()}`}
                  className="text-sm p-3 rounded-md bg-muted/50 hover:bg-muted transition-colors"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-medium">
                      {inquiry._amount?._value} {inquiry._amount?._currency}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      ID: {inquiry._id_}
                    </span>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-xs">
                      {
                        inquiry._counterparty_alias?.label_monetary_account
                          ?._display_name
                      }
                    </span>
                    <Badge variant="outline" className="text-xs h-5">
                      {inquiry._status}
                    </Badge>
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground overflow-hidden text-ellipsis whitespace-nowrap">
                    {inquiry._description}
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
