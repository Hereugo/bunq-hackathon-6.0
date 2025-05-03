import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const makeInquery = tool({
  description:
    'Makes an inquery to return money to a recipient specified by email. This tool sends an inquery request to the Bunq API and returns an inquery_id upon success.',
  parameters: z.object({
    amount: z.number(),
    currency: z.string().optional(),
    recipientEmail: z.string(),
    description: z.string().optional(),
    allow_bunqme: z.boolean().optional(),
  }),
  execute: async ({
    amount,
    currency,
    recipientEmail,
    description,
    allow_bunqme,
  }) => {
    const response = await fetch(`${fastApiUrl}/make_inquery`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount,
        currency,
        recipientEmail,
        description,
        allow_bunqme,
      }),
    });

    const message = await response.json();
    return message;
  },
});
