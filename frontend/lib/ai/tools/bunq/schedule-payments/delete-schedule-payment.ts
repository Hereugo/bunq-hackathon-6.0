import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const deleteSchedulePayment = tool({
  description: 'Delete a scheduled payment using the bunq API',
  parameters: z.object({
    schedulePaymentId: z
      .number()
      .describe('The ID of the scheduled payment to delete'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account the scheduled payment belongs to',
      ),
  }),
  execute: async ({ schedulePaymentId, monetaryAccountId }) => {
    let url = `${fastApiUrl}/schedule_payments/${schedulePaymentId}`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error deleting:', errorData);
      return errorData;
    }

    const result = await response.json();
    return result;
  },
});
