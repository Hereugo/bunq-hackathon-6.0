import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const createDraftPayment = tool({
  description:
    'Create a draft payment that requires approval before execution using the bunq API',
  parameters: z.object({
    entries: z
      .array(
        z.object({
          amount: z
            .object({
              value: z
                .string()
                .describe(
                  'Amount to transfer as string (e.g. "10.00"). Must be positive and have max 2 decimal places.',
                ),
              currency: z
                .string()
                .length(3)
                .default('EUR')
                .describe('3-letter currency code (e.g. "EUR")'),
            })
            .describe('The payment amount and currency'),
          counterparty_alias: z
            .object({
              type: z
                .enum(['EMAIL', 'PHONE_NUMBER', 'IBAN'])
                .describe('Type of identifier for the recipient'),
              value: z
                .string()
                .describe(
                  'Value of the identifier (email address, phone number, or IBAN)',
                ),
              name: z.string().describe('Name of the recipient'),
            })
            .describe('Details of the payment recipient'),
          description: z
            .string()
            .max(140)
            .describe('Payment description (max 140 characters)'),
        }),
      )
      .describe(
        'The list of entries in the draft payment. Each entry will result in a payment when the draft payment is accepted.',
      ),
    status: z
      .enum(['ACCEPTED', 'PENDING', 'REJECTED'])
      .default('PENDING')
      .describe('The status of the draft payment'),
    number_of_required_accepts: z
      .number()
      .default(1)
      .describe(
        'The number of accepts required for the draft payment to be executed',
      ),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to create the draft payment from',
      ),
  }),
  execute: async ({
    entries,
    status,
    number_of_required_accepts,
    monetaryAccountId,
  }) => {
    let url = `${fastApiUrl}/draft_payments/`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        entries,
        status,
        number_of_required_accepts,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('Error creating draft payment:', error);
      return error;
    }

    const result = await response.json();
    return result;
  },
});
