import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const makePayment = tool({
  description:
    'Makes a payment to a recipient specified by email. This tool sends a payment request to the Bunq API and returns a payment_id upon success.',
  parameters: z.object({
    amount: z.number(),
    currency: z.string().optional(),
    recipientEmail: z.string(),
    description: z.string().optional(),
  }),
  execute: async ({ amount, currency, recipientEmail, description }) => {
    const response = await fetch(`${fastApiUrl}/make_payment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount,
        currency,
        recipientEmail,
        description,
      }),
    });

    const message = await response.json();
    return message;
  },
});
