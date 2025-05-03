import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const createRequestInquiry = tool({
  description:
    'Create a payment request to another bank account using the bunq API',
  parameters: z.object({
    amount: z
      .object({
        value: z
          .string()
          .describe(
            'Amount to request as string (e.g. "10.00"). Must be positive and have max 2 decimal places.',
          ),
        currency: z
          .string()
          .length(3)
          .default('EUR')
          .describe('3-letter currency code (e.g. "EUR")'),
      })
      .describe('The request amount and currency'),
    counterparty: z
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
      .describe('Request description (max 140 characters)'),
  }),
  execute: async ({ amount, counterparty, description }) => {
    const response = await fetch(`${fastApiUrl}/request_inquiries/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount,
        counterparty,
        description,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const result = await response.json();
    return result;
  },
});
