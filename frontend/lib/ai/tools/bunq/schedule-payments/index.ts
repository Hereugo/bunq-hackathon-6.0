import { createSchedulePayment } from './create-schedule-payment';
import { deleteSchedulePayment } from './delete-schedule-payment';
import { getSchedulePayment } from './get-schedule-payment';
import { listSchedulePayments } from './list-schedule-payments';

export const schedulePaymentTools = {
  createSchedulePayment,
  getSchedulePayment,
  listSchedulePayments,
  deleteSchedulePayment,
};
