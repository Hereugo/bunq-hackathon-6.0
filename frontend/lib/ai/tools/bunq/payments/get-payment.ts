import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const getPayment = tool({
  description: 'Retrieve details of a specific payment using the bunq API',
  parameters: z.object({
    paymentId: z.number().describe('The ID of the payment to retrieve'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe('Optional ID of the monetary account to fetch payment from'),
  }),
  execute: async ({ paymentId, monetaryAccountId }) => {
    let url = `${fastApiUrl}/payments/${paymentId}`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const payment = await response.json();
    return payment;
  },
});
