import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const getRequestInquiry = tool({
  description:
    'Retrieve details of a specific request inquiry using the bunq API',
  parameters: z.object({
    inquiryId: z.number().describe('The ID of the request inquiry to retrieve'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to fetch request inquiry from',
      ),
  }),
  execute: async ({ inquiryId, monetaryAccountId }) => {
    let url = `${fastApiUrl}/request_inquiries/${inquiryId}`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const inquiry = await response.json();
    return inquiry;
  },
});
