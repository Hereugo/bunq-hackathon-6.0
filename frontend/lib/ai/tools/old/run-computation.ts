import { tool } from 'ai';
import { z } from 'zod';

export const runComputation = tool({
  description:
    'Run a JavaScript expression, DO NOT USE FOR ANY CODE BUT COMPUTATIONAL PURPOSES',
  parameters: z.object({
    expression: z.string(),
  }),
  execute: async ({ expression }) => {
    try {
      // eslint-disable-next-line no-eval
      const result = eval(expression);
      return { result };
    } catch (error) {
      return { details: `Error: ${error}` };
    }
  },
});
