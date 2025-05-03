import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const createSchedulePayment = tool({
  description: 'Create a scheduled payment using the bunq API',
  parameters: z.object({
    payment: z
      .object({
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
          .describe('Payment description (max 140 characters)'),
      })
      .describe('The payment details for the scheduled payment'),
    schedule: z
      .object({
        time_start: z
          .string()
          .describe(
            'Start time for the schedule in format "YYYY-MM-DD hh:mm:ss"',
          ),
        time_end: z
          .string()
          .optional()
          .describe(
            'Optional end time for the schedule in format "YYYY-MM-DD hh:mm:ss"',
          ),
        recurrence_unit: z
          .enum(['ONCE', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'])
          .default('ONCE')
          .describe('The schedule recurrence unit'),
        recurrence_size: z
          .number()
          .default(1)
          .describe('Recurrence size for the schedule (e.g., every 1 day)'),
      })
      .describe('Schedule details for the payment'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to create the scheduled payment from',
      ),
  }),
  execute: async ({ payment, schedule, monetaryAccountId }) => {
    let url = `${fastApiUrl}/schedule_payments/`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        payment,
        schedule,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error creating scheduled payment:', errorData);
      return errorData;
    }

    const result = await response.json();
    return result;
  },
});
