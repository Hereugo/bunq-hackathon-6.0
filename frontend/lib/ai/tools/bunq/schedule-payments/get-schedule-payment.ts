import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const getSchedulePayment = tool({
  description:
    'Retrieve details of a specific scheduled payment using the bunq API',
  parameters: z.object({
    schedulePaymentId: z
      .number()
      .describe('The ID of the scheduled payment to retrieve'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to fetch scheduled payment from',
      ),
  }),
  execute: async ({ schedulePaymentId, monetaryAccountId }) => {
    let url = `${fastApiUrl}/schedule_payments/${schedulePaymentId}`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const schedulePayment = await response.json();
    return schedulePayment;
  },
});
